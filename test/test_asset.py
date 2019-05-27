from DbgPack import Pack1
from DbgPack import Asset


def test_asset_equality():
    asset1 = Asset(name="Asset_name.txt", data=b'some_test_data', path="File path")
    asset2 = Asset(name="Asset_name.txt", data=b'some_test_data', path="File path")
    assert asset1 == asset2

def test_pack1_read():
    p1 = Pack1("test/sample.pack")
    raise NotImplementedError

def test_pack2_read():
    raise NotImplementedError

def test_from_bytes():
    raise NotImplementedError
