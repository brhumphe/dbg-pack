from dataclasses import dataclass, field

from .struct_reader import BinaryStructReader


@dataclass(init=False, repr=True, eq=True, )
class Asset:
    """
    A file archived inside a .pack file on disk.
    """
    name: str
    asset_type: str
    offset: int
    length: int
    crc32: int
    path: str
    
    _data: bytes = field(default=None, compare=False, repr=False)
    
    def __init__(self, stream: BinaryStructReader):
        self.name = stream.string(stream.uintBE())
        self.asset_type = self.name.split('.')[-1]
        self.offset = stream.uintBE()
        self.length = stream.uintBE()
        self.crc32 = stream.uintBE()
        self.path = stream.path
    
    @property
    def data(self):
        if not self._data:
            with open(self.path, mode='rb') as file:
                file.seek(self.offset, 0)
                self._data = file.read(self.length)
        
        return self._data
