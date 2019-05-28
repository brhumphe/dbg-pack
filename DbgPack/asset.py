from dataclasses import dataclass, field, InitVar
from binascii import crc32


@dataclass
class Asset:
    """Class for managing data of a single asset file.

    If data is not set, it will be read from path at the specified offset"""
    name: str
    asset_type: str = field(default=None, init=False)
    crc32: int = field(default=None)
    _data: bytes = field(init=False, repr=False, default=None, compare=False)
    offset: int = field(default=0)
    length: int = field(default=0)
    # isZipped: bool = False
    path: str = ""

    def __post_init__(self):
        if self.name:
            # This might need to be moved to a property setter on name
            self.asset_type = self.name.split('.')[-1]

    @property
    def data(self):
        if self._data:
            return self._data
    
        with open(self.path, 'rb') as reader:
            reader.seek(self.offset)
            return reader.read(self.length)

    def __len__(self):
        return self.length

    @classmethod
    def from_bytes(cls, name: str, data: bytes):
        instance = cls(name=name)
        instance._data = data
        instance.length = len(data)
        instance.crc32 = crc32(data)
    
        return instance
