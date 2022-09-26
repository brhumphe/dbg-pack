# DbgPack
A python utility library for reading .pack and .pack2 files as used in Planetside 2.

## Pack 1
The original .pack format was used in PS2 until the DX11 update in April 2019.

Usage:

    from glob import glob
    from DbgPack import AssetManager
    
    test_server = r"C:\Users\Public\Daybreak Game Company\Installed Games\PlanetSide 2 Test\Resources\Assets"
    
    print("Loading packs")
    current_manager = AssetManager(glob(test_server + "/*.pack"))
    nc_helmet_male_look011 = current_manager['Helmet_NC_Male_All_Look011_LOD0_LODAuto.dme']
    print(nc_helmet_male_look011)
    
After loading the .pack files, any asset can be loaded with `asset_manager['file_name']`
Read the binary contents of an `Asset` via the `.data` property:

    binary_data = asset.data
    
## Pack 2
Introduced with the DX11 update in April 2019, the pack2 format includes far more robust
support for **detecting** modified game files. The interface is the same, but the names of
the files are no longer included in the .pack2 file, so it is necessary to supply your own
via the `namelist=` parameter.
