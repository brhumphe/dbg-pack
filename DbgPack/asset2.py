import contextlib
import struct
from dataclasses import dataclass, field
from pathlib import Path
from zlib import decompress

from .abc import AbstractAsset
from .struct_reader import BinaryStructReader


@dataclass
class Asset2(AbstractAsset):
    name: str = field(default=None)
    path: Path = field(default=None)

    name_hash: int = field(default=None)
    offset: int = field(default=0)
    data_length: int = field(default=0)  # data_length should refer to stored data size
    unzipped_length: int = field(default=None)  # unzipped_length should refer to the real size
    is_zipped: bool = field(default=False)
    zipped_flag: int = field(default=None)
    data_hash: int = field(default=0)

    md5: str = field(default=None)

    ZIP_MAGIC = b'\xa1\xb2\xc3\xd4'

    def __post_init__(self):
        assert self.name_hash, 'name_hash is required'
        assert self.path, 'path is required'

    def get_data(self, raw=False, *, reader=None) -> bytes:
        if self.data_length == 0:
            return bytes()

        if reader is None:
            cm = BinaryStructReader(self.path)
        else:
            # Don't reopen an open reader
            cm = contextlib.nullcontext(reader)

        with cm as r:
            r.seek(self.offset)
            data = r.read(self.data_length)
            # Check if compressed
            if raw or data[:4] != self.ZIP_MAGIC:
                return data
            else:
                self.unzipped_length = struct.unpack_from('<I', data, 4)[0]
                # Skip 8 bytes to start of zip data
                return decompress(data[8:])
