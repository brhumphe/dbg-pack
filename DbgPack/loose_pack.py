from dataclasses import dataclass
from typing import Dict
from pathlib import Path
from os import walk
from re import fullmatch

from .abc import Pack
from .loose_asset import LooseAsset


# TODO: This class may be unnecessary
@dataclass
class LoosePack(Pack):
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
