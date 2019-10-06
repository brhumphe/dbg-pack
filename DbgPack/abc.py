from abc import ABC, abstractmethod
from pathlib import Path


class Asset(ABC):
    """
    An Asset represents binary data and provides a means to retrieve it.
    """
    name: str
    path: Path

    data_length: int
    crc32: int

    @abstractmethod
    def get_data(self, raw=False) -> bytes:
        """
        Returns the binary contents of the asset.
        :param raw: Copies the data directly, without unzipping or other processing.
        :return:
        """
        pass

    def __len__(self):
        """
        The size of the asset as stored on disk. For zipped files this will be the compressed size.
        :return:
        """
        return self.data_length
