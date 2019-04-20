from glob import glob
from DbgPack.asset_manager import AssetManager

test_backup = r"C:\Users\Ben\Desktop\PlanetSide 2 Test Backup March 2019\Resources\Assets"
current_test = r"C:\Users\Public\Daybreak Game Company\Installed Games\PlanetSide 2 Test\Resources\Assets"

# print("Loading packs")
# backup_manager = AssetManager(glob(test_backup + "/*.pack"))
# current_manager = AssetManager(glob(current_test + "/*.pack2"))

# print("Getting names with list comprehension")

# print(current_manager['Helmet_NC_Male_All_Look011_LOD0_LODAuto.dme'])
# print(backup_manager['Helmet_NC_Male_All_Look011_LOD0_LODAuto.dme'].data)
# names = []
# print("Iterating everything")
# for i in backup_manager:
#     names.append(backup_manager[i])
# print(names)
# print("Done")
from DbgPack import Pack2, BinaryStructReader

pack = Pack2('test/sample2.pack2')
print(pack['{NAMELIST}'])
