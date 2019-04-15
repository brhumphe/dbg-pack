from .struct_reader import BinaryStructReader
from .abc import AbstractAsset
from dataclasses import dataclass
import zlib


@dataclass()
class Asset2(AbstractAsset):
    name_hash: int
    file_offset: int
    size: int
    isZipped: bool
    crc32: int
    path: str
    
    def __init__(self, reader: BinaryStructReader, path: str):
        self.path = path
        self.name_hash = reader.uint64LE()
        self.file_offset = reader.uint64LE()
        self.size = reader.uint64LE()
        zipped = reader.uint32LE()
        if zipped == 0x1:
            self.isZipped = True
        else:
            self.isZipped = False
        
        self.crc32 = reader.uint32LE()
    
    @property
    def data(self):
        with BinaryStructReader(self.path) as reader:
            reader.seek(self.file_offset)
            if not self.isZipped:
                return reader.read(self.size)
            
            compression = reader.read(4)
            unpacked_size = reader.uint32BE()
            compressed = reader.read(self.size)
            return zlib.decompress(compressed)
            
            
            