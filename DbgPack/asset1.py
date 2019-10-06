from dataclasses import dataclass, field
from pathlib import Path

from .abc import Asset
from .struct_reader import BinaryStructReader


@dataclass
class Asset1(Asset):
    name: str = field(default=None)
    path: Path = field(default=None)

    offset: int = field(default=0)
    data_length: int = field(default=0)
    crc32: int = field(default=0)

    def __post_init__(self):
        assert self.name, 'name is required'
        assert self.path, 'path is required'

    def get_data(self, raw=False) -> bytes:
        # No raw data, so just ignore it
        if self.data_length == 0:
            return bytes()

        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            return reader.read(self.data_length)
