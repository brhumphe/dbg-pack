from dataclasses import dataclass, field
from pathlib import Path
from binascii import crc32
from re import fullmatch

from .abc import AbstractAsset
from .hash import crc64


# TODO: Handle file modifications after load


@dataclass
class LooseAsset(AbstractAsset):
    name: str
    name_hash: int
    path: Path

    size: int
    crc32: int

    def __init__(self, name: str, path: Path):
        mo = fullmatch(r'(0x[a-fA-F0-9]{16}).bin', name)
        if mo:
            print(mo)
            self.name = ''
            self.name_hash = int(mo[0], 0)

        else:
            self.name = name
            self.name_hash = crc64(name)

        self.path = path

        self.size = (self.path / self.name).stat().st_size
        self.crc32 = crc32((self.path / self.name).read_bytes())

    @property
    def data(self) -> bytes:
        return (self.path / self.name).read_bytes() if self.size > 0 else bytes()

    def __len__(self):
        return super().__len__()
