"""Roll a shape in a space with a given tiling and starting position"""
from RollyPoint import RollyPoint
from tiling_dicts.uniform_tiling_supertiles import uniform_tilings
from poly_dicts.regular_faced_polyhedron_nets import all_nets
from math import pi, sqrt
from time import time
from random import choice, randint, shuffle

SLOW = False
TIME_LIMIT = 5
WIDTH = 800
EDGESIZE = 50

stable_showcase = [('tetrahedron', '1u01 (3^6)'), ('octahedron', '1u01 (3^6)'), ('icosahedron', '1u01 (3^6)'), ('j10', '1u01 (3^6)'), ('j11', '1u01 (3^6)'), ('j12', '1u01 (3^6)'), ('j13', '1u01 (3^6)'), ('j17', '1u01 (3^6)'), ('j50', '1u01 (3^6)'), ('j51', '1u01 (3^6)'), ('j62', '1u01 (3^6)'), ('j84', '1u01 (3^6)'), ('j85', '1u01 (3^6)'), ('j86', '1u01 (3^6)'), ('j87', '1u01 (3^6)'), ('j88', '1u01 (3^6)'), ('j89', '1u01 (3^6)'), ('j90', '1u01 (3^6)'), ('cube', '1u02 (4^4)'), ('j8', '1u02 (4^4)'), ('j37', '1u02 (4^4)'), ('tetrahedron', '1u04 (3^4x6)'), ('octahedron', '1u04 (3^4x6)'), ('icosahedron', '1u04 (3^4x6)'), ('j12', '1u04 (3^4x6)'), ('j13', '1u04 (3^4x6)'), ('j17', '1u04 (3^4x6)'), ('j51', '1u04 (3^4x6)'), ('j84', '1u04 (3^4x6)'), ('cuboctahedron', '1u06 (3^2x4x3x4)'), ('j26', '1u06 (3^2x4x3x4)'), ('j31', '1u06 (3^2x4x3x4)'), ('cuboctahedron', '1u07 (3x4x6x4)'), ('tetrahedron', '2u01 (3^6;3^4x6)1'), ('octahedron', '2u01 (3^6;3^4x6)1'), ('icosahedron', '2u01 (3^6;3^4x6)1'), ('j12', '2u01 (3^6;3^4x6)1'), ('j13', '2u01 (3^6;3^4x6)1'), ('j17', '2u01 (3^6;3^4x6)1'), ('j50', '2u01 (3^6;3^4x6)1'), ('j51', '2u01 (3^6;3^4x6)1'), ('j84', '2u01 (3^6;3^4x6)1'), ('j85', '2u01 (3^6;3^4x6)1'), ('j87', '2u01 (3^6;3^4x6)1'), ('j88', '2u01 (3^6;3^4x6)1'), ('j89', '2u01 (3^6;3^4x6)1'), ('tetrahedron', '2u02 (3^6;3^4x6)2'), ('octahedron', '2u02 (3^6;3^4x6)2'), ('icosahedron', '2u02 (3^6;3^4x6)2'), ('j10', '2u02 (3^6;3^4x6)2'), ('j11', '2u02 (3^6;3^4x6)2'), ('j12', '2u02 (3^6;3^4x6)2'), ('j13', '2u02 (3^6;3^4x6)2'), ('j17', '2u02 (3^6;3^4x6)2'), ('j50', '2u02 (3^6;3^4x6)2'), ('j51', '2u02 (3^6;3^4x6)2'), ('j84', '2u02 (3^6;3^4x6)2'), ('j85', '2u02 (3^6;3^4x6)2'), ('j86', '2u02 (3^6;3^4x6)2'), ('j87', '2u02 (3^6;3^4x6)2'), ('j88', '2u02 (3^6;3^4x6)2'), ('j89', '2u02 (3^6;3^4x6)2'), ('j85', '2u03 (3^6;3^3x4^2)1'), ('j87', '2u03 (3^6;3^3x4^2)1'), ('j88', '2u03 (3^6;3^3x4^2)1'), ('j85', '2u04 (3^6;3^3x4^2)2'), ('j87', '2u04 (3^6;3^3x4^2)2'), ('j88', '2u04 (3^6;3^3x4^2)2'), ('j90', '2u04 (3^6;3^3x4^2)2'), ('cuboctahedron', '2u05 (3^6;3^2x4x3x4)'), ('cuboctahedron', '2u09 (3^3x4^2;3^2x4x3x4)1'), ('cuboctahedron', '2u14 (3^2x4x3x4;3x4x6x4)'), ('j26', '2u14 (3^2x4x3x4;3x4x6x4)'), ('j31', '2u14 (3^2x4x3x4;3x4x6x4)'), ('cuboctahedron', '3uhv16 (3^6;3^2x4x3x4;3x4x6x4)1'), ('cuboctahedron', '3uhv17 (3^6;3^2x4x3x4;3x4x6x4)2'), ('tetrahedron', '3unhv40 (3^6;3^6;3^4x6^1)'), ('octahedron', '3unhv40 (3^6;3^6;3^4x6^1)'), ('icosahedron', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j10', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j11', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j12', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j13', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j17', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j50', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j51', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j84', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j85', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j86', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j87', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j88', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j89', '3unhv40 (3^6;3^6;3^4x6^1)'), ('j90', '3unhv40 (3^6;3^6;3^4x6^1)'), ('tetrahedron', '3unhv41 (3^6;3^6;3^4x6^2)'), ('octahedron', '3unhv41 (3^6;3^6;3^4x6^2)'), ('icosahedron', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j10', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j11', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j12', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j13', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j17', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j50', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j51', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j84', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j85', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j86', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j87', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j88', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j89', '3unhv41 (3^6;3^6;3^4x6^2)'), ('j90', '3unhv41 (3^6;3^6;3^4x6^2)'), ('tetrahedron', '3unhv42 (3^6;3^6;3^4x6^3)'), ('octahedron', '3unhv42 (3^6;3^6;3^4x6^3)'), ('icosahedron', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j10', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j11', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j12', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j13', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j17', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j50', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j51', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j84', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j85', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j86', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j87', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j88', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j89', '3unhv42 (3^6;3^6;3^4x6^3)'), ('j90', '3unhv42 (3^6;3^6;3^4x6^3)'), ('tetrahedron', '3unhv43 (3^6;3^4x6;3^4x6)'), ('octahedron', '3unhv43 (3^6;3^4x6;3^4x6)'), ('icosahedron', '3unhv43 (3^6;3^4x6;3^4x6)'), ('j12', '3unhv43 (3^6;3^4x6;3^4x6)'), ('j13', '3unhv43 (3^6;3^4x6;3^4x6)'), ('j17', '3unhv43 (3^6;3^4x6;3^4x6)'), ('j50', '3unhv43 (3^6;3^4x6;3^4x6)'), ('j51', '3unhv43 (3^6;3^4x6;3^4x6)'), ('j84', '3unhv43 (3^6;3^4x6;3^4x6)'), ('j87', '3unhv43 (3^6;3^4x6;3^4x6)'), ('j85', '3unhv44 (3^6;3^6;3^3x4^2)1'), ('j87', '3unhv44 (3^6;3^6;3^3x4^2)1'), ('j88', '3unhv44 (3^6;3^6;3^3x4^2)1'), ('j90', '3unhv44 (3^6;3^6;3^3x4^2)1'), ('j85', '3unhv45 (3^6;3^6;3^3x4^2)2'), ('j87', '3unhv45 (3^6;3^6;3^3x4^2)2'), ('j88', '3unhv45 (3^6;3^6;3^3x4^2)2'), ('j90', '3unhv45 (3^6;3^6;3^3x4^2)2'), ('cuboctahedron', '3unhv48 (3^6;3^2x4x3x4;3^2x4x3x4)'), ('j26', '3unhv48 (3^6;3^2x4x3x4;3^2x4x3x4)'), ('j31', '3unhv48 (3^6;3^2x4x3x4;3^2x4x3x4)')]

def draw_text(surf, text, x, y, color, size,underline=False):
    font = pygame.font.SysFont(None, int(round(size)))
    if(underline):
        font.set_underline(True)
    text = font.render(text, True, color,background="white")
    surf.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))
