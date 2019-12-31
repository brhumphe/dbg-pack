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
    data_length: int = field(default=0)  # data_length should refer to stored data size
    unzipped_length: int = field(default=0)  # unzipped_length should refer to the real size
    is_zipped: bool = field(default=False)
    data_hash: int = field(default=0)

    _md5: str = field(default=None)

    ZIP_MAGIC = b'\xa1\xb2\xc3\xd4'

    def __post_init__(self):
        assert self.name_hash, 'name_hash is required'
        assert self.path, 'path is required'
        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            self.is_zipped = reader.peek(len(self.ZIP_MAGIC))[:4] == self.ZIP_MAGIC

    def get_data(self, raw=False) -> bytes:
        if self.data_length == 0:
            return bytes()

        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            if raw:
                return reader.read(self.data_length)

            if self.is_zipped:
                # return unzipped data
                zip_magic = reader.read(len(self.ZIP_MAGIC))
                assert zip_magic == self.ZIP_MAGIC, 'invalid zip magic'
                unzipped_len = reader.uint32BE()
                # Unzipped length may not always be set in the constructor, but user shouldn't have to always set it.
                # assert self.unzipped_length == unzipped_len, 'unzipped length mismatch'
                return decompress(reader.read(self.data_length))

            else:  # Not zipped
                return reader.read(self.data_length)

    @property
    def md5(self) -> str:
        return super().md5

    def __len__(self):
        return super().__len__()
