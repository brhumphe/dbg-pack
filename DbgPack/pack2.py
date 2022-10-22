from dataclasses import dataclass
from os import makedirs
from pathlib import Path
from typing import Dict, List

from .abc import AbstractPack, AbstractAsset
from .asset2 import Asset2
from .hash import crc64
from .loose_asset import LooseAsset
from .struct_reader import BinaryStructReader
from .struct_writer import BinaryStructWriter

_MAGIC: bytes = b'PAK\x01'
_NAMELIST_HASH: int = crc64(b'{NAMELIST}')
assert _NAMELIST_HASH == 0x4137cc65bd97fd30, 'crc64 is not generated correctly'

_ZIPPED_FLAGS = (0x01, 0x11)
_UNZIPPED_FLAGS = (0x10, 0x00)


@dataclass
class Pack2(AbstractPack):
    name: str
    path: Path

    asset_count: int
    length: int
    map_offset: int

    assets: Dict[str, Asset2]
    raw_assets: Dict[int, Asset2]

    _namelist: List[str]

    @property
    def namelist(self) -> List[str]:
        return self._namelist

    @namelist.setter
    def namelist(self, value: List[str]):
        self._namelist = value
        self.assets = {}
        self._update_assets(self._namelist)

    @staticmethod
    def export(assets: List[AbstractAsset], name: str, outdir: Path, raw: bool):
        """

        :param assets: List of assets to export
        :param name: name of file to export to
        :param outdir: path to save file
        :param raw: should we use raw zipped data
        """

        makedirs(outdir, exist_ok=True)

        with BinaryStructWriter(outdir / name) as writer:
            sizes = []
            for a in assets:
                if isinstance(a, Asset2):
                    if a.is_zipped:
                        if raw:
                            sizes.append(a.data_length)
                        else:
                            sizes.append(a.unzipped_length)

                    else:  # not zipped
                        sizes.append(a.data_length)

                else:  # not Asset2
                    sizes.append(a.data_length)

            total_data_length = sum(sizes)

            writer.write(_MAGIC)
            writer.uint32LE(len(assets))
            writer.uint64LE(0)  # Overwrite this later
            writer.uint64LE(total_data_length + 0x200)
            writer.uint64LE(256)

            # Padding
            while writer.tell() < total_data_length + 0x200:
                writer.write(b'\x00')

            data_offset = 0x200
            for a in sorted(assets, key=lambda x: x.name_hash if isinstance(x, Asset2) else crc64(x.name)):
                if isinstance(a, (Asset2, LooseAsset)):
                    writer.uint64LE(a.name_hash)
                else:
                    writer.uint64LE(crc64(a.name))

                writer.uint64LE(data_offset)
                length = 0
                flag = 0
                if isinstance(a, Asset2):
                    if a.is_zipped:
                        if raw:
                            length = a.data_length
                            flag = _ZIPPED_FLAGS[0]
                        else:
                            length = a.unzipped_length
                            flag = _UNZIPPED_FLAGS[0]

                    else:  # not zipped
                        length = a.data_length
                        flag = _UNZIPPED_FLAGS[0]

                else:  # not Asset2
                    length = a.data_length
                    flag = _UNZIPPED_FLAGS[0]

                writer.uint64LE(length)
                writer.uint32LE(flag)

                writer.uint32LE(a.data_hash)  # PTS doesn't care if the checksums don't match

                # Write data
                writer.write_to(a.get_data(raw), data_offset)
                data_offset += length

            pack_length = writer.tell()
            writer.seek(0x8, 0)
            writer.uint64LE(pack_length)

    def __init__(self, path: Path, namelist: List[str] = None):
        super().__init__(path)
        self._namelist = namelist

        with BinaryStructReader(self.path) as reader:
            assert reader.read(len(_MAGIC)) == _MAGIC, 'invalid pack2 magic'
            self.asset_count = reader.uint32LE()
            self.length = reader.uint64LE()
            self.map_offset = reader.uint64LE()

            reader.seek(self.map_offset)
            self.raw_assets = {}
            for i in range(self.asset_count):
                name_hash = reader.uint64LE()

                offset = reader.uint64LE()
                data_length = reader.uint64LE()  # length of stored data
                zipped_flag = reader.uint32LE()
                data_hash = reader.uint32LE()

                if zipped_flag in _ZIPPED_FLAGS and data_length > 0:
                    pos = reader.tell()
                    reader.seek(offset)
                    assert reader.read(len(Asset2.ZIP_MAGIC)) == Asset2.ZIP_MAGIC, 'zip flag mismatch with data header'
                    is_zipped = True
                    unzipped_length = reader.uint32BE()
                    reader.seek(pos)
                else:
                    unzipped_length = 0  # This is only used if the asset is zipped
                    is_zipped = False

                asset = Asset2(name_hash=name_hash, data_hash=data_hash, offset=offset, is_zipped=is_zipped,
                               data_length=data_length, unzipped_length=unzipped_length, path=self.path)
                self.raw_assets[asset.name_hash] = asset

        self.assets = {}
        self._update_assets(self._namelist)

    def _update_assets(self, namelist: List[str] = None):
        name_dict: Dict[int, str] = {}
        used_hashes = []

        # Check for internal namelist
        if _NAMELIST_HASH in self:
            names = self.raw_assets[_NAMELIST_HASH].get_data().strip().split(b'\n')
            for n in names:
                hash_ = crc64(n)
                name_dict[hash_] = n.decode('utf-8')

        # Check for external namelist
        if namelist:
            for n in namelist:
                hash_ = crc64(n)
                name_dict[hash_] = n

        # Apply names to assets
        for name_hash, name in name_dict.items():
            if name_hash in self.raw_assets:
                asset = self.raw_assets[name_hash]
                asset.name = name
                self.assets[asset.name] = asset

                used_hashes.append(name_hash)

        # Remaining assets will use their hashes aas keys
        unk_assets = self.asset_count - len(self.assets)
        if unk_assets:
            for hash_ in self.raw_assets.keys() - set(used_hashes):
                asset = self.raw_assets[hash_]
                self.assets[str(hash_)] = asset

    def __repr__(self):
        return super().__repr__()

    def __len__(self):
        return super().__len__()

    def __iter__(self):
        return super().__iter__()

    def __getitem__(self, item):
        if isinstance(item, str):
            try:
                return self.assets[item]
            except KeyError:
                return self.raw_assets[crc64(item)]

        elif isinstance(item, int):
            return self.raw_assets[item]
        else:
            raise KeyError

    def __contains__(self, item):
        return super().__contains__(item)
