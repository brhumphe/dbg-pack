import hashlib
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict


class AbstractAsset(ABC):
    name: str
    path: Path

    data_length: int
    data_hash: int

    _md5: str

    @abstractmethod
    def get_data(self, raw=False) -> bytes:
        pass

    @property
    @abstractmethod
    def md5(self) -> str:
        if self._md5 is None:
            hash_md5 = hashlib.md5()
            hash_md5.update(self.get_data())
            self._md5 = hash_md5.hexdigest()

        return self._md5

    # This should return the stored size of the asset
    @abstractmethod
    def __len__(self):
        return self.data_length


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
