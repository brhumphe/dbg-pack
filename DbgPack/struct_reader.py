import struct


# TODO: Should this be its own Python package?
class BinaryStructReader:
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
        return struct.unpack_from(fmt, self.file_obj.read(size))
    
    def _read_Struct(self, s: struct.Struct):
        return s.unpack_from(self.file_obj.read(s.size))[0]
    
    def uintLE(self):
        return self._read_Struct(self._uintLE)
    
    def uintBE(self):
        return self._read_Struct(self._uintBE)
    
    def string(self, length, encoding="utf-8"):
        return self.unpack_struct(str(length) + 's')[0].decode(encoding)
    
    def seek(self, offset, whence=0):
        self.file_obj.seek(offset, whence)
    
    def __init__(self, file_name, buffered=0):
        self.path = file_name
        # TODO: Is this the best place to open the file?
        self.file_obj = open(file_name, 'rb', buffering=buffered)
    
    # Context Management functions
    def __enter__(self):
        return self  # .file_obj
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.file_obj.close()
