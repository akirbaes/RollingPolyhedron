from statistics import mean

import numpy
import sympy

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

def sqrdist(tupl):
    return tupl[0]*tupl[0]+tupl[1]*tupl[1]

from SupertileCoordinatesGenerator import generate_supertile_coordinate_helpers


if __name__ == "__main__":
    from symmetry_classes.poly_symmetries import poly_symmetries
    import symmetry_classes.symmetry_functions
    def canon_fo(polyname, face, orientation):
        return symmetry_classes.symmetry_functions.canon_fo(polyname, face, orientation, poly_symmetries)

    for tilingname,tiling in all_tilings.items():
        for polyname, net in all_nets.items():
            print(tilingname,polyname)
            borders=generate_supertile_coordinate_helpers(tiling,tilingname)
            #print(borders)
            classes, transformations, groups = CFOClassGenerator.generate_CFO_classes(tiling, net, polyname, tilingname, None)
            #print(classes)
            #print(transformations)
            if(transformations):
                cids = list(range(len(classes)))
                cts = set()
                ctsd = dict()
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
                        ctsd.setdefault(startid,set())
                        ctsd[startid].add((endid,axiscoords))
                print("ctsd",ctsd)

                for groupindex,group in enumerate(groups):
                    startingstate = group[0]

                    if startingstate not in ctsd:
                        continue
                    N=len(group)
                    print(N)

                    symmetries = []


                    to_explore = [(startingstate,0,0,0)]
                    explored = set()
                    while(to_explore):
                        st,x,y,s=to_explore.pop(0)
                        #print(len(explored),N*N*N)
                        #print(N,s,x,y)
                        if(s>N):
                            continue
                        next = ctsd[st]
                        if (st,x,y) not in explored:
                            #if((x,y) not in filled_supertiles and CFOClassGenerator.has_all_tiles(coordinates[(x, y)],classes,tiling)):
                            #    filled_supertiles.add((x,y))
                                #if(len(filled_supertiles)==len(coordinates)):
                                #    break
                            explored.add((st,x,y))
                            for next_st,(dx,dy) in next:
                                if next_st == startingstate and (x+dx,y+dy)!=(0,0):
                                    nx,ny=x+dx,y+dy
                                    if(len(symmetries)<=1 and [nx,ny] not in symmetries):
                                        symmetries += [[nx, ny]]
                                    elif((len(symmetries)<2 or sqrdist((nx,ny))<=max(sqrdist(sym) for sym in symmetries)) and [nx,ny] not in symmetries):
                                        symmetries+=[[nx,ny]]
                                        #print(symmetries)
                                        matrix = numpy.array(symmetries)
                                        #print("Made",symmetries)
                                        # lambdas, V = numpy.linalg.eig(matrix.T)
                                        _, inds = sympy.Matrix(matrix).T.rref()
                                        if(len(inds)<len(symmetries)):
                                            #input(str(symmetries)+" had lin dep")
                                            for size, index in reversed(sorted((sqrdist(sym), id) for id, sym in enumerate(symmetries))):
                                                symtest = symmetries[:index]+symmetries[index+1:]
                                                matrix = numpy.array(symtest)
                                                _, inds = sympy.Matrix(matrix).T.rref()
                                                if len(inds)==len(symtest):
                                                    symmetries=symtest
                                                    break
                                        #print(symmetries)

                                    #symmetries.add((x+dx,y+dy))
                                if (next_st,x+dx,y+dy) not in explored and -N<=x+dx<=N and -N<=y+dy<=N:
                                    to_explore.insert(0,(next_st,x+dx,y+dy,s+1))

                    print(symmetries)
                    symmetries+=[[-x,-y] for (x,y) in symmetries]
                    symmetries+=[[0,0]]
                    print("Sym totla:",symmetries)
                    #
                    # is_roller=True
                    # for coord,states in coordinates.items():
                    #     if not(CFOClassGenerator.has_all_tiles(states, classes, tiling)):
                    #         is_roller = False
                    #
                    # if(is_roller):
                    #     print(tilingname,polyname,"%i/%i"%(groupindex+1,len(groups)),"is a roller in %ix%i"%(N,N))
                    #     continue
                    #
                    # else:
                    #     input("Not a roller")
                    #
                    #     for coord,states in coordinates.items():
                    #         x,y = coord
                    #         for state in states:
                    #             #print("Doing",state,"for",len(symmetries))
                    #             for symmetry in symmetries:
                    #                 dx,dy=symmetry
                    #                 if(-N<=x+dx<=N and -N<=y+dy<=N):
                    #                     coordinates[(x+dx,y+dy)].add(state)
                    N = max(max(x,y) for (x,y) in symmetries)
                    coordinates = {(i, j): set() for i in range(-N, N + 1, 1) for j in range(-N, N+1, 1)}
                    filled_supertiles = set()
                    to_explore = [(startingstate,0,0)]
                    explored = set()
                    while(to_explore):
                        st,x,y=to_explore.pop(0)
                        next = ctsd[st]
                        if st not in coordinates[(x,y)]:
                            #print(st,x,y)
                            coordinates[(x,y)].add(st)
                            if((x,y) not in filled_supertiles and CFOClassGenerator.has_all_tiles(coordinates[(x, y)],classes,tiling)):
                                filled_supertiles.add((x,y))
                                print("\r",len(filled_supertiles),"/",len(coordinates),end="")
                                if(len(filled_supertiles)==len(coordinates)):
                                    break
                            for next_st,(dx,dy) in next:
                                for sx,sy in symmetries:
                                    nx,ny = x+dx+sx, y+dy+sy
                                    if(-N<=nx<=N and -N<=ny<=N and next_st not in coordinates[(nx,ny)]):
                                        to_explore.insert(0,(next_st,nx,ny))
                    print()
                    is_roller=True
                    for coord,states in coordinates.items():
                        if not(CFOClassGenerator.has_all_tiles(states, classes, tiling)):
                            is_roller = False
                    if(is_roller):
                        print(tilingname,polyname,"%i/%i"%(groupindex+1,len(groups)),"is a roller in %ix%i"%(N,N))
                    else:
                        print(tilingname,polyname,"%i/%i"%(groupindex+1,len(groups)),"is not a roller in %ix%i"%(N,N))

                        if(N):
                            graph = [[(i, j) in filled_supertiles for i in range(-N, N + 1, 1)] for j in range(-N, N+1, 1)]
                            CFOClassGenerator.prettierprint_adjacency(graph,False)
                            #input()
                #redo but with symmetries



    print(len(all_tilings))