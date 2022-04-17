import sys
sys.path.append("..")
import os
from math import ceil
import svgwrite
from _libs.FileManagementShortcuts import outputfolder
import pygame

from _libs.GeometryFunctions import centerpoint, distance, psign, ptAdd, ptSub
from _libs.RollyPoint import RollyPoint
from _libs.SupertileCoordinatesGenerator import supertile_center, yield_insides, yield_borders
from _resources.symmetry_classes.poly_symmetries import canon_fo, canon_face


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



def closest_in(point,points,precision=5):
    for pt in points:
        if(distance(point,pt)<precision):
            return pt
    return None
def rounded(point):
    return (int(round(point[0])),int(round(point[1])))

def normalize_point(point,points,precision=5):
    point = rounded(point)
    pt = closest_in(point,points,precision)
    if(pt==None):
        points.add(point)
    else:
        point=pt
    return point
def normalize_points(lines, precision=5):
    points = set()

    result = []
    for index,poly in enumerate(lines):
        rpoly = ()
        for i,point in enumerate(poly):
            point = normalize_point(point,points,precision)
            rpoly+=point,
        result.append(rpoly)
    return result

def scour_svg(filename):
    from scour.scour import start, sanitizeOptions
    scour_options = sanitizeOptions(options=None)  # get a clean scour options object
    scour_options.remove_metadata = True
    scour_options.enable_viewboxing = True

    inputfile = open(filename, 'rb')
    outputfile = open(filename.replace("svg"+os.sep,"svg"+os.sep+"_"), 'wb')
    start(scour_options, inputfile, outputfile)

