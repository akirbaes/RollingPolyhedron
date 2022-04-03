from _resources.poly_dicts.johnson_nets import johnson_nets
from _resources.poly_dicts.plato_archi_nets import plato_archi_nets
from _resources.poly_dicts.prism_nets import prism_nets
all_nets = {**plato_archi_nets, **johnson_nets, **prism_nets}

import pprint

if __name__ == "__main__":
    print(list(all_nets))
    print(len(all_nets),"polyhedron nets")
    with open("../regular_faced_polyhedron_nets.py", "w") as f:
        f.write("all_nets = \\\n")
        f.write(pprint.pformat(all_nets, indent=1, sort_dicts=False))