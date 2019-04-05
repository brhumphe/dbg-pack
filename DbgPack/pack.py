from typing import Dict
from DbgPack.asset import Asset
from DbgPack.struct_reader import BinaryStructReader


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

                for i in range(file_count):
                    asset = Asset(stream)
                    self.assets.update({asset.name: asset})

                stream.seek(next_chunk_offset)
    
    def __repr__(self):
        return f"Pack(\"{self.path}\")"
    
    def __getitem__(self, item):
        return self.assets[item]
    
    def __len__(self):
        return len(self.assets)
