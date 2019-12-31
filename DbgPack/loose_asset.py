from binascii import crc32
from dataclasses import dataclass
from pathlib import Path
from re import fullmatch

from .abc import AbstractAsset
from .hash import crc64


# TODO: Handle file modifications after load


@dataclass
class LooseAsset(AbstractAsset):
    name: str
    name_hash: int
    path: Path

    data_length: int
    data_hash: int

    def __init__(self, name: str, path: Path):
        mo = fullmatch(r'(0x[a-fA-F0-9]{16}).bin', name)
        if mo:
            self.name_hash = int(mo.group(1), 0)

        else:
            self.name_hash = crc64(name)
        self.name = name
        self.path = path

        self.data_length = (self.path / self.name).stat().st_size
        self.crc32 = crc32((self.path / self.name).read_bytes())

    def get_data(self, raw=False) -> bytes:
        # Ignore raw for now. Maybe we can keep these in zipped files
        return (self.path / self.name).read_bytes() if self.data_length > 0 else bytes()

    def __len__(self):
        return super().__len__()
