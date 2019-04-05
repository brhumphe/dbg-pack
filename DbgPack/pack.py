from collections import ChainMap
from typing import Dict, List
from typing import ChainMap as ChainMapType
from DbgPack.asset import Asset
from DbgPack.chunk import Chunk
from DbgPack.struct_reader import BinaryStructReader


# TODO: Add ability to write new .pack files
class Pack:
    """
    A .pack file archive for storing game assets
    """
    path: str
    chunks: List[Chunk]
    assets: ChainMapType[str, Asset]
    
    def __init__(self, path: str):
        self.chunks = []
        self.path = path
        with BinaryStructReader(path) as reader:
            offset = -1
            
            while offset != 0:
                chunk = Chunk(reader)
                self.chunks.append(chunk)
                
                offset = chunk.next_chunk_offset
                reader.seek(offset)
        
        self.assets = ChainMap(*[c.assets for c in self.chunks])
    
    def __repr__(self):
        return f"Pack(\"{self.path}\")"
    
    def __getitem__(self, item):
        return self.assets[item]
    
    def __len__(self):
        return len(self.assets)
