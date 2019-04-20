from dataclasses import dataclass
from typing import Dict, List

from .struct_reader import BinaryStructReader
from .abc import AbstractPack
from .asset2 import Asset2
from .hash import crc64


@dataclass()
class Pack2(AbstractPack):
    asset_count: int
    file_size: int
    map_offset: int
    assets: Dict[str, Asset2]
    raw_assets: Dict[int, Asset2]
    path: str

    def __init__(self, path: str):
        super().__init__(path)
        self.path = path
        with BinaryStructReader(path) as reader:
            magic = reader.read(4)
            assert magic == b'PAK\x01'
            self.asset_count = reader.uint32LE()
            self.file_size = reader.uint64LE()
            self.map_offset = reader.uint64LE()

            reader.seek(self.map_offset)
            self.raw_assets = {}
            for i in range(self.asset_count):
                asset = Asset2(reader, path)
                self.raw_assets.update({int(asset.name_hash): asset})

        self._update_asset_names()

    def _update_asset_names(self):
        # Build assets dict with proper names
        self.assets = {}
        namelist = self.raw_assets[0x4137cc65bd97fd30].data.split()
        for name in namelist:
            name = str(name, encoding='ascii')
            name_hash = crc64(name)
            try:
                asset = self.raw_assets[name_hash]
                asset.name = name
                self.assets.update({name: asset})
            except KeyError:
                print("Could not find", name, "in", self.path)
                pass

        # TODO: Identify assets which were not contained in the name list

    def __repr__(self):
        return f"Pack2(\"{self.path}\")"

    def __getitem__(self, item):
        return self.assets[item]

    def __len__(self):
        return len(self.assets)
