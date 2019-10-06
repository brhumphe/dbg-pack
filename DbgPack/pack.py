from abc import ABC
from pathlib import Path


class Pack(ABC, dict):
    """
    A collection of assets.
    """

    @classmethod
    # @abstractmethod
    def from_file(cls, path: Path):
        pass

    @classmethod
    # @abstractmethod
    def to_file(cls, path: Path):
        pass