def drawtemp(points,color,outline=0):
    temp.fill((255, 255, 255, 0))
    draw_polygon(temp, color, points, outline)
    screen.blit(temp, (0, 0))

def convertToTuples(points): #make sure they are non-mutable
    return  tuple((int(x), int(y)) for x,y in points)
def centerpoint(points):
    mx = sum(x for x,y in points)
    my = sum(y for x,y in points)
    return (int(round(mx / len(points))), int(round(my / len(points))))
def distance(p1,p2):
    return sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
from copy import deepcopy
def ngon(sides,p1,p2): #returns an n-gon of sides starting clockwise from p1,p2
    sol = [(p1), (p2)]
    pa = RollyPoint(p1)
    pb = RollyPoint(p2)
    for i in range(sides-2):
        pn = pb + (pa - pb).rotate(-(sides-2) * pi / (sides))
        sol.append((pn.as_tuple()))
        pa = deepcopy(pb)
        pb = deepcopy(pn)
    return sol

def draw_background(surf,grid,color=(0,0,0),width=2,numbers=False):
    for data in grid.values():
        #data = (cface, cell)
        points = data[0]
        #cell = data[1]
        pygame.draw.polygon(surf, color, convertToTuples(points), width)
        if(numbers):
            cell = data[1]
            ccenter=centerpoint(points)
            draw_text(surf, str(cell), ccenter[0], ccenter[1], color, 40)

