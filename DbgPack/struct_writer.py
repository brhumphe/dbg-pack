import struct
from io import BufferedWriter
from pathlib import Path


class BinaryStructWriter(BufferedWriter):
    path: Path

    # Big-endian structs:
    _uint32BE = struct.Struct('>I')
    _uint64BE = struct.Struct('>Q')

    # Little-endian structs
    _uint32LE = struct.Struct('<I')
    _uint64LE = struct.Struct('<Q')

    def _write_struct(self, s: struct.Struct, value):
        self.write(s.pack(value))

    def uint32LE(self, value):
        return self._write_struct(self._uint32LE, value)

    def uint32BE(self, value):
        return self._write_struct(self._uint32BE, value)

    def uint64LE(self, value):
        return self._write_struct(self._uint64LE, value)

    def uint64BE(self, value):
        return self._write_struct(self._uint64BE, value)

    def string(self, value: str, encoding='utf-8'):
        self.write(value.encode(encoding))

    def write_to(self, data: bytes, offset: int):
        pos = self.tell()
        self.seek(offset, 0)
        self.write(data)
        self.seek(pos, 0)

    def __init__(self, path: Path):
        file_io = path.open('wb')
        super().__init__(file_io)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
