import copy
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


def is_roller(tiling,tilingname,net,polyname):
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
            #print(group)
            startingstate = group[0]

            if startingstate not in ctsd:
                continue
            N=len(group)
            print("Group %i/%i"%(groupindex,len(groups)),"N=",N)

            symmetries = []
            min_symmetries = []

            to_explore = [(startingstate,0,0,0)]
            explored = set()
            while(to_explore):
                st,x,y,s=to_explore.pop(0)
                #print(len(explored),N*N*N)
                #print(N,s,x,y)
                if(s>N+1):
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
                            if([nx,ny] not in symmetries):
                                symmetries += [[nx, ny]]

                            if(len(min_symmetries)<1 and [nx,ny] not in min_symmetries):
                                min_symmetries += [[nx, ny]]
                            elif((len(min_symmetries)>0 or sqrdist((nx,ny))<=max(sqrdist(sym) for sym in min_symmetries)) and [nx,ny] not in min_symmetries):
                                min_symmetries+=[[nx,ny]]
                                #print(symmetries)

                                matrix = numpy.array(min_symmetries)
                                #print("Made",symmetries)
                                # lambdas, V = numpy.linalg.eig(matrix.T)
                                _, inds = sympy.Matrix(matrix).T.rref()
                                while((len(inds)<len(min_symmetries))):
                                    #print("Syms",symmetries)
                                    #input(str(symmetries)+" had lin dep")
                                    for size, index in reversed(sorted((sqrdist(sym), id) for id, sym in enumerate(min_symmetries))):
                                        symtest = min_symmetries[:index]+min_symmetries[index+1:]
                                        #print("Symtest",symtest)
                                        matrix = numpy.array(symtest)
                                        _, inds = sympy.Matrix(matrix).T.rref()
                                        if len(inds)==len(symtest):
                                            min_symmetries=symtest
                                            #print(symmetries)
                                            break
                                    matrix = numpy.array(min_symmetries)
                                    _, inds = sympy.Matrix(matrix).T.rref()
                                #print(symmetries)

                            #symmetries.add((x+dx,y+dy))
                        if (next_st,x+dx,y+dy) not in explored and -N<=x+dx<=N and -N<=y+dy<=N:
                            to_explore.insert(0,(next_st,x+dx,y+dy,s+1))

                    if([-1,0]in min_symmetries or [1,0] in min_symmetries)and([0,1] in min_symmetries or [0,-1] in min_symmetries):
                        print("Break early found minimal symmetry")
                        to_explore = []
                        break
            # print("Symmetries:",symmetries)
            print("Min Symmetries:",min_symmetries)

            if(len(min_symmetries)<=1):
                print("Not enough symmetries to cover the plane")
                continue
            #symmetries+=[[sum(x for x,y in symmetries),sum(y for x,y in symmetries)]]
            # min_symmetries+=[[-x,-y] for (x,y) in symmetries]
            #symmetries+=[[2*x,2*y] for (x,y) in symmetries]
            #min_symmetries+=[[0,0]]
            # print("All Symmetries:",symmetries)
            #print("Sym total:",symmetries)
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
            N = max(max(abs(x),abs(y)) for (x,y) in min_symmetries)+1
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
                        # print(to_explore)
                        # if(len(filled_supertiles)==len(coordinates)):
                        #     break
                    for next_st,(dx,dy) in list(next)+[(st,(0,0))]:
                        (x1,y1),(x2,y2)= min_symmetries
                        # nx = x+dx
                        # ny = y+dy
                        # if ((nx,ny) in coordinates and next_st not in coordinates[(nx, ny)]
                        #         and (next_st, nx, ny) not in to_explore):
                        #     to_explore.insert(0,(next_st,nx,ny))
                        for s1,s2 in ((1,1),(1,-1),(-1,1),(-1,-1)):
                            # print("S:",s1,s2)
                            nx = x + dx
                            ny = y + dy
                            while ((nx,ny) in coordinates):
                                nxold = nx
                                nyold = ny
                                while ((nx,ny) in coordinates):
                                    if (next_st not in coordinates[(nx, ny)]
                                            and (next_st, nx, ny) not in to_explore):
                                        to_explore.insert(0,(next_st,nx,ny))
                                    nx+=x2*s2
                                    ny+=y2*s2
                                    # print(nx,ny)
                                # print("Quit:",nx,ny)
                                nx = nxold + x1*s1
                                ny = nyold + y1*s1
                            # print("Quit:",nx,ny)

                        # input()

                        # for
                        #     for sx2,sy2 in symmetries:
                            # nx = x+dx
                            # ny = y + dy
                            # while(-N<=nx<=N and -N<=ny<=N):
                            #         if (next_st not in coordinates[(nx, ny)] and (
                            #         next_st, nx, ny) not in to_explore):
                            #             to_explore.insert(0,(next_st,nx,ny))
                            #         ny+=sy
                            #         if(sy==0):
                            #             break
                            #     nx+=sx
                            #     if(sx==0):
                            #         break

                        # for sx, sy in symmetries:
                        #     nx,ny = x+dx+sx, y+dy+sy
                        #     if(-N<=nx<=N and -N<=ny<=N and next_st not in coordinates[(nx,ny)] and (next_st,nx,ny) not in to_explore):
                        #         to_explore.insert(0,(next_st,nx,ny))
                                #print(next_st,nx,ny)
            print()
            is_roller=True
            for coord,states in coordinates.items():
                if not(CFOClassGenerator.has_all_tiles(states, classes, tiling)):
                    is_roller = False
            if(is_roller):
                print(tilingname,polyname,"%i/%i"%(groupindex+1,len(groups)),"is a roller in -%i:%i"%(N,N))
                return True
            else:
                print(tilingname,polyname,"%i/%i"%(groupindex+1,len(groups)),"is not a roller in -%i:%i"%(N,N))

                if(N):
                    graph = [[bool((i, j) in filled_supertiles)+bool(coordinates[(i,j)]) for i in range(-N, N + 1, 1)] for j in range(-N, N+1, 1)]
                    CFOClassGenerator.prettyprint_012(graph)
                    #input()
        #redo but with symmetries
        return False


if __name__ == "__main__":
    rollers = list()
    from symmetry_classes.poly_symmetries import poly_symmetries
    import symmetry_classes.symmetry_functions
    def canon_fo(polyname, face, orientation):
        return symmetry_classes.symmetry_functions.canon_fo(polyname, face, orientation, poly_symmetries)

    # for tilingname, polyname in [["3^6","j8"]]:
#     for tilingname, polyname in [
# ["3^6;3^2x4x3x4", "cuboctahedron"],
# ["3^6;3^2x6^2", "truncated_tetrahedron"],
# ["(3^3x4^2;3^2x4x3x4)1", "cuboctahedron"],
# ["(3^3x4^2;3^2x4x3x4)1", "j1"],
# ["(3^3x4^2;3^2x4x3x4)1", "j27"]
#         ]:
    for tilingname, polyname in ((t,p) for t in all_tilings.keys() for p in all_nets.keys()):
    # for tilingname, polyname in [["3^6;3^2x4x3x4","j89"]]:
        tiling = all_tilings[tilingname]
        net = all_nets[polyname]
        print(tilingname,polyname)
        if(is_roller(tiling,tilingname,net,polyname)):
            if((tilingname,polyname) not in rollers):
                rollers.append((tilingname,polyname))
    print()
    for tilingname,polyname in rollers:
        print(tilingname,polyname)
    print(len(rollers))