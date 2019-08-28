from dataclasses import dataclass, field
from pathlib import Path

from .abc import AbstractAsset
from .struct_reader import BinaryStructReader


@dataclass
class Asset1(AbstractAsset):
    name: str = field(default=None)
    path: Path = field(default=None)

    offset: int = field(default=0)
    size: int = field(default=0)
    crc32: int = field(default=0)

    def __post_init__(self):
        assert self.name, 'name is required'
        assert self.path, 'path is required'

    @property
    def data(self) -> bytes:
        if self.size == 0:
            return bytes()

        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            return reader.read(self.size)

    def __len__(self):
        return super().__len__()
