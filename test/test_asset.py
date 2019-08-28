import binascii
from pathlib import Path

from DbgPack import Pack2, Asset1, Asset2
from DbgPack.hash import crc64


# def test_asset_equality():
#     asset1 = Asset1(name='AbilityClasses.txt', offset=8192, size=149, crc32=1748740018, path=Path('sample.pack'))
#     asset2 = Asset2(name='AbilityClasses.txt', offset=8192, size=149, crc32=1748740018, path=Path('sample.pack'))
#     assert asset1 == asset2
#
#     asset3 = Asset1(name="Asset_name.txt", path=Path('File path'))
#     assert asset1 != asset3


def test_pack1_read():
    sample_data = b'#*ABILITY_CLASS_ID^NAME_ID^DESCRIPTION_ID^ICON_ID^\r\n2^0^0^0^\r\n3^0^0^0^\r\n4^0^0^0^\r\n5^0^0^0^\r\n6^0^0^5714^\r\n7^0^0^5715^\r\n8^0^0^0^\r\n9^0^0^0^\r\n10^0^0^0^\r\n'
    a1 = Asset1(name='AbilityClasses.txt', offset=8192, size=149, crc32=1748740018, path=Path('sample.pack'))
    # Make sure data read is correctly from a pack1 file
    assert a1.get_data() == sample_data
    assert a1.crc32 == binascii.crc32(a1.get_data())


def test_pack2_read():
    sample_data = b'#*ABILITY_CLASS_ID^NAME_ID^DESCRIPTION_ID^ICON_ID^\r\n2^0^0^0^\r\n3^0^0^0^\r\n4^0^0^0^\r\n5^0^0^0^\r\n6^0^0^5714^\r\n7^0^0^5715^\r\n8^0^0^0^\r\n9^0^0^0^\r\n10^0^0^0^\r\n'
    p2 = Pack2(Path('data_x64_0_with_namelist.pack2'))
    a1 = p2['AbilityClasses.txt']
    assert a1.get_data() == sample_data

    a2 = Asset2(name_hash=4696632789834285999, offset=512, size=97, crc32=1187660072,
                path=Path('data_x64_0_with_namelist.pack2'), name='AbilityClasses.txt')
    # assert a1 == a2
    assert a2.name_hash == crc64(a2.name)
    # The way the hashes are calculated changed at some point. Need to figure out how.
    # assert a1.crc32 == binascii.crc32(a1.data)


# def test_from_bytes():
#     sample_data = b'#*ABILITY_CLASS_ID^NAME_ID^DESCRIPTION_ID^ICON_ID^\r\n2^0^0^0^\r\n3^0^0^0^\r\n4^0^0^0^\r\n5^0^0^0^\r\n6^0^0^5714^\r\n7^0^0^5715^\r\n8^0^0^0^\r\n9^0^0^0^\r\n10^0^0^0^\r\n'
#     p1 = Pack1("sample.pack")
#     a1 = p1['AbilityClasses.txt']
#     a2 = Asset.from_bytes('AbilityClasses.txt', data=sample_data)
#
#     assert a2.data == sample_data
#     assert a2.crc32 == a1.crc32
#     assert a2.crc32 == binascii.crc32(a2.data)
#     assert len(a2) == len(a1)
