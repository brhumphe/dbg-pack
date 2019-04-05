from dataclasses import dataclass, field
from typing import Dict

from DbgPack.asset import Asset
from DbgPack.struct_reader import BinaryStructReader


@dataclass()
class Chunk:
    next_chunk_offset: int
    file_count: int
    assets: Dict[str, Asset] = field(default_factory=Dict, repr=False, init=False)
    
    def __init__(self, stream: BinaryStructReader):
        self.next_chunk_offset = stream.uintBE()
        self.file_count = stream.uintBE()
        self.assets = {}
        
        for i in range(self.file_count):
            asset = Asset(stream)
            self.assets.update({asset.name: asset})
