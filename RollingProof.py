import copy
import os
import pickle
import time
from datetime import datetime
from math import ceil
from statistics import mean

import numpy
import pygame
import sympy

GENERATE_PROOF = True
GENERATE_STAB = True
UPDATE_RESULTS = True
DUPLICATE_IMAGES = False

from GeometryFunctions import centerpoint
from RollyPoint import RollyPoint
from symmetry_classes.poly_symmetries import poly_symmetries
from symmetry_classes.symmetry_functions import canon_fo
from tiling_dicts.archimedean_tilings import archimedean_tilings
from tiling_dicts.platonic_tilings import platonic_tilings
from tiling_dicts.isogonal_tilings import biisogonal_tilings
from tiling_dicts.triisogonal_vertex_homogeneous import triisogonal_vertex_homogeneous
from poly_dicts.prism_nets import prism_nets
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.johnson_nets import johnson_nets
all_tilings = {**platonic_tilings, **archimedean_tilings, **biisogonal_tilings, **triisogonal_vertex_homogeneous}
# all_tilings = {**triisogonal_vertex_homogeneous}
all_nets = {**plato_archi_nets, **johnson_nets, **prism_nets}


import CFOClassGenerator

def generate_stability_image(tilingname,polyname,tiling,polyhedron,hexborders,type,stable_spots):
    p1 = RollyPoint(0, 0)
    EDGESIZE = 100
    p2 = RollyPoint(0 + EDGESIZE, 0)
    startcell = 0
    cx,cy = supertile_center(tiling, startcell, p1, p2, precision=7)

    faces_withsides = [[] for x in range(13)]
    for face,neigh in polyhedron.items():
        faces_withsides[len(neigh)].append(face)

    #1: determine the shape and position of every cell IRT the supertile center
    cells_pos = dict()
    for cell, pa, pb, cgon, ccenter in yield_insides(tiling,startcell,p1,p2,precision=7):
        cells_pos[cell]=[(x-cx,y-cy) for (x,y) in cgon]

    neighbour_pos = dict()
    supertile_border_segments = list()
    # 2: determine the position of neighbouring supertiles in order to create the coords
    # and the borders of the supertile IRT the supertile center
    for cell, nextcellid, cgon, nextcgon, pa, pb in yield_borders(tiling, startcell, p1, p2, precision=7):
        nextcell, nextid = nextcellid
        neigh = supertile_center(tiling, nextcell, pa, pb, precision=3)
        neighcoord = hexborders[(cell,nextcellid)]
        neighbour_pos[neighcoord]=neigh
        supertile_border_segments.append([(x-cx,y-cy) for (x,y) in nextcgon[0:2]])

    dx = neighbour_pos[(1,0)]
    dx = [dx[0]-cx,dx[1]-cy]
    dy = neighbour_pos[(0,1)]
    dy = [dy[0]-cx,dy[1]-cy]

    drawn_tiles = list()
    drawn_supertiles = list()
    filled_tiles = list()
    empty_tiles = list()

    min_x=0
    min_y=0
    max_x=0
    max_y=0

    for coordinates,stability in stable_spots.items():
        hcoordx,hcoordy = coordinates
        x0 = hcoordx*dx[0] + hcoordy*dy[0]
        y0 = hcoordx*dx[1] + hcoordy*dy[1]
        for c1,stable in enumerate(stability):
            polygon = [(x0 + x, y0 + y) for (x, y) in cells_pos[c1]]

            drawn_tiles.append(polygon)
            if(stable):
                filled_tiles.append(polygon)
            if not faces_withsides[len(polygon)]:
                empty_tiles.append(polygon)

            min_x = min(min_x, min(x for (x, y) in polygon))
            min_y = min(min_y, min(y for (x, y) in polygon))
            max_x = max(max_x, max(x for (x, y) in polygon))
            max_y = max(max_y, max(y for (x, y) in polygon))
        for segment in supertile_border_segments:
            seg = [(x0+x,y0+y) for (x,y) in segment]
            drawn_supertiles.append(seg)

    width = max_x-min_x
    height = max_y-min_y
    print("Width=",width)
    if(width>height):
        final_width = 980
        ratio = final_width/width
        final_height = int((max_y-min_y)*ratio)
    else:
        final_height = 980
        ratio = final_height/height
        final_width = int((max_x-min_x)*ratio)
    # ratio = ratio**0.5
    def coord_adapt(shape):
        return [((x-min_x)*final_width/width+10, (y-min_y)*final_width/width+10) for (x,y) in shape]

    drawn_supertiles = [coord_adapt(segment) for segment in drawn_supertiles]
    drawn_tiles = [coord_adapt(poly) for poly in drawn_tiles]
    filled_tiles = [coord_adapt(poly) for poly in filled_tiles]
    empty_tiles = [coord_adapt(poly) for poly in empty_tiles]

    cells_pos = list(cells_pos.values())
    cells_pos = [coord_adapt(poly) for poly in cells_pos]

    ratio=ratio
    pygame.init()
    surf = pygame.Surface((final_width+20, final_height+20))
    surf.fill((255,255,255))
    for poly in cells_pos:
        color = (230,255,255)
        pygame.draw.polygon(surf,color,poly,width=0)
    for poly in filled_tiles:
        color = (96,96,96)
        if(poly in cells_pos):
            color=(90,110,110)
        pygame.draw.polygon(surf,color,poly,width=0)
    for poly in empty_tiles:
        color = (0,0,32)
        if(poly in cells_pos):
            color = (0,32,40)
        pygame.draw.polygon(surf,color,poly,width=0)
    typeset = (type=="quasi-roller" )*2
    for poly in drawn_tiles:
        pygame.draw.lines(surf,(192,192,192),1,poly,width=int(ceil((6+typeset)*ratio)))
    for line in drawn_supertiles:
        pygame.draw.line(surf,(0,0,0),*line,width=int(ceil((8-typeset)*ratio)))
    # for line in supertile_border_segments:
    #     pygame.draw.line(surf,(0,0,0),*line,width=int(8*ratio))
    if(width<height):
        surf=pygame.transform.rotate(surf,90)

    path = "_proofimages/"+type+"_stability/"
    try:os.mkdir("_proofimages/")
    except:pass
    try:os.mkdir(path)
    except:pass
    pygame.image.save(surf,path+polyname+"@"+tilingname+" stability"+".png")


