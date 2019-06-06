import zlib
from dataclasses import dataclass, field, InitVar
from binascii import crc32

from DbgPack.struct_reader import BinaryStructReader
from DbgPack.hash import crc64


@dataclass
class Asset:
    """Class for managing data of a single asset file.

    If data is not set, it will be read from path at the specified offset"""
    name: str = field(default="")
    name_hash: int = field(default=None)
    crc32: int = field(default=None)
    offset: int = field(default=0)
    length: int = field(default=0)
    # isZipped: bool = False
    path: str = ""
    _data: bytes = field(init=False, repr=False, default=None, compare=False)

    def __post_init__(self):
        if self.name and not self.name_hash:
            self.name_hash = crc64(self.name)

    @property
    def data(self):
        if self._data:
            return self._data
        if self.length == 0:
            return bytes()

        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            if reader.peek(1)[:4] != b'\xa1\xb2\xc3\xd4':
                return reader.read(self.length)
            else:
                compression = reader.read(4)
                assert compression == b'\xa1\xb2\xc3\xd4'
                unpacked_size = reader.uint32BE()
                compressed = reader.read(self.length)
                return zlib.decompress(compressed)

    def __len__(self):
        return self.length

    @classmethod
    def from_bytes(cls, name: str, data: bytes):
        instance = cls(name=name)
        instance._data = data
        instance.length = len(data)
        instance.crc32 = crc32(data)
    
        return instance
