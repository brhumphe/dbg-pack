from DbgPack import Pack2

partial_namelist = [b'AbilityClasses.txt', b'AbilityLines.txt', b'AbilityLineMembers.txt', b'AchievementCategories.txt',
                    b'ActorAnimTriggerDefinitions.xml', b'AnimationGroups.xml', b'AnimationTypes.xml',
                    b'AnimationTransitionRules.xml', b'ActorDecalEmitterDefinitions.xml', b'CleanroomAreas.xml',
                    b'AbilitySets.txt', b'AnimValues.xml', b'AdminCommandAliases.xml', b'AnimEnums.xml',
                    b'HossinGroupNexusAreas.xml', b'designerIslandAreas.xml', b'LandOfJayneAreas.xml',
                    b'MickeysAreas.xml']


def test_load_pack2():
    pack2v1 = Pack2("data_x64_0_with_namelist.pack2")
    assert len(pack2v1) == 2478
    assert len(pack2v1.assets) == 2478
    asset1 = pack2v1['AbilityClasses.txt']
    print(asset1)
    # assert asset1.asset_type == 'txt'
    assert asset1.offset == 512
    # assert len(asset1) == 149
    assert asset1.crc32 == 1187660072
    
    # TODO: Lookup via bytes should also work
    # asset1b = pack2v1[b'AbilityClasses.txt']
    # assert asset1b == asset1
    # assert asset1b.asset_type == 'txt'
    # assert asset1b.offset == 512
    # # assert len(asset1) == 149

    # TODO: Figure out what they changed the crc32 hashes to. They don't match the python crc32
    # assert asset1b.crc32 == 1187660072
    
    pack2v2 = Pack2("data_x64_0_without_namelist.pack2")
    assert len(pack2v2) == 2485
    assert len(pack2v2.assets) == 0
    asset2 = pack2v2['AbilityClasses.txt']
    # assert asset2.asset_type == 'txt'
    # assert asset2.offset == 8192
    # assert len(asset2) == 149
    # assert asset2.crc32 == 1748740018


def test_pack2_namelist():
    # Initialize with a namelist
    new_pack = Pack2("data_x64_0_without_namelist.pack2", namelist=partial_namelist)
    assert new_pack.namelist == partial_namelist
    assert len(new_pack.assets) == len(partial_namelist)
    
    # Assign a namelist after initialization
    new_pack.namelist = []
    assert new_pack.namelist == []
    assert len(new_pack.assets) == 0
    new_pack.namelist = partial_namelist[:5]
    assert len(new_pack.namelist) == 5
    assert len(new_pack.assets) == 5

    # TODO: Handle passing names which are not in the namelist but ARE in the pack file.
    # materials_ps4 = new_pack[b'materials_ps4.xml']
    
    # TODO: Handle passing names that are not contained in the pack
    new_pack.namelist = ['Invalid File Name']
    assert len(new_pack.assets) == 0
    # Need to remove invalid names from namelist?
    # assert len(new_pack.namelist) == 0
