from dataclasses import dataclass
from .abc import AbstractAsset
from .struct_reader import BinaryStructReader


@dataclass
class Asset1(AbstractAsset):
    name: str
    asset_type: str
    offset: int
    size: int
    crc32: int
    path: str

    @property
    def data(self):
        """
        Lazily-loaded binary contents of the asset.
        :return:
        """
        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            return reader.read(self.size)
    
    def __len__(self):
        return self.size
