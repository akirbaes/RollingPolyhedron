import pygame
from _libs.GeometryFunctions import xgon, centerpoint, floatcenterpoint
from _libs.RollyPoint import RollyPoint
from _resources.symmetry_classes.poly_symmetries import canon_fo
from _resources.symmetry_classes.tiling_symmetries import canon_co

ROLLING_NETS = True




def convertToTuples(points):
    return  tuple((int(x), int(y)) for x,y in points)
def convertToTuple(point):
    x,y = point
    return  (int(x), int(y))
pygame.init()

def draw_text(surf, text, x, y, color, size,underline=False):
    font = pygame.font.SysFont(None, int(round(size)))
    if(underline):
        font.set_underline(True)
    text = font.render(text, True, color)
    surf.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))


def rounded_center(coordslist,precision=5):
    ccenter = tuple(floatcenterpoint(coordslist))
    ccenter = int(round(ccenter[0] / precision) * precision), int(round(ccenter[1] / precision) * precision)
    return ccenter

def draw_tiling(spa,spb,surface,startcell,startorientation,tiling:dict,iterlevel=0,itercolors=[(0,0,0)],visitedcoords=[]):
    draw_numbers = False
    draw_cursor = False
    if(iterlevel<0):
        return visitedcoords
    # print(visitedcoords)
    tempsurf = pygame.Surface((surface.get_width(),surface.get_height()), pygame.SRCALPHA)
    tempsurf2 = pygame.Surface((surface.get_width(),surface.get_height()), pygame.SRCALPHA)
    # print(itercolors)
    visitedcoords = visitedcoords[:] #copy
    try:
        color = itercolors[0]
        itercolors=itercolors[1:]
    except: color=(128,128,128)
    outsidecells = list()
    insidecells = [(spa,spb,startcell,startorientation)]
    visitedfaces = set()
    i = 0
    while(insidecells):
        # print("inside",iterlevel,insidecells)
        p1,p2,cell,orientation = insidecells.pop(0)
        cell_poly = xgon(len(tiling[cell]),p1,p2)
        ccenter = rounded_center(cell_poly,5)
        if(ccenter in visitedcoords):
            # print("Found it!")
            continue
        else:
            pass
            # print(ccenter,"not in",visitedcoords)
        if(cell in visitedfaces):
            continue
        visitedcoords.append(ccenter)
        visitedfaces.add(cell)
        cell_poly = cell_poly[orientation:]+cell_poly[:orientation]
        if(draw_cursor):
            draw_polygon(surface,((255-i*8)%255,0,(255-i*8)%255),cell_poly,2)
            i+=1
            refresh()
        if(draw_numbers):
            draw_text(tempsurf,str(cell),ccenter[0],ccenter[1],color,40)
        for index in range(len(tiling[cell])):
            # print(cell,tiling[cell],tiling[cell][index])
            nextcellindex = tiling[cell][index]
            nextcell, nextp = nextcellindex
            # print(nextcell,tiling[nextcell],cell,nextp)
            try:nextcell_shift = tiling[nextcell].index((cell,-nextp))
            except:nextcell_shift = tiling[nextcell].index((cell,nextp))
            extp1,extp2 = cell_poly[(index+1)%len(cell_poly)], cell_poly[index]
            nextcell_stub = xgon(len(tiling[nextcell]), extp1,extp2)
            # Reorient it
            pa, pb = nextcell_stub[-nextcell_shift], nextcell_stub[(-nextcell_shift+1)%len(nextcell_stub)]
            ccenter = rounded_center(nextcell_stub,5)
            if(ccenter in visitedcoords):
                continue
            if(nextp==0 and cell!=nextcell):
                insidecells.append((pa,pb,nextcell,0)) #oriented at zero!
            else:
                # pygame.draw.aaline(tempsurf,color,extp1,extp2)
                pygame.draw.line(tempsurf2,(0,0,0),convertToTuple(extp1),convertToTuple(extp2),width=5)
                pygame.draw.line(tempsurf,color,convertToTuple(extp1),convertToTuple(extp2),width=3)

                outsidecells.append((pa,pb,nextcell,0))
    #[TODO] iterlevel return candidates to parent which process them so that there are no stealing between levels
    if(iterlevel>0):
        for celldata in outsidecells:
            p1,p2,cell,orientation = celldata

            cell_poly = xgon(len(tiling[cell]), p1, p2)
            ccenter = rounded_center(cell_poly, 5)
            if ccenter not in visitedcoords:
                v = draw_tiling(p1,p2,surface,cell,orientation,tiling,iterlevel-1,itercolors[:],visitedcoords)
                visitedcoords.extend(v)
                # print("outside",iterlevel,outsidecells)
    surface.blit(tempsurf2,(0,0))
    surface.blit(tempsurf,(0,0))
    refresh()
    # input()
    return visitedcoords






