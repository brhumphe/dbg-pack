from pathlib import Path

from DbgPack import Pack1, AssetManager


def test_load_pack1():
    pack = Pack1(Path('sample.pack'))
    assert len(pack) == 235
    assert pack.path == Path('sample.pack')


def test_load_asset1():
    pack = Pack1(Path('sample.pack'))
    asset1 = pack['AbilityClasses.txt']
    assert asset1.offset == 8192
    assert len(asset1) == 149
    assert asset1.data_hash == 1748740018

    asset2 = pack['Contrails_Vortex_Purple.xml']
    assert asset2.offset == 770682
    assert len(asset2) == 2563
    assert asset2.data_hash == 4092021062


def test_asset1_manager():
    manager = AssetManager([Path('sample.pack')])
    asset1 = manager['AbilityClasses.txt']
    assert asset1.offset == 8192
    assert len(asset1) == 149
    assert asset1.data_hash == 1748740018

    asset2 = manager['Contrails_Vortex_Purple.xml']
    assert asset2.offset == 770682
    assert len(asset2) == 2563
    assert asset2.data_hash == 4092021062
