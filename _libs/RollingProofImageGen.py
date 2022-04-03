import os
from math import ceil

import pygame

from _libs.GeometryFunctions import centerpoint
from _libs.RollyPoint import RollyPoint
from _libs.SupertileCoordinatesGenerator import supertile_center, yield_insides, yield_borders


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
    print("Symmetries:",symmetries)
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
        print(shape)
        return [((x-min_x)*final_width/width+10, (y-min_y)*final_width/width+10) for (x,y) in shape]

    drawn_supertiles = [coord_adapt(segment) for segment in drawn_supertiles]
    # print("b",symmetrylines)
    try:
        symmetrylines = [coord_adapt(line) for line in symmetrylines]
    except:
        pass
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
        pygame.draw.polygon(surf,(16,16,48),poly,width=0)
    for poly in drawn_tiles:
        pygame.draw.lines(surf,(192,192,192),1,poly,width=int(6*ratio))
    for line in drawn_supertiles:
        pygame.draw.line(surf,(0,0,0),*line,width=int(8*ratio))
    try:
        for index,line in enumerate(symmetrylines):
            b=(255,255,0,0)
            pygame.draw.line(surf,(0,128,b[index]),*line,width=int(9*ratio))
            pygame.draw.circle(surf,(0,128,b[index]),line[0],12*ratio*ratio)
            pygame.draw.circle(surf,(0,128,b[index]),line[1],12*ratio*ratio)
    except:
        pass
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
    # text = pygame.font.SysFont(None, 70).render(polyname+"    %i/%i"%(groups.index(group)+1,len(groups)), True, (0, 0, 0))
    text = pygame.font.SysFont(None, 70).render(polyname+"    %s, %s"%(str(symmetries[0]),str(symmetries[1])), True, (0, 0, 0))
    totalsurf.blit(text, (newwidth+4,2))
    text = pygame.font.SysFont(None, 70).render(tilingname, True, (0, 0, 0))
    totalsurf.blit(text, (newwidth+4,52))
    # text = pygame.font.SysFont(None, 70).render(str(symmetries), True, (0, 0, 0))
    # totalsurf.blit(text, (newwidth+4,102))


    text = pygame.font.SysFont(None, 20).render("polyhedron render via Wikipedia", True, (128, 128, 128))
    totalsurf.blit(text, (1000-text.get_width()-2,52))

    path = "_proofimages/"+type+"/"
    try:os.mkdir("_proofimages/")
    except:pass
    try:os.mkdir(path)
    except:pass
    # pygame.image.save(totalsurf,path+polyname+"@"+tilingname+" %i"%(groups.index(group)+1)+".png")
    pygame.image.save(totalsurf,path+polyname+"@"+tilingname+".png")