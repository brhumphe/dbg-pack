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

    @abstractmethod
    def __len__(self):
        return self.size


class AbstractPack(ABC):
    name: str
    path: Path

    asset_count: int
    assets: Dict[str, AbstractAsset]

    @abstractmethod
    def __init__(self, path: Path):
        self.path = path
        self.name = self.path.stem

    @abstractmethod
    def __repr__(self):
        return f'{self.__class__.__name__}("{self.path}")'

    @abstractmethod
    def __len__(self):
        return self.asset_count

    @abstractmethod
    def __iter__(self):
        return iter(self.assets.values())

    @abstractmethod
    def __getitem__(self, item):
        pass

    @abstractmethod
    def __contains__(self, item):
        try:
            return self[item] is not None
        except KeyError:
            return False
