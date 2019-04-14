from collections import namedtuple

from DbgPack.struct_reader import BinaryStructReader

_assetTuple = namedtuple("AssetTuple", ["name", "asset_type", "offset", "length", "crc32", "path"])


class Asset1(_assetTuple):
    @property
    def data(self):
        """
        Lazily-loaded binary contents of the asset.
        :return:
        """
        with BinaryStructReader(self.path) as reader:
            reader.seek(self.offset)
            return reader.read(self.length)
    
    def __len__(self):
        return self.length
