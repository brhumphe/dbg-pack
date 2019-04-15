from collections import ChainMap
from dataclasses import dataclass, field
from typing import List
from typing import ChainMap as ChainMapType

from DbgPack.abc import AbstractPack, AbstractAsset


@dataclass()
class AssetManager:
    packs: List[AbstractPack] = field(default_factory=list)
    assets: ChainMapType[str, AbstractAsset] = field(default_factory=ChainMap, repr=False, init=False)

    def __init__(self, packs: List[str]):
        self.packs = [AbstractPack(path) for path in packs]
        self.assets = ChainMap(*[p.assets for p in self.packs])

    def __getitem__(self, item):
        return self.assets[item]

    def __contains__(self, item):
        return item in self.assets

    def __len__(self):
        return len(self.assets)

    def __iter__(self):
        return iter(self.assets.values())