def generate_image(tiling,polyhedron,tilingname,polyname,classes,group,groups,hexborders,symmetries,explored,type,stable_spots = []):
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
    neighbour_points_set = set()
    for cell, nextcellid, cgon, nextcgon, pa, pb in yield_borders(tiling, startcell, p1, p2, precision=7):
        nextcell, nextid = nextcellid
        neigh = supertile_center(tiling, nextcell, pa, pb, precision=7)
        neighcoord = hexborders[(cell,nextcellid)]
        neighbour_pos[neighcoord]=neigh
        supertile_border_segments.append([(x-cx,y-cy) for (x,y) in nextcgon[0:2]])

    dx = neighbour_pos[(1,0)]
    dx = [dx[0]-cx,dx[1]-cy]
    dy = neighbour_pos[(0,1)]
    dy = [dy[0]-cx,dy[1]-cy]
    symmetrylines = [[None,None],[None,None]]
    s1,s2 = symmetries
    def rebase(vec,x,y):
        return (vec[0]*x[0]+vec[1]*y[0],vec[0]*x[1]+vec[1]*y[1])
    symmetrylines = [ ((0,0),rebase(s1,dx,dy)),((0,0),rebase(s2,dx,dy)) ]

    #Try to optimize one if it can be easily changed by adding/subbing another one
    for i,f in ((ii,ff) for ii in (0,1) for ff in(ptSub,ptAdd)):
            newline = f(symmetrylines[i][1],symmetrylines[not i][1])
            if(distance((0,0),newline)+1<distance(*symmetrylines[i])):
                symmetrylines[i]=((0,0),newline)
            break;
    #Make them start from top
    # for index,(zero, line) in enumerate(symmetrylines):
    #     if line[1]<0:
    #         symmetrylines[index] = (zero,(-line[0],-line[1]))



    print("Fixed symmetry lines:",symmetrylines)
    drawn_tiles = list()
    drawn_supertiles = list()
    filled_tiles = list()
    facefull_tiles = list()
    faceorifull_tiles = list()
    unused_tiles = list()
    compatible_stable_tiles = list()
    used_stable_tiles = list()

    min_x=0
    min_y=0
    max_x=0
    max_y=0
    used_fo = set((f,o) for explored_classes in explored.keys() for classid in explored_classes for (c,f,o) in classes[classid])
    used_faces = set(f for (f,o) in used_fo)
    used_faces_withsides = [[] for x in range(13)]
    for face in used_faces:
        neigh = polyhedron[face]
        used_faces_withsides[len(neigh)].append(face)

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
                symmetrylines = tuple(tuple(ptAdd(point, center) for point in line) for line in symmetrylines)
            #     symmetrylines[0][0] = center
            #     symmetrylines[1][0] = center
            # if c1 == startcell and list(coordinates) == list(symmetries[0]):
            #     symmetrylines[0][1] = center
            # if c1 == startcell and list(coordinates) == list(symmetries[1]):
            #     symmetrylines[1][1] = center

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
            else:
                # canon_reached_fo = set(canon_fo(polyname,f,o) for (f,o) in reached_fo)
                # if all((canon_fo(polyname,f,o) in canon_reached_fo) for f in faces_withsides[len(polygon)] for o in range(len(polygon))):
                #     compatible_stable_tiles.append((polygon))
                # if all((canon_fo(polyname,f,o) in canon_reached_fo) for f in used_faces_withsides[len(polygon)] for o in range(len(polygon))):
                #     used_stable_tiles.append((polygon))
                canon_reached_faces = set(canon_face(polyname,f) for (f,o) in reached_fo)
                if all((canon_face(polyname,f) in canon_reached_faces) for f in faces_withsides[len(polygon)]):
                    compatible_stable_tiles.append((polygon))
                if all((canon_face(polyname,f) in canon_reached_faces) for f in used_faces_withsides[len(polygon)]):
                    used_stable_tiles.append((polygon))

        # if(polyname=="cube"):
        #     input("cube fo |%s|"%str(reached_fo))
        for segment in supertile_border_segments:
            seg = [(x0+x,y0+y) for (x,y) in segment]
            drawn_supertiles.append(seg)

            min_x = min(min_x,min(x for (x,y) in segment))
            min_y = min(min_y,min(y for (x,y) in segment))
            max_x = max(max_x,max(x for (x,y) in segment))
            max_y = max(max_y,max(y for (x,y) in segment))
        for segment in symmetrylines:
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
    # if(width>height):
    #     final_width = 980
    #     ratio = final_width/width
    #     final_height = int((max_y-min_y)*ratio)
    # else:
    #     final_height = 980
    #     ratio = final_height/height
    #     final_width = int((max_x-min_x)*ratio)
    final_width,final_height = width+20,height+20
    ratio = 1
    # ratio = ratio**0.5

    points_set = set()
    def coord_adapt(shape):
        # print(shape)
        # return [((x-min_x)*final_width/width+10, (y-min_y)*final_width/width+10) for (x,y) in shape]
        return [normalize_point(((x-min_x)+10, (y-min_y)+10),points_set,20) for (x,y) in shape]

    drawn_supertiles = [coord_adapt(segment) for segment in drawn_supertiles]
    print("supertiles",drawn_supertiles)
    print("symmetries",symmetrylines)
    symmetrylines = [coord_adapt(line) for line in symmetrylines]
    print("symmetries",symmetrylines)
    drawn_tiles = [coord_adapt(poly) for poly in drawn_tiles]
    filled_tiles = [coord_adapt(poly) for poly in filled_tiles]
    facefull_tiles = [coord_adapt(poly) for poly in facefull_tiles]
    faceorifull_tiles = [coord_adapt(poly) for poly in faceorifull_tiles]
    unused_tiles = [coord_adapt(poly) for poly in unused_tiles]
    compatible_stable_tiles = [coord_adapt(poly) for poly in compatible_stable_tiles]
    used_stable_tiles = [coord_adapt(poly) for poly in used_stable_tiles]

    print("tiles",drawn_tiles)
    if("pygame"):
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
            try:
                polimage=pygame.image.load("polyhedron_images/"+polyname+".jpg")
            except:
                pass

        try:
            width,height = polimage.get_width(),polimage.get_height()
            newwidth=int(width/height*100)
            polimage=pygame.transform.scale(polimage,(newwidth,100))
            totalsurf.blit(polimage,(0,0))
        except:
            width,height = 50,50
            newwidth=int(width/height*100)

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
    if("svg"):
        filename = outputfolder("_results","svg")+polyname+"@"+tilingname+'.svg'
        svg = svgwrite.Drawing(filename, profile='tiny',height=final_width+20, width=final_height+20)
        
        for poly in filled_tiles:
            # print("poly:",poly)
            if(poly in faceorifull_tiles):
                color = "rgb(255,0,0)"
            elif(poly in facefull_tiles):
                color = "rgb(128,0,0)"
            else:
                color = "rgb(128,128,128)"
            svg.add(svg.polygon(poly, fill=color))
        for poly in unused_tiles:
            xx,yy=centerpoint(poly)
            svg.add(svg.line((xx-15,yy-15),(xx+15,yy+15), stroke="black", stroke_width=2))
            svg.add(svg.line((xx+15,yy-15),(xx-15,yy+15), stroke="black", stroke_width=2))
        # for line in drawn_supertiles:
        #     print("supertile line:",line)
        #     svg.add(svg.polyline(line, stroke="green", stroke_width=16))
        drawn_supertiles = list(set(tuple(liste) for liste in drawn_supertiles))
        # print("supertile:", drawn_supertiles)

        color = "rgb(128,0,0)","rgb(0,128,0)","rgb(0,0,128)"
        counter = 0
        for line in drawn_supertiles:
            # print("tile line:",line)
            svg.add(svg.polygon(line, fill="none",stroke="black", stroke_width=8))
            counter=(counter+1)%3
        for poly in drawn_tiles:
            for i in range(len(poly)):
                line = poly[i-1],poly[i]
                line_reverse = poly[i],poly[i-1]
                # print("tile line:",line)
                if line not in drawn_supertiles and line_reverse not in drawn_supertiles:
                    svg.add(svg.polygon(line, fill="none",stroke="black", stroke_width=2))

        # supertile_border_segments = list(set((point for line in drawn_supertiles for point in line)))
        # svg.add(svg.polygon(supertile_border_segments, fill="none",stroke="green", stroke_width=8))
        #TODO: take the center and reorder them to make a polygon

        # supertile = list(drawn_supertiles.pop(0))
        # while(drawn_supertiles):
        #     for index,line in enumerate(drawn_supertiles):
        #         if(distance(line[0], supertile[-1])<5):
        #             print(distance(line[0], supertile[-1]),line[0], supertile[-1])
        #             drawn_supertiles.pop(index)
        #             supertile.append(line[1])

        for poly in compatible_stable_tiles:
            svg.add(svg.circle(center=centerpoint(poly), fill="black", r=16))
        if not all(poly in compatible_stable_tiles for poly in used_stable_tiles):
            input(polyname+" "+tilingname+" has conditional stability on\n    "+str(used_stable_tiles))
        for poly in used_stable_tiles:
            if(poly not in compatible_stable_tiles):
                p,w = ptSub(centerpoint(poly),(16,16)),(32,32)
                svg.add(svg.rect(p,w, fill="black"))
        #scour removes this color: "rgb(0,128,288)"
        try:
            for index,line in enumerate(symmetrylines):
                svg.add(svg.line(*line, stroke="royalblue", stroke_width=int(9)))
                svg.add(svg.circle(center=line[1], fill="royalblue",r=12))

            svg.add(svg.circle(center=symmetrylines[0][0], fill="royalblue", r=12))
        except:
            pass
        svg.save()
        # scour_svg(filename)
        #Scour is less good than SVGO

        