def generate_image(tiling,polyhedron,tilingname,polyname,classes,group,groups,hexborders,symmetries,explored,type):
    p1 = RollyPoint(0, 0)
    EDGESIZE = 100
    p2 = RollyPoint(0 + EDGESIZE, 0)
    startcell = list(classes[group[0]])[0][0]
    cx,cy = supertile_center(tiling, startcell, p1, p2, precision=7)

    faces_withsides = [[] for x in range(13)]
    for face,neigh in polyhedron.items():
        faces_withsides[len(neigh)].append(face)

    #1: determine the shape and position of every cell IRT the supertile center
    cells_pos = dict()
    for cell, pa, pb, cgon, ccenter in yield_insides(tiling,startcell,p1,p2,precision=7):
        cells_pos[cell]=[(x-cx,y-cy) for (x,y) in cgon]

    neighbour_pos = dict()
    supertile_border_segments = list()
    # 2: determine the position of neighbouring supertiles in order to create the coords
    # and the borders of the supertile IRT the supertile center
    for cell, nextcellid, cgon, nextcgon, pa, pb in yield_borders(tiling, startcell, p1, p2, precision=7):
        nextcell, nextid = nextcellid
        neigh = supertile_center(tiling, nextcell, pa, pb, precision=3)
        neighcoord = hexborders[(cell,nextcellid)]
        neighbour_pos[neighcoord]=neigh
        supertile_border_segments.append([(x-cx,y-cy) for (x,y) in nextcgon[0:2]])

    dx = neighbour_pos[(1,0)]
    dx = [dx[0]-cx,dx[1]-cy]
    dy = neighbour_pos[(0,1)]
    dy = [dy[0]-cx,dy[1]-cy]
    symmetrylines = [[None,None],[None,None]]


    drawn_tiles = list()
    drawn_supertiles = list()
    filled_tiles = list()
    facefull_tiles = list()
    faceorifull_tiles = list()
    unused_tiles = list()

    min_x=0
    min_y=0
    max_x=0
    max_y=0

    for coordinates,eclasses in explored.items():
        hcoordx,hcoordy = coordinates
        x0 = cx + hcoordx*dx[0] + hcoordy*dy[0]
        y0 = cy + hcoordx*dx[1] + hcoordy*dy[1]
        #cx, cy unnecessary
        #coloration? count compatible faces in advance and decide from there
        #symmetries: draw a line from the center of a tile to another

        faces = set()
        faceori = set()

        for c1 in tiling:
            reached_faces = set()
            reached_fo = set()

            polygon = [(x0 + x, y0 + y) for (x, y) in cells_pos[c1]]
            center = centerpoint(polygon)
            if c1 == startcell and coordinates == (0, 0):
                symmetrylines[0][0] = center
                symmetrylines[1][0] = center
            if c1 == startcell and list(coordinates) == list(symmetries[0]):
                symmetrylines[0][1] = center
            if c1 == startcell and list(coordinates) == list(symmetries[1]):
                symmetrylines[1][1] = center

            drawn_tiles.append(polygon)

            min_x = min(min_x, min(x for (x, y) in polygon))
            min_y = min(min_y, min(y for (x, y) in polygon))
            max_x = max(max_x, max(x for (x, y) in polygon))
            max_y = max(max_y, max(y for (x, y) in polygon))

            for clas in eclasses:
                for c,f,o in classes[clas]:
                    if c == c1:
                        reached_faces.add(f)
                        reached_fo.add((f,o))
            if(reached_faces):
                filled_tiles.append(polygon)
            if(len(reached_faces)==len(faces_withsides[len(polygon)])):
                facefull_tiles.append(polygon)
            if(len(reached_fo)==len(faces_withsides[len(polygon)]*len(polygon))):
                faceorifull_tiles.append(polygon)
            # print("Faces with",len(polygon),"sides:",faces_withsides[len(polygon)])
            if len(faces_withsides[len(polygon)])==0:
                unused_tiles.append(polygon)
        # if(polyname=="cube"):
        #     input("cube fo |%s|"%str(reached_fo))
        for segment in supertile_border_segments:
            seg = [(x0+x,y0+y) for (x,y) in segment]
            drawn_supertiles.append(seg)

            min_x = min(min_x,min(x for (x,y) in segment))
            min_y = min(min_y,min(y for (x,y) in segment))
            max_x = max(max_x,max(x for (x,y) in segment))
            max_y = max(max_y,max(y for (x,y) in segment))
    # print(supertile_border_segments)
    # print(explored)
    # print(max_x,max_y,min_x,min_y)
    width = max_x-min_x
    height = max_y-min_y
    print("Width=",width)
    if(width>height):
        final_width = 980
        ratio = final_width/width
        final_height = int((max_y-min_y)*ratio)
    else:
        final_height = 980
        ratio = final_height/height
        final_width = int((max_x-min_x)*ratio)
    ratio = ratio**0.5
    def coord_adapt(shape):
        return [((x-min_x)*final_width/width+10, (y-min_y)*final_width/width+10) for (x,y) in shape]

    drawn_supertiles = [coord_adapt(segment) for segment in drawn_supertiles]
    # print("b",symmetrylines)
    symmetrylines = [coord_adapt(line) for line in symmetrylines]
    # print("a",symmetrylines)
    drawn_tiles = [coord_adapt(poly) for poly in drawn_tiles]
    filled_tiles = [coord_adapt(poly) for poly in filled_tiles]
    facefull_tiles = [coord_adapt(poly) for poly in facefull_tiles]
    faceorifull_tiles = [coord_adapt(poly) for poly in faceorifull_tiles]
    unused_tiles = [coord_adapt(poly) for poly in unused_tiles]

    pygame.init()
    surf = pygame.Surface((final_width+20, final_height+20), pygame.SRCALPHA)
    surf.fill((255,255,255))
    for poly in filled_tiles:
        # print("poly:",poly)
        if(poly in faceorifull_tiles):
            color = (255,0,0)
        elif(poly in facefull_tiles):
            color = (128,0,0)
        else:
            color = (128,128,128)
        pygame.draw.polygon(surf,color,poly,width=0)
    for poly in unused_tiles:
        pygame.draw.polygon(surf,(0,0,64),poly,width=0)
    for poly in drawn_tiles:
        pygame.draw.lines(surf,(192,192,192),1,poly,width=int(6*ratio))
    for line in drawn_supertiles:
        pygame.draw.line(surf,(0,0,0),*line,width=int(8*ratio))
    for index,line in enumerate(symmetrylines):
        b=(255,255,0,0)
        pygame.draw.line(surf,(0,128,b[index]),*line,width=int(9*ratio))
        pygame.draw.circle(surf,(0,128,b[index]),line[0],12*ratio*ratio)
        pygame.draw.circle(surf,(0,128,b[index]),line[1],12*ratio*ratio)
    if(width<height):
        surf=pygame.transform.rotate(surf,90)
    totalsurf = pygame.Surface((1000, surf.get_height()+100), pygame.SRCALPHA)
    totalsurf.fill((255,255,255))
    totalsurf.blit(surf,(0,100))
    # surf.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
    try:
        polimage=pygame.image.load("polyhedron_images/"+polyname+".png")
    except:
        polimage=pygame.image.load("polyhedron_images/"+polyname+".jpg")

    width,height = polimage.get_width(),polimage.get_height()
    newwidth=int(width/height*100)
    polimage=pygame.transform.scale(polimage,(newwidth,100))

    totalsurf.blit(polimage,(0,0))
    text = pygame.font.SysFont(None, 70).render(polyname+"    %i/%i"%(groups.index(group)+1,len(groups)), True, (0, 0, 0))
    totalsurf.blit(text, (newwidth+4,2))
    text = pygame.font.SysFont(None, 70).render(tilingname, True, (0, 0, 0))
    totalsurf.blit(text, (newwidth+4,52))
    text = pygame.font.SysFont(None, 20).render("polyhedron render via Wikipedia", True, (128, 128, 128))
    totalsurf.blit(text, (1000-text.get_width()-2,52))

    path = "_proofimages/"+type+"/"
    try:os.mkdir("_proofimages/")
    except:pass
    try:os.mkdir(path)
    except:pass
    pygame.image.save(totalsurf,path+polyname+"@"+tilingname+" %i"%(groups.index(group)+1)+".png")



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

