import os
import pprint

path = "./"

def convert_tiling(tiling):
    p = len(tiling)
    return {key: [(x % p) for x in value] for key, value in tiling.items()}


category_name = "prism_nets"

all_tilings = dict()
for dirpath, dirnames, filenames in os.walk(path):
    for name in filenames:
        if name.endswith((".py")) and name!="simplify.py" and category_name not in name:
            pathname =os.path.join(dirpath, name)
            print(pathname)
            f=open(pathname)
            exec(f.read())
            f.close()
            
output = "#dict[face]=[neighbour_face ...]\n"
output += category_name + "= dict()\n"
# prisms = dict()
for tilename in all_tilings:
    new_tiling = convert_tiling(all_tilings[tilename])
    dictline = pprint.pformat(new_tiling, indent=4, sort_dicts=True,width=80)
    # prisms[tilename]=new_tiling
    output += "%s['%s'] = \\\n%s\n\n" % (category_name, tilename, dictline)
    
f = open(category_name + ".py", "w")
f.write(output)
f.close()