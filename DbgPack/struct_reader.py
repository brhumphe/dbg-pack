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
    _uLL_LE = struct.Struct('<Q')
    
    def unpack_struct(self, fmt):
        size = struct.calcsize(fmt)
        return struct.unpack_from(fmt, self.read(size))
    
    def _read_Struct(self, s: struct.Struct):
        unpacked = s.unpack_from(self.read(s.size))
        if len(unpacked) == 1:
            return unpacked[0]
        else:
            return unpacked
    
    def uintLE(self):
        return self._read_Struct(self._uintLE)
    
    def uintBE(self):
        return self._read_Struct(self._uintBE)
    
    def ulonglongLE(self):
        return self._read_Struct(self._uLL_LE)
    
    def string(self, length, encoding="utf-8"):
        return self.unpack_struct(str(length) + 's')[0].decode(encoding)

    def __init__(self, path: str):
        file_io = open(path, 'rb')
        super().__init__(file_io)

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()