def draw_polynet(surf,surface2,polyhedron,startface,startorientation,p1,p2,tilingname,polyname,unusedfaces = None):
    xx,yy,XX,YY = 9999,9999,0,0

    if(unusedfaces==None):
        unusedfaces = unusedfacesdict.get((tilingname,polyname),None) or []
    visited_faces = list()
    visits = [(startface,startorientation,p1,p2)]

    while(visits):
        face, orientation, p1, p2 = visits.pop()
        if(face in visited_faces):
            continue
        visited_faces.append(face)
        face_poly = xgon(len(polyhedron[face]),p1,p2)
        face_poly = face_poly[orientation:]+face_poly[:orientation] #align
        textsize = int(((p1.x-p2.x)**2+(p1.y-p2.y)**2)**0.5/2)
        center = centerpoint(face_poly)
        x,y = int(center[0]),int(center[1])

        if(face not in unusedfaces):
            color1 = (0,0,255)
            color2 = (0,0,128)
        else:
            color1 = (255,0,0)
            color2 = (128,0,0)
        if(face!=startface):
            pygame.draw.circle(surface2, color1,(x,y), int(textsize/2))
            surf.blit(surface2, (0, 0))
            pygame.draw.polygon(surface2, color1, convertToTuples(face_poly), 0)
            surf.blit(surface2, (0, 0))
            surface2.fill((0,0,0,0))
        pygame.draw.polygon(surf, color2, convertToTuples(face_poly), 1)
        text = pygame.font.SysFont(None, textsize).render(str(face), True, (0,0,0))
        surf.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

        for x,y in face_poly:
            x=int(x)
            y=int(y)
            xx, yy, XX, YY = min(x, xx), min(y, yy), max(XX, x), max(YY, y)
        for index,nextface in enumerate(polyhedron[face]):
            face_shift = polyhedron[nextface].index(face)
            # Create a stub nextface at the edge of the current face
            nextface_stub = xgon(len(polyhedron[nextface]), face_poly[(index+1)%len(face_poly)], face_poly[index])
            # Reorient it
            pa, pb = nextface_stub[-face_shift], nextface_stub[(-face_shift+1)%len(nextface_stub)]
            orientation = polyhedron[nextface].index(face)

            if face not in unusedfaces or nextface in unusedfaces:
                visits.insert(0,(nextface,0,pa,pb))
    return xx,yy,XX,YY

def draw_background(surf,grid,color=(0,0,0),width=2,numbers=False):
    for data in grid.values():
        points = data[0]
        #cell = data[1]
        #distance = data[2] #not always available, distance from center
        # print(points)
        pygame.draw.polygon(surf, color, convertToTuples(points), width)
        if(numbers):
            cell = data[1]
            ccenter=centerpoint(points)
            draw_text(surf, str(cell), ccenter[0], ccenter[1], color, 40)

def draw_polygon(surf,color,points,width):
    pygame.draw.polygon(surf, color, convertToTuples(points), width)

