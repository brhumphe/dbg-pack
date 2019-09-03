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
    crc32: int = field(default=0)

    ZIP_MAGIC = b'\xa1\xb2\xc3\xd4'

    def __post_init__(self):
        assert self.name_hash, 'name_hash is required'
        assert self.path, 'path is required'

    def get_data(self, raw=False) -> bytes:
        if self.data_length == 0:
            return bytes()

        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            if self.is_zipped:
                if raw:
                    # Return raw data
                    return reader.read(self.data_length)

                # return unzipped data
                assert reader.read(len(self.ZIP_MAGIC)) == self.ZIP_MAGIC, 'invalid zip magic'
                assert self.unzipped_length == reader.uint32BE(), 'unzipped length mismatch'
                return decompress(reader.read(self.data_length))

            else:  # Not zipped
                # return raw data
                return reader.read(self.data_length)

    # This will return the length of the stored data, not the unpacked length
    def __len__(self):
        return self.data_length
