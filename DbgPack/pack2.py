from dataclasses import dataclass, field
from typing import Dict, List, Union

from DbgPack import Asset

from .abc import AbstractPack
from .hash import crc64
from .struct_reader import BinaryStructReader


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
        # TODO: All the commented out print statements are pretty annoying. Switch to a better way to log them

        # TODO: Decide whether to store the hashes alongside the names in the master list
        # TODO: Store the correct capitalization in the master namelist.
        # TODO: Move these to the namelist project
        name_dict = {}
        used_hashes = []

        # XXX: print(f'Pack contains {self.asset_count} assets.')

        # Check for internal namelist
        if crc64('{NAMELIST}') in self:
            # XXX: print('Using internal namelist')

            names = self.raw_assets[crc64('{NAMELIST}')].data.strip().split(b'\n')
            for n in names:
                hash_ = crc64(n)
                name_dict[hash_] = n.decode('utf-8')

        # Check for external namelist
        if namelist:
            # XXX: print('Using external namelist')
            for name in namelist:
                hash_ = crc64(name)
                name_dict[hash_] = name

        # Apply names to assets
        for name_hash, name in name_dict.items():
            try:
                asset = self.raw_assets[name_hash]
                asset.name = name
                self.assets.update({name: asset})

                used_hashes.append(name_hash)

            except KeyError:
                # This error is spammed when using the master namelist
                # XXX: print("Could not find", name, "in", self.path)
                pass

        # Remaining assets will use their hash as the key instead of a name
        remaining_assets = self.asset_count - len(self.assets)
        if remaining_assets:
            # XXX: print(f'{remaining_assets} missing names')
            for hash_ in self.raw_assets.keys() - set(used_hashes):
                asset = self.raw_assets[hash_]
                self.assets[str(hash_)] = asset

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
