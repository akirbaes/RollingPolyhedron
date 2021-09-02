import os
import pprint
from copy import deepcopy

from poly_dicts.johnson_nets import johnson_nets
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.prism_nets import prism_nets
all_nets = {**plato_archi_nets, **johnson_nets, **prism_nets}


if __name__ == "__main__":
    print(list(all_nets))
    print(len(all_nets),"polyhedron nets")