def wait_for_input():
    clock = pygame.time.Clock()
    running=True
    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            break;
        if(len(pygame.event.get())==0):
            clock.tick(20)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                #print("Resume with mouse",e.type,flush=True)
                running = False
            if e.type == pygame.KEYDOWN:
                running = False
                #print("Resume with key",e.key,flush=True)
            if e.type == pygame.QUIT:
                running = False
                print("Quit!",flush=True)
                pygame.quit()
def refresh():
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

def cell_match(tiling, previous_case, newcaseid):
    #Imported from screenspaceroller
    """tiling = dict
previous_case = int
newcaseid = tuple"""
    current_case, id = newcaseid
    # Match mirror id first
    for index, pc in enumerate(tiling[current_case]):
        pcc, pid = pc
        if (pcc == previous_case and pid == -id):
            return index
    # Match same id
    for index, pc in enumerate(tiling[current_case]):
        pcc, pid = pc
        if (pcc == previous_case and pid == id):
            return index
    print(previous_case,newcaseid,tiling)

def map_screenspace(tiling, startcell, area, p1, p2, precision, limit=False):
    #imported from screenspaceroller
    "visited areas[center points: (polygon, cell number)]"
    visited_areas = dict()
    visits = [(startcell, p1, p2)]
    while (visits):
        cell, p1, p2 = visits.pop()
        cface = xgon(len(tiling[cell]), p1, p2)
        ccenter = tuple(floatcenterpoint(cface))
        ccenter = int(round(ccenter[0] / precision) * precision), int(round(ccenter[1] / precision) * precision)

        if not (area[0] < ccenter[0] < area[2]) or not (area[1] < ccenter[1] < area[3]):
            continue
        if (ccenter in visited_areas):
            continue

        visited_areas[ccenter] = (cface, cell)  # later for drawing

        for index, nextcellid in enumerate(tiling[cell]):
            cell_shift = cell_match(tiling, cell, nextcellid)
            nextcell, id = nextcellid
            # Create a stub ncface at the edge of the current cface
            nextface_stub = xgon(len(tiling[nextcell]), cface[(index + 1) % len(cface)], cface[index])
            # Reorient it
            pa, pb = nextface_stub[-cell_shift], nextface_stub[(-cell_shift + 1) % len(nextface_stub)]
            if(not limit or id==0 and nextcell!=cell):
                visits.append((nextcell, pa, pb))
    return visited_areas


def draw_answer(filename,tilingname,polyname,visits,grid,polyhedron,p1,p2,startface,startorientation,w,h,unusedfaces):
    #no need for startcase because grid and p1,p2 is enough
    surf = pygame.Surface((w,h))
    surf.fill((255,255,255))
    face = xgon(len(polyhedron[startface]),p1,p2)
    draw_background(surf,grid)
    surface2 = pygame.Surface((w,h), pygame.SRCALPHA)
    surface2.set_colorkey((0, 0, 0))
    surface2.set_alpha(100)

    pygame.draw.polygon(surf, (255,255,0), convertToTuples(face), 0)
    xx,yy,XX,YY = draw_polynet(surf,surface2,polyhedron,startface,startorientation,p1,p2,tilingname, polyname,unusedfaces)
    surface2.set_alpha(255)
    text = pygame.font.SysFont(None, 30).render(tilingname+" with "+polyname, True, (0, 0, 0))
    xx-=10
    XX+=10
    yy-=10+text.get_height()
    YY+=10
    if XX-xx<text.get_width()+2:
        xx-=int(text.get_width()-(XX-xx)+2)/2
        XX+=int(text.get_width()-(XX-xx)+2)
    pygame.draw.rect(surf, (255,255,255),(xx,yy,text.get_width()+2,text.get_height()+2))
    surf.blit(text, (xx+1,yy+1))
    # sub = screen.subsurface(rect)
    # print(xx,yy,XX,YY,w,h)
    pygame.image.save(surf.subsurface([xx,yy,XX-xx,YY-yy]),filename)

def canon_cfo(tilingname,polyname,c,f,o):
    f,o = canon_fo(polyname,f,o)
    c,o = canon_co(tilingname,c,o)
    return c,f,o

