from typing import Dict

from DbgPack.asset import Asset
from DbgPack.struct_reader import BinaryStructReader


class Pack:
    """
    A .pack file archive for storing game assets
    """
    path: str
    assets: Dict[str, Asset]

    def __init__(self, path: str):
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
                    # This could go in the __init__ of Asset, but I don't think it's worth messing with namedtuple
                    name = reader.string(reader.uintBE())
                    asset_type = name.split('.')[-1]
                    offset = reader.uintBE()
                    length = reader.uintBE()
                    crc32 = reader.uintBE()

                    asset = Asset(name, asset_type, offset, length, crc32, self.path)
                    self.assets.update({asset.name: asset})

                reader.seek(next_chunk_offset)

    def __repr__(self):
        return f"Pack(\"{self.path}\")"

    def __getitem__(self, item):
        return self.assets[item]

    def __len__(self):
        return len(self.assets)
