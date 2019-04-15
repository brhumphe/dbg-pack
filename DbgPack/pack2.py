from dataclasses import dataclass
from typing import Dict

from .struct_reader import BinaryStructReader
from .abc import AbstractPack
from .asset2 import Asset2


@dataclass()
class Pack2(AbstractPack):
    asset_count: int
    file_size: int
    map_offset: int
    unknown1: int
    unknownChecksum: bytes
    assets: Dict[str, Asset2]
    
    def __init__(self, path: str):
        super().__init__(path)
        with BinaryStructReader(path) as reader:
            magic = reader.read(4)
            print(magic)
            assert magic == b'PAK\x01'
            self.asset_count = reader.uintLE()
            self.file_size = reader.ulonglongLE()
            self.map_offset = reader.ulonglongLE()
            
            reader.seek(self.map_offset)
            for i in range(self.asset_count):
                print(Asset2(reader, path))
                