def draw_polygon(surf,color,points,width):
    pygame.draw.polygon(surf, color, convertToTuples(points), width)

def wait_for_input():
    clock = pygame.time.Clock()
    running = True
    while running:
        # keys = pygame.key.get_pressed()
        # if keys[pygame.K_RETURN]:
        #     break;
        if (len(pygame.event.get()) == 0):
            clock.tick(20)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN or e.type == pygame.KEYDOWN:
                running = False
            if e.type == pygame.QUIT:
                pygame.quit()

def refresh():
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

def cell_match(tiling, previous_case, newcaseid):
    #match two cells based on their pairing id
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

def is_outside(previouscase,newcaseid):
    newcase, id = newcaseid
    if(previouscase==newcase):
        return True
    if id!=0:
        return True
    return False

def map_screenspace(tiling, startcell, area, p1, p2, precision=7, limit_to_one=False):
    #tile the screen with the given tiling
    visited_areas = dict()
    visits = [(startcell, p1, p2)]
    counter = 0
    while (visits):
        cell, p1, p2 = visits.pop()
        cface = ngon(len(tiling[cell]), p1, p2)
        ccenter = tuple(centerpoint(cface))
        #Use an approximate center as cell identifier to know where we are
        # ccenter = int(round(ccenter[0] / precision) * precision), int(round(ccenter[1] / precision) * precision)

        if not (area[0] < ccenter[0] < area[2]) or not (area[1] < ccenter[1] < area[3]):
            continue
        if (ccenter in visited_areas):
            continue
        drawtemp(cface, (255,255,255))
        drawtemp(cface, (128,128,128),2)
        counter+=1
        if counter%50==0:
            refresh()
        # wait_for_input()
        if(visited_areas):
            all_distances = [(distance(ccenter, other), other) for other in visited_areas]
            dist, closest = min(all_distances)
            if (dist < 2):
                # print("Already visited")
                continue
        visited_areas[ccenter] = (cface, cell)  # later for drawing


        for index, nextcellid in enumerate(tiling[cell]):
            cell_shift = cell_match(tiling, cell, nextcellid)
            nextcell, id = nextcellid
            # Create a stub ncface at the edge of the current cface
            nextface_stub = ngon(len(tiling[nextcell]), cface[(index + 1) % len(cface)], cface[index])
            # Reorient it so that neighbours match
            pa, pb = nextface_stub[-cell_shift], nextface_stub[(-cell_shift + 1) % len(nextface_stub)]
            if(not limit_to_one or id==0 and nextcell!=cell):
                visits.append((nextcell, pa, pb))
    return visited_areas