from SupertileCoordinatesGenerator import generate_supertile_coordinate_helpers, supertile_center, yield_insides, \
    yield_borders


def is_roller(tiling,tilingname,net,polyname):

    if not any(len(n) == len(ne) for n in tiling.values() for ne in net.values()):
        return

    borders=generate_supertile_coordinate_helpers(tiling,tilingname)
    #print(borders)
    classes, transformations, groups = CFOClassGenerator.generate_CFO_classes(tiling, net, polyname, tilingname, None)
    # print("Classes:",classes)
    # print("Transformations:",transformations)
    # print("Groups:",groups)
    """Turn class transformation into integers"""
    if transformations!=0:
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

        tiling_sides = set(len(n) for n in tiling.values())
        poly_sides = set(len(n) for n in net.values())
        incompatible = len(tiling_sides-poly_sides)
        all_data = [dict() for x in groups]
        stability = [False]*len(groups)
        """For every group, explore the transformations up to N supertiles away to build symmetry vectors"""
        for groupindex,group in enumerate(groups):
            # print(groupindex,group)
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
            all_data[groupindex]["symmetry_vectors"]=min_symmetries
            if(len(min_symmetries)<=1):
                print("Not enough symmetries to cover the plane")
                if len(min_symmetries)==1:
                    all_data[groupindex]["type"]="band"
                else:
                    all_data[groupindex]["type"]="area"
                continue
            N = max(max(abs(x),abs(y)) for (x,y) in min_symmetries)+1
            coordinates = {(i, j): set() for i in range(-N, N + 1, 1) for j in range(-N, N+1, 1)}
            filled_supertiles = set()
            to_explore = [(startingstate,0,0)]
            explored = set()
            """Using the symmetry vectors, fill a N*2 space"""
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
            """After the exploration, gather results"""
            print()
            is_roller=True

            all_data[groupindex]["exploration"]=coordinates
            for coord,states in coordinates.items():
                if not(CFOClassGenerator.has_all_tiles(states, classes, tiling)):
                    is_roller = False
            if(is_roller):
                print(tilingname,polyname,"%i/%i"%(groupindex+1,len(groups)),"is a roller in -%i:%i"%(N,N))
                stability[groupindex]=True
                type = "roller"
                all_data[groupindex]["type"]= type
            else:
                is_quasi_roller = True
                for coord,states in coordinates.items():
                    if not(CFOClassGenerator.has_all_compatible_tiles(states, classes, tiling,net)):
                        is_quasi_roller = False
                stability[groupindex]=is_quasi_roller
                print(tilingname,polyname,"%i/%i"%(groupindex+1,len(groups)),"is not a roller in -%i:%i"%(N,N))
                if(is_quasi_roller):
                    type="quasi_roller"
                    all_data[groupindex]["type"]= type
                else:
                    type="non-roller"
                    all_data[groupindex]["type"]= "hollow"
                if(N):
                    graph = [[bool((i, j) in filled_supertiles)+bool(coordinates[(i,j)]) for i in range(-N//2, N//2 + 1, 1)] for j in range(-N//2, N//2+1, 1)]
                    CFOClassGenerator.prettyprint_012(graph)
                    #input()
            if(GENERATE_PROOF):
                if not any(stability[:groupindex]) or DUPLICATE_IMAGES:
                    generate_image(tiling, net, tilingname, polyname, classes, group, groups, borders, min_symmetries, coordinates,type)
        """Done with all the groups"""
        is_stable = not False in stability
        results = dict()
        results["all_data"]=all_data
        results["stability"]=is_stable
        if True in stability and not incompatible:
            results["type"]="roller"
        elif True in stability and incompatible:
            results["type"]="quasi_roller"
        elif "hollow" in (result["type"] for result in all_data if "type" in result.keys()):
            results["type"]="hollow"
        elif "band" in (result["type"] for result in all_data if "type" in result.keys()):
            results["type"]="band"
        elif "area" in (result["type"] for result in all_data if "type" in result.keys()):
            results["type"]="area"
        elif len(groups)==0:
            results["type"]="area"
        else:
            results["type"]="unknown"
        #for now, let's ignore hollow plane that are not quasi?
        results["polyhedron"]=polyname
        results["tiling"]=tilingname

        """Stability tiles"""
        #for every tile
        #it every face and orientation on it are in a roller group
        #then it is a stable position
        #so it's more like: for every group:
        #   if it has a tile it's representative of that tile's stability
        #for every tile:
        #   if every representative is roller, then the tile is stable

        #[pos][c] is stable if it is equal to maxfo[c]
        if True in stability:
            min_size_area = \
            min((len(res["exploration"]), index) for index, res in enumerate(all_data) if "exploration" in res.keys())[
                1]
            fill_area = {pos: [0 for cell in tiling] for pos in all_data[min_size_area]["exploration"]}
            maxfo = [sum(len(n) for n in net.values() if len(n) == len(neigh)) for tile, neigh in
                     sorted(tiling.items())]
            cell_stability = [0 for cell in tiling]
            for index,group in enumerate(groups):
                for clas in group:
                    for c,f,o in classes[clas]:
                        cell_stability[c] += stability[index]
            for index, result in enumerate(all_data):
                if "exploration" in result.keys():
                    for pos, group in result["exploration"].items():
                        for clas in group:
                            for c, f, o in classes[clas]:
                                try:
                                    fill_area[pos][c] += stability[index]
                                except KeyError:
                                    pass


            stable_spots = {pos:[counter == maxfo[cell] for cell,counter in enumerate(celldata)] for pos,celldata in fill_area.items()}
            stable_spots = {pos:[cell_stability[cell]==maxfo[cell] and maxfo[cell]!=0 for cell in range(len(tiling))] for pos in fill_area}
            type=("roller","quasi-roller")[bool(incompatible)]
            if(GENERATE_STAB):
                generate_stability_image(tilingname,polyname,tiling,net,borders,type,stable_spots)

            results["stability"]=all(cell_stability[cell]==maxfo[cell] for cell in range(len(tiling)))
        return results
    else:
        if(classes):
            results = {"type":"area"}
            return results

    #else no cmpatibility

start_time = time.time()
def timer():
    global start_time
    old_time = start_time
    start_time=time.time()
    return start_time-old_time
def timerstring():
    s=str(timer())
    if("." in s):
        s=s[:s.index(".")+2]
    return s.ljust(5)+"s "
def timestamp():
    return datetime.now().strftime("%H:%M:%S")

if __name__ == "__main__":
    timer()
    print(timestamp())
    rollers = list()
    quasirollers = list()
    rollersdata = dict()
    all_results = dict()
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
    # for tilingname, polyname in [["3^2x4x3x4;3x4x6x4","j29"]]:
    # for tilingname, polyname in [["4^4","cube"]]:
        tiling = all_tilings[tilingname]
        net = all_nets[polyname]
        print(tilingname,polyname)
        results = is_roller(tiling,tilingname,net,polyname)
        all_results[(tilingname,polyname)]=results
        if(results==None):
            rollersdata[(tilingname,polyname)]=" "
        elif(results["type"]=="roller"):
            if((tilingname,polyname) not in rollers):
                rollers.append((tilingname,polyname))
            if results["stability"]:
                rollersdata[(tilingname,polyname)]="SPR"
            else:
                rollersdata[(tilingname,polyname)]="PR"
        elif(results["type"]=="quasi_roller"):
            quasirollers.append((tilingname,polyname))
            if results["stability"]:
                rollersdata[(tilingname,polyname)]="SQPR"
            else:
                rollersdata[(tilingname,polyname)]="QPR"
        elif(results["type"]=="hollow"):
            rollersdata[(tilingname,polyname)]="HPR"
        elif(results["type"]=="band"):
            rollersdata[(tilingname,polyname)]="br"
        elif(results["type"]=="area"):
            rollersdata[(tilingname,polyname)]="ar"
        else:
            rollersdata[(tilingname,polyname)]="x"
    print()
    if(UPDATE_RESULTS):
        with open('rolling_results.pickle', 'wb') as handle:
            pickle.dump(all_results, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('rollersdata.pickle', 'wb') as handle:
            pickle.dump((rollersdata,tuple(all_tilings.keys()),tuple(all_nets.keys())), handle, protocol=pickle.HIGHEST_PROTOCOL)
    #output_table(all_nets,all_tilings,rollersdata)
    for tilingname,polyname in rollers:
        print(tilingname,polyname)
    print(len(rollers))
    print("Tilings:",len(all_tilings))
    print(timestamp())
    print("Total duration:",timerstring())