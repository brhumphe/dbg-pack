from abc import ABC, abstractmethod
from typing import Dict

from DbgPack import Asset


class AbstractPack(ABC):
    path: str
    assets: Dict[str, Asset]
    
    @abstractmethod
    def __init__(self, path: str):
        pass
