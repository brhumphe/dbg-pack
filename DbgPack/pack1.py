from typing import Dict
from .abc import AbstractPack

from DbgPack.asset import Asset
from DbgPack.struct_reader import BinaryStructReader


class Pack1(AbstractPack):
    """
    A .pack file archive for storing game assets
    """
    path: str
    assets: Dict[str, Asset]

    def __init__(self, path: str):
        super().__init__(path)
        self.assets = {}
        self.path = path
        with BinaryStructReader(path) as reader:
            next_chunk_offset = -1

            while next_chunk_offset != 0:
                # Read a chunk
                next_chunk_offset = reader.uint32BE()
                file_count = reader.uint32BE()

                # Read asset headers from chunk
                for i in range(file_count):
                    name = reader.string(reader.uint32BE())
                    asset_type = name.split('.')[-1]
                    offset = reader.uint32BE()
                    length = reader.uint32BE()
                    crc32 = reader.uint32BE()

                    asset = Asset(name=name, offset=offset, length=length, crc32=crc32, path=self.path)
                    self.assets.update({asset.name: asset})

                reader.seek(next_chunk_offset)

    def __repr__(self):
        return f"Pack1(\"{self.path}\")"

    def __getitem__(self, item):
        return self.assets[item]

    def __len__(self):
        return len(self.assets)
