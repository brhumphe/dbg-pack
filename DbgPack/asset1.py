import contextlib
from dataclasses import dataclass, field
from pathlib import Path

from .abc import AbstractAsset
from .struct_reader import BinaryStructReader


@dataclass
class Asset1(AbstractAsset):
    name: str = field(default=None)
    path: Path = field(default=None)

    offset: int = field(default=0)
    data_length: int = field(default=0)
    data_hash: int = field(default=0)

    md5: str = field(default=None)

    def __post_init__(self):
        assert self.name, 'name is required'
        assert self.path, 'path is required'

    def get_data(self, raw=False, reader=None) -> bytes:
        # No raw data, so just ignore it
        if self.data_length == 0:
            return bytes()

        if reader is None:
            cm = BinaryStructReader(self.path)
        else:
            # Don't reopen an open reader
            cm = contextlib.nullcontext(reader)

        with cm as r:
            r.seek(self.offset)
            return r.read(self.data_length)

    def __len__(self):
        return super().__len__()
