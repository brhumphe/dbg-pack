from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict


class AbstractAsset(ABC):
    name: str
    path: Path

    size: int
    crc32: int

    @property
    @abstractmethod
    def data(self) -> bytes:
        pass

    def __len__(self):
        return self.size


class AbstractPack(ABC):
    name: str
    path: Path

    asset_count: int
    assets: Dict[str, AbstractAsset]  # Not sure if this will work correctly

    @abstractmethod
    def __init__(self, path: Path):
        self.path = path
        self.name = self.path.stem

    def __repr__(self):
        return f'{self.__class__.__name__}("{self.path}")'

    def __len__(self):
        return self.asset_count
