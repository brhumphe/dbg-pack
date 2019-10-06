from pathlib import Path
from typing import Dict

from .abc import Pack
from .asset1 import Asset1
from .struct_reader import BinaryStructReader


class Pack1(Pack):
    """
    A .pack1 asset archive used in Planetside 2 until April 2019
    """
    # name: str
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
                    crc32 = reader.uint32BE()

                    asset = Asset1(name=name, path=self.path, offset=offset, data_length=data_length, crc32=crc32)
                    self.assets[asset.name] = asset

                self.asset_count += asset_count
                reader.seek(next_chunk)
