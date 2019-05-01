from DbgPack import Pack2

partial_namelist = [b'AbilityClasses.txt', b'AbilityLines.txt', b'AbilityLineMembers.txt', b'AchievementCategories.txt',
                    b'ActorAnimTriggerDefinitions.xml', b'AnimationGroups.xml', b'AnimationTypes.xml',
                    b'AnimationTransitionRules.xml', b'ActorDecalEmitterDefinitions.xml', b'CleanroomAreas.xml',
                    b'AbilitySets.txt', b'AnimValues.xml', b'AdminCommandAliases.xml', b'AnimEnums.xml',
                    b'HossinGroupNexusAreas.xml', b'designerIslandAreas.xml', b'LandOfJayneAreas.xml',
                    b'MickeysAreas.xml']


def test_load_pack2():
    old_pack = Pack2("data_x64_0_with_namelist.pack2")
    assert len(old_pack) == 2478
    assert len(old_pack.assets) == 2478
    
    new_pack = Pack2("data_x64_0_without_namelist.pack2")
    assert len(new_pack) == 2485
    assert len(new_pack.assets) == 0


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
    
    # TODO: Handle passing names that are not contained in the pack
    new_pack.namelist = ['Invalid File Name']
    assert len(new_pack.assets) == 0
    # Need to remove invalid names from namelist?
    # assert len(new_pack.namelist) == 0
