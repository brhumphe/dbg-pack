from collections import ChainMap
from dataclasses import dataclass, field
from multiprocessing import Event
from pathlib import Path
from typing import List, ChainMap as ChainMapType, Callable, Optional, Union
import multiprocessing.pool as pool
import os

from .abc import AbstractPack, AbstractAsset
from .asset2 import Asset2
from .hash import crc64
from .loose_pack import LoosePack
from .pack1 import Pack1
from .pack2 import Pack2


@dataclass
class AssetManager:
    packs: List[AbstractPack]
    assets: ChainMapType[str, AbstractAsset] = field(repr=False)

    @staticmethod
    def load_pack(path: Path, namelist: List[str] = None):
        if path.is_file():
            if path.suffix == '.pack':
                return Pack1(path)
            elif path.suffix == '.pack2':
                return Pack2(path, namelist=namelist)
        else:
            return LoosePack(path)

    def export_pack2(self, name: str, outdir: Path, raw=False):
        Pack2.export(list(self.assets.values()), name, outdir, raw)

    def __init__(self, paths: List[Path], namelist: List[str] = None, p: pool.Pool = None):
        self.loaded = Event()
        self.pool = p
        if self.pool:
            self.pool.starmap_async(
                AssetManager.load_pack, 
                [[path, namelist] for path in paths],
                callback=self.loaded_callback
            )
        else:
            self.packs = [AssetManager.load_pack(path, namelist=namelist) for path in paths]
            self.assets = ChainMap(*[p.assets for p in self.packs])
            self.loaded.set()

    def loaded_callback(self, packs: List[Union[Pack1, Pack2, LoosePack]]):
        self.packs = packs   
        self.assets = ChainMap(*[p.assets for p in self.packs])
        self.loaded.set()
    
    def refresh_assets(self, *_):
        self.assets = ChainMap(*[p.assets for p in self.packs])

    def __len__(self):
        if not self.loaded.is_set():
            return 0
        return len(self.assets)

    def __getitem__(self, item):
        if not self.loaded.is_set():
            raise KeyError("Assets not loaded!")
        return self.assets[item]

    def __contains__(self, item):
        if not self.loaded.is_set():
            return False
        return item in self.assets

    def __iter__(self):
        if not self.loaded.is_set():
            return iter([])
        return iter(self.assets.values())
    
    def search(self, term: str, suffix: str = ""):
        names = []
        if not self.loaded.is_set():
            return names
        for key in self.assets.values():
            if term.lower() in key.name.lower() and key.name.endswith(suffix):
                names.append(key.name)
        names.sort()
        return names
    
    def get_raw(self, name: str) -> Optional[Asset2]:
        if not self.loaded.is_set():
            return None
        name_hash = crc64(name.encode("ascii"))
        for pack in self.packs:
            assert type(pack) == Pack2
            if name_hash in pack.raw_assets:
                return pack.raw_assets[name_hash]
        return None
    
    def save_raw(self, name: str, dest_dir: str="./") -> bool:
        to_save = self.get_raw(name)
        if to_save is not None:
            try:
                with open(dest_dir + name, "wb") as f:
                    f.write(to_save.get_data())
            except Exception as e:
                print(e)
                return False
            return True
        return False
    
    def search_magic(self, magic: bytes):
        names = []
        if not self.loaded.is_set():
            return names
        for pack in self.packs:
            for namehash, asset in pack.raw_assets.items():
                data = asset.get_data()
                if data[:4] == magic:
                    names.append(asset.name if asset.name != '' else str(namehash))
        return names
    
    def assets_by_magic(self, magic: bytes):
        assets = []
        if not self.loaded.is_set():
            return assets
        for pack in self.packs:
            for namehash, asset in pack.raw_assets.items():
                data = asset.get_data()
                if data[:4] == magic:
                    assets.append(asset)
        return assets
    
    def assets_by_content(self, content: bytes):
        assets = []
        if not self.loaded.is_set():
            return assets
        for pack in self.packs:
            for namehash, asset in pack.raw_assets.items():
                data = asset.get_data()
                if content in data:
                    assets.append(asset)
        return assets
    
    def export_all_of_magic(self, magic: bytes, callback: Callable = lambda x, y, z: None, suffix: str = None):
        if not self.loaded.is_set():
            return None
        assert len(magic) == 4
        i = 0
        total = 0
        for pack in self.packs:
            total += len(pack.raw_assets)
        for pack in self.packs:
            for namehash, asset in pack.raw_assets.items():
                name = str(namehash) + "." + (suffix if suffix is not None else str(magic, encoding="utf-8").strip().lower())
                if asset.name != '':
                    name = asset.name
                callback(i, total, Path(name))
                i += 1
                data = asset.get_data()
                if data[:4] == magic:
                    if not os.path.exists(pack.name):
                        os.makedirs(pack.name, exist_ok=True)
                    if os.path.exists(pack.name + os.sep + name):
                        continue
                    with open(pack.name + os.sep + name, "wb") as f:
                        f.write(data)
                    
    
    def save(self, key: str):
        if not self.loaded.is_set():
            return None
        with open(key, "wb") as f:
            f.write(self.assets[key].get_data())
    
    def save_as(self, key: str, path: str):
        if not self.loaded.is_set():
            return None
        with open(path, "wb") as f:
            f.write(self.assets[key].get_data())

    def save_raw_as(self, key: str, dest: str):
        to_save = self.get_raw(key)
        if to_save is not None:
            try:
                with open(dest, "wb") as f:
                    f.write(to_save.get_data())
            except Exception as e:
                print(e)
                return False
            return True
        return False
