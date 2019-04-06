# DbgPack
A python utility library for reading the .pack v1 files used in Planetside 2 prior to the 2019 DX11 update.

Usage:

    from glob import glob
    from DbgPack.asset_manager import AssetManager
    
    test_server = r"C:\Users\Public\Daybreak Game Company\Installed Games\PlanetSide 2 Test\Resources\Assets"
    
    print("Loading packs")
    current_manager = AssetManager(glob(test_server + "/*.pack"))
    nc_helmet_male_look011 = current_manager['Helmet_NC_Male_All_Look011_LOD0_LODAuto.dme']
    print(nc_helmet_look011)
    
After loading the .pack files, any asset can be loaded with `asset_manager['file_name']`
Read the binary contents of an `Asset` via the `.data` property:

    binary_data = asset.data
    
