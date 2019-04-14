from collections import ChainMap
from dataclasses import dataclass, field
from typing import List
from typing import ChainMap as ChainMapType

from .pack1 import Pack1
from .asset1 import Asset1


@dataclass()
class AssetManager:
    packs: List[Pack1] = field(default_factory=list)
    assets: ChainMapType[str, Asset1] = field(default_factory=ChainMap, repr=False, init=False)

    def __init__(self, packs: List[str]):
        self.packs = [Pack1(path) for path in packs]
        self.assets = ChainMap(*[p.assets for p in self.packs])

    def __getitem__(self, item):
        return self.assets[item]

    def __contains__(self, item):
        return item in self.assets

    def __len__(self):
        return len(self.assets)

    def __iter__(self):
        return iter(self.assets.values())
