from dataclasses import dataclass, field
from typing import Dict, List, Union

from DbgPack import Asset
from .struct_reader import BinaryStructReader
from .abc import AbstractPack
from .hash import crc64


@dataclass()
class Pack2(AbstractPack):
    asset_count: int
    file_size: int
    map_offset: int
    assets: Dict[str, Asset]
    raw_assets: Dict[int, Asset]
    path: str
    _namelist: List[Union[bytes, str]] = field(default_factory=list, init=False, repr=False)

    @property
    def namelist(self):
        if self._namelist is None:
            self._namelist = []
        return self._namelist

    @namelist.setter
    def namelist(self, value: List[Union[bytes, str]]):
        self._namelist = value
        self.assets = {}
        self._update_asset_names(value)

    def __init__(self, path: str, namelist: List[str] = None):
        super().__init__(path)
        self.path = path
        self._namelist = namelist
        with BinaryStructReader(path) as reader:
            magic = reader.read(4)
            assert magic == b'PAK\x01'
            self.asset_count = reader.uint32LE()
            self.file_size = reader.uint64LE()
            self.map_offset = reader.uint64LE()

            reader.seek(self.map_offset)
            self.raw_assets = {}
            for i in range(self.asset_count):
                name_hash = reader.uint64LE()
                offset = reader.uint64LE()
                size = reader.uint64LE()
                zipped_flag = reader.uint32LE()
                crc32 = reader.uint32LE()
                asset = Asset(name_hash=name_hash, crc32=crc32, offset=offset, length=size, path=self.path)
                self.raw_assets.update({int(asset.name_hash): asset})

        self.assets = {}
        self._update_asset_names(namelist)

    def _update_asset_names(self, namelist: List[str] = None):
        """
        Build asset dict from namelist
        :param namelist:
        :return:
        """
        if not namelist and 0x4137cc65bd97fd30 not in self:
            # TODO: If no namelist contained in pack, fallback to list of known filenames.
            for asset in self.raw_assets.values():
                self.assets.update({f'{asset.name_hash:016x}.bin': asset})

            return
    
        if not namelist:
            namelist = self.raw_assets[crc64('{NAMELIST}')].data.strip().split(b'\n')
        for name in namelist:
            name_hash = crc64(name)
            if type(name) == bytes:
                name = name.decode("ascii")
            try:
                asset = self.raw_assets[name_hash]
                asset.name = name
                self.assets.update({name: asset})
            except KeyError:
                # TODO: Log this error instead of just printing to console.
                print("Could not find", name, "in", self.path)
                pass

        # TODO: Identify assets which were not contained in the name list

    def __repr__(self):
        return f"Pack2(\"{self.path}\")"

    def __getitem__(self, item):
        if type(item) == str:
            try:
                return self.assets[item]
            except KeyError:
                return self.raw_assets[crc64(item)]
        elif type(item) == int:
            return self.raw_assets[item]
        else:
            raise KeyError

    def __contains__(self, item):
        try:
            return self[item] is not None
        except KeyError:
            return False

    def __len__(self):
        return self.asset_count
