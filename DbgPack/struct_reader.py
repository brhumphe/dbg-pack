import struct
from io import BufferedReader


class BinaryStructReader(BufferedReader):
    """
    A convenience wrapper for reading binary files.
    """
    path: str
    # Big-endian structs
    _uintBE = struct.Struct('>I')
    
    # Little-endian structs
    _uintLE = struct.Struct('<I')
    
    def unpack_struct(self, fmt):
        size = struct.calcsize(fmt)
        return struct.unpack_from(fmt, self.read(size))
    
    def _read_Struct(self, s: struct.Struct):
        return s.unpack_from(self.read(s.size))[0]
    
    def uintLE(self):
        return self._read_Struct(self._uintLE)
    
    def uintBE(self):
        return self._read_Struct(self._uintBE)
    
    def string(self, length, encoding="utf-8"):
        return self.unpack_struct(str(length) + 's')[0].decode(encoding)

    def __init__(self, file_io):
        super().__init__(file_io)
