from dataclasses import dataclass, field


@dataclass
class Asset:
    """Class for managing data of a single asset file.

    If data is not set, it will be read from path at the specified offset"""
    name: str
    path: str = ""
    data: bytes = field(repr=False, default=None)
    offset: int = field(default=0)
    crc32: int = field(default=None)  # TODO: How to handle when this is not passed in?
    isZipped: bool = False

    @classmethod
    def from_bytes(cls, name):
        raise NotImplementedError