def area_explore(tiling, tilename, net, polyname, mapping,sp1,sp2, startcase=0, startface=0, startorientation=0, ):
    TIMERSTART = time()

    text= pygame.font.SysFont(None,30).render((tilename+"    ") + polyname, True, (0,0,0),(255,255,255))
    titlecard = text.copy()
    titlecard.fill((255,255,255))
    titlecard.blit(text,(0,0))

    screen.blit(outlines, (0, 0))
    screen.blit(titlecard, (0, 0))
    refresh()
    visits = [(startface, startcase, startorientation, sp1, sp2)]
    "mapping= visited areas[center points: (polygon, cell number)]"

    while visits and (TIMERSTART+TIME_LIMIT>time() and TIME_LIMIT>0):
        face, case, orientation, p1, p2 = visits[-1]
        if (len(net[face]) != len(tiling[case])):
            # print("can't explore this")
            visits.pop()
            continue
        cface = ngon(len(net[face]), p1, p2)
        ccenter = list(centerpoint(cface))

        all_distances = [ (distance(ccenter,other),other) for other in mapping]
        dist,closest = min(all_distances)
        if(dist>2):
            # print("Out of map")
            visits.pop()
            continue

        color = tuple(randint(0,255) for i in range(3))
        drawtemp(cface, color)
        neighbours_faces = net[face]
        neighbours_faces = neighbours_faces[orientation:] + neighbours_faces[:orientation] #rotate to match orientation
        possible_directions = list()
        for index, nextcellid in enumerate(tiling[case]):
            nextcell, id = nextcellid #one of the possible directions: cell name, pairing identifier
            nextface = neighbours_faces[index]  # aligned with cell
            if(len(net[nextface])!=len(tiling[nextcell])):
                continue #not same polyhedron

            face_shift = net[nextface].index(face)
            cell_shift = cell_match(tiling,case,nextcellid)
            # Create a stub nface at the edge of the current face
            nextface_stub = ngon(len(net[nextface]), cface[(index + 1) % len(cface)], cface[index])
            pa, pb = nextface_stub[-cell_shift], nextface_stub[(-cell_shift + 1) % len(nextface_stub)]
            #align the points with the right rotation for the next shape

            nextorientation = (-cell_shift + face_shift)%len(nextface_stub)
            nextcenter = list(centerpoint(nextface_stub))

            possible_directions.append((nextface, nextcell, nextorientation, pa, pb))
        if not(possible_directions):
            visits.pop()
            continue
        visits.append(choice(possible_directions))
        screen.blit(outlines, (0, 0))
        screen.blit(titlecard, (0, 0))
        refresh()
        if SLOW:
           wait_for_input()




def common_face(net,tiling):
    for face, neigh in net.items():
        for cell, vois in tiling.items():
            if(len(neigh)==len(vois)):
                return face, cell
    return None, None


if __name__ == "__main__":
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, WIDTH), pygame.DOUBLEBUF)
    outlines = pygame.Surface((WIDTH, WIDTH), pygame.SRCALPHA)
    temp = pygame.Surface((WIDTH, WIDTH), pygame.SRCALPHA)

    xx = WIDTH / 2
    yy = WIDTH / 2
    p1 = (xx, yy)
    p2 = (xx + EDGESIZE, yy)

    startcell = 0
    startface = 0
    startorientation = 0
    area = (0,0,WIDTH, WIDTH)
    shuffle(stable_showcase)
    stable_showcase = [('tetrahedron', '1u01 (3^6)'), ('cube', '1u02 (4^4)')]+stable_showcase
    for polyname, tilename in stable_showcase:
        tiling = uniform_tilings[tilename]
        net = all_nets[polyname]
        startface,startcell = common_face(net,tiling)
        if(startcell==None):
            continue

        print("Map",tilename,polyname)
        mapping = map_screenspace(tiling, startcell, area, p1, p2)
        print("Start",tilename,polyname)
        screen.fill((255, 255, 255, 255))
        draw_background(outlines, mapping)
        area_explore(tiling, tilename, net, polyname, mapping, p1, p2, startcell, startface, startorientation)

        outlines.fill((255, 255, 255, 0))


