from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from .abc import AbstractPack
from .struct_reader import BinaryStructReader
from .asset2 import Asset2
from .hash import crc64


_MAGIC: bytes = b'PAK\x01'
_NAMELIST_HASH: int = crc64(b'{NAMELIST}')
assert _NAMELIST_HASH == 0x4137cc65bd97fd30, 'crc64 is not generated correctly'


@dataclass
class Pack2(AbstractPack):
    name: str
    path: Path

    asset_count: int
    size: int
    map_offset: int

    assets: Dict[str, Asset2]
    raw_assets: Dict[int, Asset2]

    _namelist: List[str]

    def __init__(self, path: Path, namelist: List[str] = None):
        super().__init__(path)
        self._namelist = namelist

        with BinaryStructReader(self.path) as reader:
            assert reader.read(len(_MAGIC)) == _MAGIC, 'invalid pack2 magic'
            self.asset_count = reader.uint32LE()
            self.size = reader.uint64LE()
            self.map_offset = reader.uint64LE()

            reader.seek(self.map_offset)
            self.raw_assets = {}
            for i in range(self.asset_count):
                name_hash = reader.uint64LE()
                offset = reader.uint64LE()
                size = reader.uint64LE()
                zip_flag = reader.uint32LE()
                crc32 = reader.uint32LE()

                asset = Asset2(name_hash=name_hash, crc32=crc32, offset=offset,
                               size=size, path=self.path)
                self.raw_assets[asset.name_hash] = asset

        self.assets = {}
        self._update_assets(self._namelist)

    def _update_assets(self, namelist: List[str] = None):
        name_dict = {}
        used_hashes = []

        # Check for internal namelist
        if _NAMELIST_HASH in self:
            names = self.raw_assets[_NAMELIST_HASH].data.strip().split(b'\n')
            for n in names:
                hash_ = crc64(n)
                name_dict[hash_] = n.decode('utf-8')

        # Check for external namelist
        if namelist:
            for n in namelist:
                hash_ = crc64(n)
                name_dict[hash_] = n

        # Apply names to assets
        for name_hash, name in name_dict.items():
            try:
                asset = self.raw_assets[name_hash]
                asset.name = name
                self.assets[asset.name] = asset

                used_hashes.append(name_hash)

            except KeyError:
                # This error is spammed when using a large namelist
                # TODO: Log this more efficiently
                pass

        # Remaining assets will use their hashes aas keys
        unk_assets = self.asset_count - len(self.assets)
        if unk_assets:
            for hash_ in self.raw_assets.keys() - set(used_hashes):
                asset = self.raw_assets[hash_]
                self.assets[str(hash_)] = asset

    def __repr__(self):
        return super().__repr__()

    def __len__(self):
        return super().__len__()

    def __getitem__(self, item):
        if isinstance(item, str):
            try:
                return self.assets[item]
            except KeyError:
                return self.raw_assets[crc64(item)]

        elif isinstance(item, int):
            return self.raw_assets[item]
        else:
            raise KeyError

    def __contains__(self, item):
        return super().__contains__(item)
