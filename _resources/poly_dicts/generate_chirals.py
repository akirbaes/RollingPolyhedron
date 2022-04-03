import os
import pprint
from copy import deepcopy

from johnson_nets import johnson_nets
from plato_archi_nets import plato_archi_nets
from prism_nets import prism_nets
all_nets = {**plato_archi_nets, **johnson_nets, **prism_nets}

def rotatechiral(net):
    newnet = dict()
    for key, value in net.items():
        newnet[key]=list(reversed(value))
    # print(net)
    # print(newnet)
    return newnet

archi_chirals = "snub_cube", "snub_dodecahedron"
johnson_chirals = "j44", "j45", "j46", "j47", "j48"
   
def chiralmake():
    all_symmetries = dict()
    for netname in archi_chirals:
        net: dict = all_nets[netname]
        chiral_net: dict = rotatechiral(net)
        print('plato_archi_nets["%s"]=\\'%(netname+"_c"))
        pprint.pprint(chiral_net,indent=4)
           
    
    for netname in johnson_chirals:
        net: dict = all_nets[netname]
        chiral_net: dict = rotatechiral(net)
        print('johnson_nets["%s"]=\\'%(netname+"_c"))
        pprint.pprint(chiral_net,indent=4)
        

if __name__ == "__main__":
    chiralmake()
    print("All done")