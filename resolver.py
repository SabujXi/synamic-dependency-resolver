class Mod(object):
    def __init__(s, name, deps=None):
        s.__deps = [] if deps is None else deps
        s.__name = name
    
    @property
    def name(s):
        return s.__name
    
    @property
    def dependencies(s):
        return s.__deps
    

def create_dep_list(mods: dict):
    # sanity check : check that dict key and the mod name referred to by that name is the same. Only the framework programmer can make this mistake!
    for name, mod in mods.items():
        if name != mod.name:
            raise Exception("Fatal error - key name and mod name against that key must be the same!\nThe key name was `%s` and the mod name is `%s`" % (name, mod.name))

    # circulur dependency checker - direct and non-direct    
    for name, mod in mods.items():
        if len(mod.dependencies) == 0:
            continue
        
        _d_list = mod.dependencies.copy() # initializing for first while loop
        _mod = mod
        
        # for detecting dependency chain
        dep_mod_chain = []
        
        while _mod is not None:
            dep_mod_chain.append(_mod)
            
            if name in _mod.dependencies:
                dep_mod_chain.append(mods[_mod.dependencies[_mod.dependencies.index(name)]])
                # chain representation:
                _str = ""
                for __mod in dep_mod_chain:
                    _str += "%s : %s\n" % (__mod.name, __mod.dependencies)
                raise Exception("Case 1: circulur dependency. Dependency chain: \n%s" % _str)
            else:
                
                _d_list.extend(_mod.dependencies)
                
                if _d_list:
                    _mod = mods[_d_list[-1]]
                    del _d_list[-1]
                else:
                    _mod = None
            #print("In the end of first while loop check done")
    #print("Dependency check done")
    my_mods = mods.copy()
    # zero dep modules
    done_mods = {}
    undone_mods = {}
    zero_dep_mods = {}
    dep_list = []
    
    # zero dep mod filtering
    for name, mod in my_mods.items():
        if len(mod.dependencies) == 0:
            zero_dep_mods[name] = mod
            dep_list.append(name)
        else:
            undone_mods[name] = mod
            
    if len(zero_dep_mods) == 0:
        raise Exception("At least one Zero Dependency Modules must be present")
        
    done_mods.update(zero_dep_mods)
    
    # dependency list building

    while len(undone_mods) > 0:
        for name, mod in undone_mods.copy().items():
            all_done = True
            for d_name in mod.dependencies:
                if d_name not in done_mods:
                    all_done = False
                    break
            if all_done:
                del undone_mods[name]
                done_mods[name] = mod
                dep_list.append(name)
    return dep_list

dep_list = create_dep_list({
        "m1": Mod("m1"),
        "m2": Mod("m2", ["m1"]),
        "m3": Mod("m3")
    })

print(dep_list)


dep_list = create_dep_list({
        "m1": Mod("m1"),
        "m2": Mod("m2", ["m1"]),
        "m3": Mod("m3", ["m1", "m2"])
    })

print(dep_list)

""" raised circulur dependency
dep_list = create_dep_list({
        "m1": Mod("m1"),
        "m2": Mod("m2", ["m1", "m2"]),
        "m3": Mod("m3", ["m1", "m2"])
    })

print(dep_list)
"""

dep_list = create_dep_list({
        "m1": Mod("m1"),
        "m2": Mod("m2", ["m6"]),
        "m3": Mod("m3", ["m1", "m2"]),
        "m4": Mod("m4", ["m1", "m3"]),
        "m5": Mod("m5", ["m4"]),
        "m6": Mod("m6", ["m1", "m5"])
    })

print(dep_list)
