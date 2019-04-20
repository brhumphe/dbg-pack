from DbgPack import AssetManager, Pack1


def test_load_pack1():
    pack = Pack1("sample.pack")
    assert len(pack) == 235
    assert pack.path == "sample.pack"


def test_load_asset1():
    pack = Pack1("sample.pack")
    asset1 = pack['AbilityClasses.txt']
    assert asset1.asset_type == 'txt'
    assert asset1.offset == 8192
    assert len(asset1) == 149
    assert asset1.crc32 == 1748740018
    
    asset2 = pack['Contrails_Vortex_Purple.xml']
    assert asset2.asset_type == 'xml'
    assert asset2.offset == 770682
    assert len(asset2) == 2563
    assert asset2.crc32 == 4092021062


def test_asset1_manager():
    manager = AssetManager(["sample.pack"])
    asset1 = manager['AbilityClasses.txt']
    assert asset1.asset_type == 'txt'
    assert asset1.offset == 8192
    assert len(asset1) == 149
    assert asset1.crc32 == 1748740018
    
    asset2 = manager['Contrails_Vortex_Purple.xml']
    assert asset2.asset_type == 'xml'
    assert asset2.offset == 770682
    assert len(asset2) == 2563
    assert asset2.crc32 == 4092021062
