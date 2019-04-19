from DbgPack.hash import crc64


def test_crc64():
    with open('hashes.txt') as file:
        for line in file:
            hashed, filename = line.split(':')
            assert int(hashed, 16) == crc64(filename)
            