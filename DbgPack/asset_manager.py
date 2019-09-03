from collections import ChainMap
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, ChainMap as ChainMapType

from .abc import AbstractPack, AbstractAsset
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

    def __init__(self, paths: List[Path], namelist: List[str] = None):
        self.packs = [AssetManager.load_pack(path, namelist=namelist) for path in paths]
        self.assets = ChainMap(*[p.assets for p in self.packs])

    def __len__(self):
        return len(self.assets)

    def __getitem__(self, item):
        return self.assets[item]

    def __contains__(self, item):
        return item in self.assets

    def __iter__(self):
        return iter(self.assets.values())
