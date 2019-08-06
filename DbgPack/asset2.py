from dataclasses import dataclass, field
from pathlib import Path
from zlib import decompress

from .abc import AbstractAsset
from .struct_reader import BinaryStructReader


@dataclass
class Asset2(AbstractAsset):
    name: str = field(default='')
    path: Path = field(default=None)

    name_hash: int = field(default=None)
    offset: int = field(default=0)
    size: int = field(default=0)
    # zipped: bool
    crc32: int = field(default=0)

    def __post_init__(self):
        assert self.name_hash, 'name_hash is required'
        assert self.path, 'path is required'

    @property
    def data(self) -> bytes:
        zip_magic = b'\xa1\xb2\xc3\xd4'

        if self.size == 0:
            return bytes()

        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            if reader.peek(1)[:len(zip_magic)] != zip_magic:
                return reader.read(self.size)
            else:
                assert reader.read(len(zip_magic)) == zip_magic, 'invalid zip magic'
                unzip_size = reader.uint32BE()
                return decompress(reader.read(self.size))

    def __len__(self):
        return super().__len__()
