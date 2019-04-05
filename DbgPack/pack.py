from typing import Dict
from DbgPack.struct_reader import BinaryStructReader
from collections import namedtuple

_assetTuple = namedtuple("AssetTuple", ["name", "asset_type", "offset", "length", "crc32", "path"])


class Asset(_assetTuple):
    @property
    def data(self):
        """
        Lazily-loaded binary contents of the asset.
        :return:
        """
        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            return reader.read(self.length)


# TODO: Add ability to write new .pack files
class Pack:
    """
    A .pack file archive for storing game assets
    """
    path: str
    assets: Dict[str, Asset]

    def __init__(self, path: str):
        self.assets = {}
        self.path = path
        with BinaryStructReader(path) as stream:
            next_chunk_offset = -1

            while next_chunk_offset != 0:
                # Read a chunk
                next_chunk_offset = stream.uintBE()
                file_count = stream.uintBE()

                # Read asset headers from chunk
                for i in range(file_count):
                    # This could go in the __init__ of Asset, but I don't think it's worth messing with namedtuple
                    name = stream.string(stream.uintBE())
                    asset_type = name.split('.')[-1]
                    offset = stream.uintBE()
                    length = stream.uintBE()
                    crc32 = stream.uintBE()

                    asset = Asset(name, asset_type, offset, length, crc32, stream.path)
                    self.assets.update({asset.name: asset})

                stream.seek(next_chunk_offset)

    def __repr__(self):
        return f"Pack(\"{self.path}\")"

    def __getitem__(self, item):
        return self.assets[item]

    def __len__(self):
        return len(self.assets)
