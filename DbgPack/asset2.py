from .struct_reader import BinaryStructReader
from .abc import AbstractAsset
from dataclasses import dataclass
import zlib


@dataclass()
class Asset2(AbstractAsset):
    name_hash: int
    offset: int
    size: int
    crc32: int
    path: str
    name: str = None
    
    def __init__(self, reader: BinaryStructReader, path: str):
        self.path = path
        self.name_hash = reader.uint64LE()
        self.offset = reader.uint64LE()
        self.size = reader.uint64LE()
        self._zipped_flag = reader.uint32LE()
        self.isZipped = (self._zipped_flag == 0x11)
        self.crc32 = reader.uint32LE()
    
    @property
    def data(self):
        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            if not self.isZipped:
                return reader.read(self.size)

            compression = reader.read(4)
            assert compression == b'\xa1\xb2\xc3\xd4'
            unpacked_size = reader.uint32BE()
            compressed = reader.read(self.size)
            return zlib.decompress(compressed)

    def __len__(self):
        return self.size
