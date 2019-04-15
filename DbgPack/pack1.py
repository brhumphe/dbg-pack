from typing import Dict
from .abc import AbstractPack

from DbgPack.asset1 import Asset1
from DbgPack.struct_reader import BinaryStructReader


class Pack1(AbstractPack):
    """
    A .pack file archive for storing game assets
    """
    path: str
    assets: Dict[str, Asset1]

    def __init__(self, path: str):
        super().__init__(path)
        self.assets = {}
        self.path = path
        with BinaryStructReader(path) as reader:
            next_chunk_offset = -1

            while next_chunk_offset != 0:
                # Read a chunk
                next_chunk_offset = reader.uintBE()
                file_count = reader.uintBE()

                # Read asset headers from chunk
                for i in range(file_count):
                    name = reader.string(reader.uintBE())
                    asset_type = name.split('.')[-1]
                    offset = reader.uintBE()
                    length = reader.uintBE()
                    crc32 = reader.uintBE()

                    asset = Asset1(name, asset_type, offset, length, crc32, self.path)
                    self.assets.update({asset.name: asset})

                reader.seek(next_chunk_offset)

    def __repr__(self):
        return f"Pack(\"{self.path}\")"

    def __getitem__(self, item):
        return self.assets[item]

    def __len__(self):
        return len(self.assets)
