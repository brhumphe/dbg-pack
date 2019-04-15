_Based on the work of Rhett, shaql, and others_

# Pack2

Pack2 files are the updated asset packaging format with additional security measures to
protect against modification of files.

# Format
The file uses little-endian format unless stated otherwise.

## Header
Magic: 4 byte character string b'PAK '
Asset count: uint32
Pack length: uint32
Map offset: uint32
unknown: uint32
unknown2: 128 bytes (Probably a checksum)

## Data
Binary data, most of it compressed with zlib. Compressed blocks have the header:
Unknown: 4 bytes `A1B2C3D4`
Uncompressed size: `uint32`



## Map
A listing of all the assets contained in the file.

Asset name hash: crc64 hash (Name is UPPERCASE)
Asset offset: unsigned long
Asset data size: unsigned long
IsZipped: uint32 (1 for compressed, 2 for uncompressed)
crc32: uint32
