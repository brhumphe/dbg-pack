from DbgPack import Pack1
from DbgPack import Asset


def test_asset_equality():
    asset1 = Asset(name='AbilityClasses.txt', offset=8192, length=149, crc32=1748740018, path='sample.pack')
    asset2 = Asset(name='AbilityClasses.txt', offset=8192, length=149, crc32=1748740018, path='sample.pack')
    assert asset1 == asset2

    asset3 = Asset(name="Asset_name.txt", path="File path")
    assert asset1 != asset3


def test_pack1_read():
    sample_data = b'#*ABILITY_CLASS_ID^NAME_ID^DESCRIPTION_ID^ICON_ID^\r\n2^0^0^0^\r\n3^0^0^0^\r\n4^0^0^0^\r\n5^0^0^0^\r\n6^0^0^5714^\r\n7^0^0^5715^\r\n8^0^0^0^\r\n9^0^0^0^\r\n10^0^0^0^\r\n'
    a1 = Asset(name='AbilityClasses.txt', offset=8192, length=149, crc32=1748740018, path='sample.pack')
    # Make sure data read is correctly from a pack1 file
    assert a1.data == sample_data


def test_pack2_read():
    raise NotImplementedError


def test_from_bytes():
    sample_data = b'#*ABILITY_CLASS_ID^NAME_ID^DESCRIPTION_ID^ICON_ID^\r\n2^0^0^0^\r\n3^0^0^0^\r\n4^0^0^0^\r\n5^0^0^0^\r\n6^0^0^5714^\r\n7^0^0^5715^\r\n8^0^0^0^\r\n9^0^0^0^\r\n10^0^0^0^\r\n'
    p1 = Pack1("sample.pack")
    a1 = p1['AbilityClasses.txt']
    a2 = Asset.from_bytes('AbilityClasses.txt', data=sample_data)
    
    assert a2.data == sample_data
    assert a2.crc32 == a1.crc32
    assert a2.asset_type == a1.asset_type
    assert len(a2) == len(a1)
