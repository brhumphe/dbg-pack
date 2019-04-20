from .struct_reader import BinaryStructReader
from .abc import AbstractAsset
from dataclasses import dataclass
import zlib


@dataclass()
class Asset2(AbstractAsset):
    name_hash: int
    file_offset: int
    size: int
    crc32: int
    path: str
    name: str = None
    
    def __init__(self, reader: BinaryStructReader, path: str):
        self.path = path
        self.name_hash = reader.uint64LE()
        self.file_offset = reader.uint64LE()
        self.size = reader.uint64LE()
        self._zipped_flag = reader.uint32LE()
        self.crc32 = reader.uint32LE()

    @property
    def isZipped(self) -> bool:
        with BinaryStructReader(self.path) as reader:
            reader.seek(self.file_offset)
            if reader.peek(1)[:4] == b'\xa1\xb2\xc3\xd4':
                return True
            else:
                return False
    
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
