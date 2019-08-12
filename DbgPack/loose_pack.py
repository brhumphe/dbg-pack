from dataclasses import dataclass
from typing import Dict
from pathlib import Path
from os import walk
from re import fullmatch

from .abc import AbstractPack
from .loose_asset import LooseAsset


@dataclass
class LoosePack(AbstractPack):
    name: str
    path: Path

    asset_count: int
    assets: Dict[str, LooseAsset]

    def __init__(self, path: Path):
        super().__init__(path)

        self.assets = {}
        for root, _, files in walk(self.path):
            for file in files:
                asset = LooseAsset(name=file, path=self.path)
                self.assets[asset.name] = asset

    def __repr__(self):
        return super().__repr__()

    def __len__(self):
        return super().__len__()

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.assets[item]
        else:
            raise KeyError

    def __iter__(self):
        return iter(self.assets.values())

    def __contains__(self, item):
        super().__contains__(item)
