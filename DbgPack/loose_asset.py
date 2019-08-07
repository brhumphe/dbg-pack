from dataclasses import dataclass, field
from pathlib import Path
from binascii import crc32

from .abc import AbstractAsset


# TODO: Handle file modifications after load


@dataclass
class LooseAsset(AbstractAsset):
    name: str
    path: Path

    size: int
    crc32: int

    def __init__(self, name: str, path: Path):
        self.name = name
        self.path = path

        self.size = (self.path / self.name).stat().st_size
        self.crc32 = crc32((self.path / self.name).read_bytes())

    @property
    def data(self) -> bytes:
        return (self.path / self.name).read_bytes() if self.size > 0 else bytes()

    def __len__(self):
        return super().__len__()
