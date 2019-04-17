from dataclasses import dataclass
from typing import Dict, List

from .struct_reader import BinaryStructReader
from .abc import AbstractPack
from .asset2 import Asset2


@dataclass()
class Pack2(AbstractPack):
    asset_count: int
    file_size: int
    map_offset: int
    assets: Dict[str, Asset2]
    
    def __init__(self, path: str):
        super().__init__(path)
        with BinaryStructReader(path) as reader:
            magic = reader.read(4)
            print(magic)
            assert magic == b'PAK\x01'
            self.asset_count = reader.uint32LE()
            self.file_size = reader.uint64LE()
            self.map_offset = reader.uint64LE()
            
            reader.seek(self.map_offset)
            self.raw_assets = {}
            for i in range(self.asset_count):
                asset = Asset2(reader, path)
                self.raw_assets.update({int(asset.name_hash): asset})
