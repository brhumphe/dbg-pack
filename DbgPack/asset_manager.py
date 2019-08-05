# from collections import ChainMap
# from dataclasses import dataclass, field
# from pathlib import Path
# from typing import List, ChainMap as ChainMapType
#
# from DbgPack import Pack1, Pack2
# from DbgPack.abc import AbstractPack
#
#
# # TODO: Decide how to handle name collisions in pack files
# # TODO: Write unit tests for AssetManager
# @dataclass()
# class AssetManager:
#     packs: List[AbstractPack] = field(default_factory=list)
#     assets: ChainMapType[str, Asset] = field(default_factory=ChainMap, repr=False, init=False)
#
#     @staticmethod
#     def load_pack(path: str, namelist: List[str] = None):
#         pack_type = Path(path).suffix
#         if pack_type == '.pack':
#             return Pack1(path)
#         elif pack_type == '.pack2':
#             return Pack2(path, namelist=namelist)
#
#     def __init__(self, packs: List[str], namelist: List[str] = None):
#         self.packs = [self.load_pack(path, namelist=namelist) for path in packs]
#         self.assets = ChainMap(*[p.assets for p in self.packs])
#
#     def __getitem__(self, item):
#         return self.assets[item]
#
#     def __contains__(self, item):
#         return item in self.assets
#
#     def __len__(self):
#         return len(self.assets)
#
#     def __iter__(self):
#         return iter(self.assets.values())
