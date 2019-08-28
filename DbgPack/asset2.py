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
    zipped_size: int = field(default=0)
    # zipped: bool
    crc32: int = field(default=0)

    ZIP_MAGIC = b'\xa1\xb2\xc3\xd4'

    def __post_init__(self):
        assert self.name_hash, 'name_hash is required'
        assert self.path, 'path is required'

    @property
    def data(self) -> bytes:
        if self.size == 0:
            return bytes()

        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            if reader.peek(1)[:len(self.ZIP_MAGIC)] != self.ZIP_MAGIC:
                return reader.read(self.size)
            else:
                assert reader.read(len(self.ZIP_MAGIC)) == self.ZIP_MAGIC, 'invalid zip magic'
                _ = reader.uint32BE()  # Actual size is already read and stored
                return decompress(reader.read(self.zipped_size))

    def __len__(self):
        return super().__len__()
