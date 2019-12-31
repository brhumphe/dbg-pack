from pathlib import Path
from typing import Dict

from .abc import AbstractPack
from .asset1 import Asset1
from .struct_reader import BinaryStructReader


class Pack1(AbstractPack):
    name: str
    path: Path

    asset_count: int
    assets: Dict[str, Asset1]

    def __init__(self, path: Path):
        super().__init__(path)

        self.assets = {}
        self.asset_count = 0
        with BinaryStructReader(self.path) as reader:
            next_chunk = -1
            while next_chunk != 0:
                next_chunk = reader.uint32BE()
                asset_count = reader.uint32BE()

                for i in range(asset_count):
                    name_length = reader.uint32BE()
                    name = reader.read(name_length).decode('utf-8')
                    offset = reader.uint32BE()
                    data_length = reader.uint32BE()
                    file_hash = reader.uint32BE()

                    asset = Asset1(name=name, path=self.path, offset=offset, data_length=data_length, data_hash=file_hash)
                    self.assets[asset.name] = asset

                self.asset_count += asset_count
                reader.seek(next_chunk)

    def __repr__(self):
        return super().__repr__()

    def __len__(self):
        return super().__len__()

    def __iter__(self):
        return super().__iter__()

    def __getitem__(self, item):
        if isinstance(item, str):
            return self.assets[item]
        else:
            raise KeyError

    def __contains__(self, item):
        super().__contains__(item)
