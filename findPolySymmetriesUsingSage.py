from sage.all import *
import os
import pprint
from copy import deepcopy
# sage -python findPolySymmetriesUsingSage.py

from poly_dicts.johnson_nets import johnson_nets
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.prism_nets import prism_nets

MAX_ANTENNAE_AMOUNT = 3
#None for all

def modify_net(net,face,ori):
    n = len(net)
    currentface = n
    sides = len(net[face])
    size=1
    net[currentface]=[face]
    net[face].append(currentface)
    currentface+=1
    size+=1
    # print("Max antennae",maxantennae)
    antennasides = size if MAX_ANTENNAE_AMOUNT==None else (MAX_ANTENNAE_AMOUNT-1)
    # print("sides to mark:",antennasides,"/",sides)

    for i in range(min(sides,antennasides)):
        index = (i+ori)%sides
        f = net[face][index]
        for k in range(size):
            net[f].append(currentface)
            net[currentface]=[f]
            f=currentface
            currentface+=1
        size+=1


def generate_classes(net):
    classes = list()
    for face1 in sorted(net):
        classes.append([])
        for ori1 in range(len(net[face1])):
            classes[-1].append(set())
            classes[-1][-1].add((face1,ori1))
            # classes[(face1,ori1)]=set()
    # for idx, x in numpy.ndenumerate(FFOO):
    #     f1,f2,ori1,ori2 = idx
    #     if(x):
    #         classes[f1,ori1].add((f2,ori2))

    modified = list()
    for face1 in sorted(net):
        modified.append([])
        for ori1 in range(len(net[face1])):
            modified_net = deepcopy(net)
            modify_net(modified_net,face1,ori1)
            # modified[-1].append((modified_net))
            g = Graph(modified_net)
            modified[-1].append(g)
            # p=g.plot()
            # p.show()

    for face1 in sorted(net):
        for ori1 in range(len(net[face1])):
            for face2 in sorted(net):
                for ori2 in range(len(net[face2])):
                    if modified[face1][ori1].is_isomorphic(modified[face2][ori2]):
                        classes[face1][ori1].add((face2, ori2))
    droplevel = list()
    print(classes)
    for clas in classes:
        droplevel.extend(clas)
    classes_unique = set( tuple(sorted(clas)) for clas in droplevel )
    return sorted(classes_unique)




all_nets = {**johnson_nets, **plato_archi_nets, **prism_nets}

def firstdraft():
    all_symmetries = dict()
    for netname in all_nets:#["snub_cube"]:#['hexagonal_prism']:  # all_nets:
        print(netname)
        net: dict = all_nets[netname]

        classes = generate_classes(net)
        clasp = pprint.pformat(classes)
        print(len(classes), "classes")
        print(clasp)
        try:
            os.mkdir("symmetry_classes/SAGE")
        except:
            pass
        f = open("symmetry_classes/SAGE/" + netname + "_" + "SAGE" +"A%s"%MAX_ANTENNAE_AMOUNT+ ".txt", "w")
        f.write(clasp)
        f.close()
        all_symmetries[netname] = classes



    all = pprint.pformat(all_symmetries)
    f = open("symmetry_classes/" + "_" + "SAGE"  +"A%s"%MAX_ANTENNAE_AMOUNT+ ".py", "w")
    f.write(all)
    f.close()

if __name__ == "__main__":
    # for antenna in (0,1,2,None):
    #     print("Antenna mode",antenna)
    #     global MAX_ANTENNAE_AMOUNT
    #     MAX_ANTENNAE_AMOUNT = antenna
        # input()

    firstdraft()
    # print("Done with ",antenna,"antennae modifier")
    print("All done")