def draw_answers_nets(rollersdata):
    rollerscount = 0
    print("Generating rollers nets images")
    types = "roller","hollow", "band"," area"
    for (tilingname,polyname),value in rollersdata.items():
        if(value!=None and value["type"]=="roller"):
            print((tilingname,polyname), value.keys())
            group_max = sum(1 for group_data in value["all_data"] if group_data and group_data["type"]=="roller")
            group_counter = 0
            explored_cfo = set()
            for group_index,group_data in enumerate(value["all_data"]):
                if group_data and group_data["type"]=="roller":
                    # print(group_data.keys())
                    # print(group_data["symmetry_vectors"])
                    # print(group_data["exploration"])
                    # print("Current group:",value["CFO_class_groups"][group_index], value["CFO_class_groups"][group_index][0])
                    # print("Classes",len(value["CFO_classes"]),value["CFO_classes"])

                    tiling = all_tilings[tilingname]
                    net = all_nets[polyname]
                    #instead of an arbitrary, choose the least frequent face

                    existing_faces = set(net)
                    used_faces = set(f for cfo_group in value["CFO_class_groups"][group_index] for c,f,o in value["CFO_classes"][cfo_group])
                    unused_faces = existing_faces-used_faces

                    face_counter = {facesize: sum(1 for face in net if len(net[face])==facesize) for facesize in set(len(net[face]) for face in used_faces)}
                    rarest_face = sorted((face_counter[len(net[face])], face) for face in used_faces)[0][1]

                    # c,f,o = list(value["CFO_classes"][value["CFO_class_groups"][group_index][0]])[0]
                    all_cfo = {(c,f,o) for cfo_group in value["CFO_class_groups"][group_index] for c,f,o in value["CFO_classes"][cfo_group]}
                    if(all_cfo.intersection(explored_cfo)):
                        # print("cfo known")
                        continue
                    all_cfo2 = {canon_cfo(tilingname,polyname,c,f,o) for (c,f,o) in all_cfo}
                    if (all_cfo2.intersection(explored_cfo)):
                        # print("cfo known")
                        continue
                    explored_cfo=explored_cfo.union(all_cfo)
                    explored_cfo=explored_cfo.union(all_cfo2)
                    c,f,o =  [(c,f,o) for c,f,o in all_cfo if f==rarest_face][0]
                    # if(tilingname.startswith("2u03") and polyname=="j87"):
                    #     print(face_counter)
                    #     print("face",rarest_face,"of size",len(net[rarest_face]))

                    area = (-200, -200, 1000, 1000)
                    area2 = (0, 0, 800, 800)
                    xx = (area[0] + area[2]) / 2
                    yy = (area[1] + area[3]) / 2
                    p1 = RollyPoint(xx, yy)
                    EDGESIZE = 50
                    p2 = RollyPoint(xx + EDGESIZE, yy)
                    precision = 7

                    mapping =  map_screenspace(tiling, c, area, p1, p2, precision)


                    gc = ""
                    if(group_max>1):
                        group_counter+=1
                        if(group_counter>1):
                            gc = " (%s)"%str(group_counter)
                            print(tilingname,polyname,"has",group_counter,"answers")
                    try:os.mkdir("rolled_nets/")
                    except:pass
                    rollerscount+=1
                    filename = "rolled_nets/[%03d]"%rollerscount+tilingname + " @ " + polyname + gc + ".png"

                    draw_answer(filename, tilingname, polyname, None, mapping, net, p1, p2, f, o,area2[2], area2[3],unused_faces)
    print("Generated roller nets images")




if __name__ == "__main__":
    if(ROLLING_NETS):
        from _resources.tiling_dicts import uniform_tilings as all_tilings
        from _resources.poly_dicts import all_nets
        import os
        import pickle
        with open("../rolling_results.pickle", "rb") as handle:
            rollingresults = pickle.load(handle)
        draw_answers_nets(rollingresults)