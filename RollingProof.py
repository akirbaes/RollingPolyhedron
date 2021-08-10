from statistics import mean

from symmetry_classes.poly_symmetries import poly_symmetries
from symmetry_classes.symmetry_functions import canon_fo
from tiling_dicts.archimedean_tilings import archimedean_tilings
from tiling_dicts.platonic_tilings import platonic_tilings
from tiling_dicts.isogonal_tilings import biisogonal_tilings
from poly_dicts.prism_nets import prism_nets
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.johnson_nets import johnson_nets
all_tilings = {**platonic_tilings, **archimedean_tilings, **biisogonal_tilings}
all_nets = {**plato_archi_nets, **johnson_nets, **prism_nets}


import CFOClassGenerator
def determine_n(tiling,net,polyname):#,startcase,startface,startorientation):
    # classes = CFOClassGenerator.explore_inside(tiling,net,polyname,canon_fo)
    # borders = CFOClassGenerator.explore_borders(tiling,net)
    N = sum(len(net[face])==len(tiling[cell]) and (face,o)==canon_fo(polyname,face,o)
            for face in net for cell in tiling for o in range(len(net[face])))
    classes = CFOClassGenerator.explore_inside(tiling,net,polyname,canon_fo)
    N2 = len(classes)
    # print(classes)
    # print("N=",N)
    size = max(len(elem) for elem in poly_symmetries[polyname])
    # if(size==1):
    #     input("Biggest symmetry class for %s:\n:::%i"%(polyname,size))
    # else:
    print("Biggest symmetry class for %s:\n:::%i"%(polyname,size))
    if(N2>N):
        print("[Error]Amount of classes bigger than amount of positions, N=%i<%i"%(N2,N))
    elif(N2<N):
        print("[Optimisation]Amount of classes smaller than amount of positions, N=%i<%i"%(N2,N))
    else:
    #     print("Amount of states smaller than amount of classes,
        print("[No optimisation]N=%i==%i"%(N,N2))
    return min(N+1,N2+1)

from SupertileCoordinatesGenerator import generate_supertile_coordinate_helpers

if __name__ == "__main__":
    for tilingname,tiling in all_tilings.items():
        for polyname, net in all_nets.items():
            borders=generate_supertile_coordinate_helpers(tiling,tilingname)
            print(borders)
            classes, transformations, groups = CFOClassGenerator.generate_CFO_classes(tiling, net, polyname, tilingname, None)
            print(classes)
            print(transformations)
            if(transformations):
                cids = list(range(len(classes)))
                cts = set()
                for cfo,rotations in transformations.items():
                    for rotation,endcfo in rotations.items():
                        if rotation not in borders:
                            print(rotation,"does not have coordinates infos!")
                            raise PermissionError
                        axiscoords = borders[rotation]
                        startid = CFOClassGenerator.cfo_class_index(classes, cfo)
                        endid = CFOClassGenerator.cfo_class_index(classes, endcfo)
                        # if(startid==endid):
                        #     print(startid,endid)
                        #     print("So those are in")
                        #     exit()
                        cts.add((startid,endid,axiscoords))
            print(cts)
            #exit()
    print(len(all_tilings))