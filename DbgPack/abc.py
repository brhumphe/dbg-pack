from abc import ABC, abstractmethod
from typing import Dict


class AbstractAsset(ABC):
    @property
    @abstractmethod
    def data(self):
        pass


class AbstractPack(ABC):
    path: str
    assets: Dict[str, AbstractAsset]
    
    @abstractmethod
    def __init__(self, path: str):
        pass
