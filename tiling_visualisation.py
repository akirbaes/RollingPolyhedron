"""Tileset visualiser by Akira Baes
#just draws a tiling
#useless or out-to-date functions copied from main
"""
import os
import pprint
import sys

from GenPngScreenspaceRoller import draw_background, refresh, wait_for_input
from GeometryFunctions import *
from sys import setrecursionlimit
import DrawingFunctions as Draw

from tilings_oldformat import *

all_tilings = dict()
path = "isogonal_tilings"
for dirpath, dirnames, filenames in os.walk(path):

    for name in filenames:
        if name.endswith((".py")):
            pathname = os.path.join(dirpath, name)
            f = open(pathname)
            data = f.read()
            f.close()
            exec(data)

isogonals = all_tilings
print(isogonals)



setrecursionlimit(10 ** 4)
WIDTH = 800
HEIGHT = 800
EDGESIZE = 50
p1 = RollyPoint(300, 300)
p2 = RollyPoint(300 + EDGESIZE, 300)  # 350 300
textsize = int(round((EDGESIZE) / 2))
Draw.initialise_drawing(WIDTH, HEIGHT)
def make_shape(points, color, filling=0):
    color = (180, 180, 180)
    Draw.polygon_shape(points, color, filling)
    Draw.polygon_shape(points, (0, 0, 0), 0, outline=2)
    return points
def make_cursor(points, color=5, filling=0.1):
    Draw.polygon_cursor(points, color, filling)
    Draw.polygon_cursor(points, color, 0, outline=2)
    return points
def number(id, point):
    # graph.create_text((point.x, point.y), text=str(id))
    Draw.text_center(str(id), point.x, point.y, (0, 0, 0), textsize)
def numcenter(id, points):
    number(id, sum(points, RollyPoint(0, 0)) / len(points))
def numbours(id, neighbours, points):
    m = sum(points, RollyPoint(0, 0)) / len(points)
    number(id, m)
    for i in range(len(neighbours)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        p = ((p1 + p2) / 2 + m) / 2
        number(neighbours[i] % len(order), p)


class RollyPoly:
    def __init__(self, id, points, color=None, full=False, alpha=1):
        self.n = []
        self.id = id
        self.points = points
        self.color = color
        realid = id % len(order)
        if (full):
            self.pid = make_shape(points, color, 1)
        elif (color == None):
            # self.pid = make_shape(points, (int((id - realid) / len(order))) ,0.7)
            self.pid = make_shape(points, (0, 0, 0), 0)
        else:
            self.pid = make_shape(points, color, 1)
        # print(points)

        # number(realid, sum(points, Point(0, 0)) / len(points))

    def order(self, neighbor):
        index = self.n.index(neighbor)
        return self.n[neighbor:] + self.n[:neighbor]

    def fill(self, neighbours):
        self.n = list(neighbours)

    def __eq__(self, other):
        return self.id == other

    def has_points(self, pts):
        # print(sorted(self.points),sorted(pts),sorted(self.points)==sorted(pts))
        return sorted(round(x) for x in self.points) == sorted(round(x) for x in pts)

    def remplis(self, color=(255, 0, 0)):
        return
        make_shape(self.points, (255, 0, 0), 0.1)

    def __repr__(self):
        return str(self.points)

    def center(self) -> tuple:
        return centerpoint(self.points)


def get_face_points(p1, p2, face, noisy=True):
    faceid = face % len(order)
    if (len(shape[faceid])) == 3:
        points = triangle(p1, p2)
        if (noisy): print(" triangle ", face)
    elif (len(shape[faceid])) == 4:
        points = square(p1, p2)
        if (noisy): print(" square ", face)
    elif (len(shape[faceid])) == 6:
        points = hexagon(p1, p2)
        if (noisy): print(" hexagon ", face)
    elif (len(shape[faceid])) == 8:
        points = octagon(p1, p2)
        if (noisy): print(" octagon ", face)
    elif (len(shape[faceid])) == 12:
        points = dodecagon(p1, p2)
        if (noisy): print(" dodecagon ", face)
    else:
        raise IndexError(len(shape[faceid]))
    return points


def visualise(p1, p2, newshape, oldshape, color=0, drawnshapes=None, shapespoly=None, fill=True, ord=None,
              prints=False, refresh = False):
    realshape = newshape % len(order)
    if (drawnshapes == None):
        drawnshapes = list()
    if (prints): print("Visualise---------", newshape, oldshape, "(%s)" % realshape, shape[realshape])
    if (shapespoly == None):
        shapespoly = list()
    points = get_face_points(p1, p2, newshape, False)
    shapespoly.append(RollyPoly(newshape, points, color, fill))
    current = shape[realshape]
    if (prints): print(current, 'of shape', realshape, ', coming from', oldshape)
    try:
        index = current.index(oldshape)
    except:
        # Maybe the -P +P formula is not respected
        index = current.index(-oldshape + 2 * (oldshape % len(order)))
        #print("Exception matching", oldshape % len(order), "+%dP" % (oldshape // len(order)))

    current = current[index:] + current[:index]
    shapespoly[-1].fill(current)
    drawnshapes.append(realshape)
    if(refresh):
        Draw.refresh()
    # sleep(0.1)
    # print("I have",len(points),"points")
    # if(newshape==realshape):
    # print("Next ones:",current)
    for index, p in enumerate(current):
        # print("Looking",p)
        # print(index)
        p1 = points[index % len(points)]
        p2 = points[(index + 1) % len(points)]
        if (p not in drawnshapes) and (p % len(order) == p):
            visualise(p2, p1, p, newshape, color, drawnshapes, shapespoly, fill)
        """else:
			if(p in drawnshapes):
				print("P in drawn:",p,drawnshapes,p not in drawnshapes)
			if(p%len(order)!=p):
				print("P not to draw",p,p%len(order))"""
    return shapespoly


def point_outside(point):
    x, y = point.x, point.y
    if (x < 0 or y < 0 or x > WIDTH or y > HEIGHT):
        return True

def case_match(tiling, previous_case, newcaseid):
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
cell_match=case_match

def map_screenspace(tiling, startcell, area, p1, p2, precision, limit=False):
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

def points_outside(points):
    for point in points:
        if (point_outside(point)):
            return True
    return False


def swap(oldshape):
    return -oldshape + 2 * (oldshape % len(order))


def rest(oldshape):
    return oldshape - (oldshape % len(order))


def real(shape):
    return shape % len(order)


def rounded(pts):
    return tuple(round(x / 10) for x in pts)


from random import randint

tempshape = []


def fill_screen(p1, p2, newshape, oldshape=None, exploredpoints=None, drawnpoly=None, color=None, prints=False, refresh=True):
    global tempshape

    if (exploredpoints == None):
        exploredpoints = list()
    if (drawnpoly == None):
        drawnpoly = list()
    realshape = newshape % len(order)
    if (realshape != newshape):
        print("Erreur de paramètre....", realshape, newshape)
    points = get_face_points(p1, p2, newshape, False)

    if (points_outside(points)):
        return
    if (centerpoint(points) in exploredpoints):
        return

    exploredpoints.append(centerpoint(points))
    current = shape[realshape]
    if (prints): print("Oldshape:", oldshape)
    if (oldshape == None):
        # Turns a n+P number into n-P (find pair)
        oldshape = -current[0] + 2 * (current[0] % len(order))
        # n%P - (n-n%P) = -n + 2*(n%P)

    # if(oldshape!=None and newshape==realshape): #on explore même quand on est dehors
    # print(oldshape,"in",current,newshape,realshape)
    if (prints): print(current, "of shape", realshape, "coming from", oldshape, flush=True)
    try:
        index = current.index(oldshape)
    except:
        # Maybe the -P +P formula is not respected
        index = current.index(-oldshape + 2 * (oldshape % len(order)))
        # print("Exception matching", oldshape % len(order), "+%dP" % (oldshape // len(order)))
    current = current[index:] + current[:index]
    # print("Previous:",oldshape,"Next:",current)
    # screen.fill((255,255,255))
    # sleep(0.5)
    # print("I have",len(points),"points")
    # if(newshape==realshape):
    drawn = False
    for poly in drawnpoly:
        if (poly.has_points(points)):
            drawn = True
    if not drawn:
        # print("Not yet drawn")
        # print(drawnpoly)
        if (color == None):
            c = randint(0, 100)
            c = -1
            drawnpoly += visualise(p1, p2, newshape, oldshape, c, fill=False, refresh=refresh)
        else:
            visualise(p1, p2, newshape, oldshape, color, fill=False, refresh=refresh)
        # print("Drawn")
    # print(drawnpoly[-1])
    # color+=1
    # print("Finished drawing")
    for index, p in enumerate(current):
        # print(index)
        p1 = points[index % len(points)]
        p2 = points[(index + 1) % len(points)]
        # print("Do I explore ",realshape," to ",p,"(",p%len(order),") ?")
        if ((p % len(order) == p) and (p % len(order) != realshape)):
            fill_screen(p2, p1, real(p), newshape - rest(p), exploredpoints, drawnpoly, color)

    for index, p in enumerate(current):
        # print(index)
        p1 = points[index % len(points)]
        p2 = points[(index + 1) % len(points)]
        if ((p % len(order) != p) or p % len(order) == realshape):
            # sleep(0.5)
            # color+=1
            # print(newshape,p,rest(p))
            # print(newshape + rest(p))
            fill_screen(p2, p1, real(p), newshape - rest(p), exploredpoints, drawnpoly, color)


screenshot_counter = 0


def convert_tiling(tiling):
    p = len(tiling)
    return {key: list((((x % p), (x // p)) for x in value)) for key, value in tiling.items()}


def convert_all_tiling(all_tilings, category_name):
    output = """#dict[face]=[(neighbour_face, differenciator)]
#neighbour faces in clockwise order
#match differenciator: -d with +d, else d with d\n"""
    output += category_name + "= dict()\n"
    for tilename in all_tilings:
        new_tiling = convert_tiling(all_tilings[tilename])
        dictline = pprint.pformat(new_tiling, indent=4, sort_dicts=True,width=110)
        output += "%s['%s'] = \\\n%s\n\n" % (category_name, tilename, dictline)
    try:
        os.mkdir("tiling_dicts")
    except:
        pass
    f = open("tiling_dicts/" + category_name + ".py", "w")
    f.write(output)
    f.close()


if __name__ == "__main__":
    global shape_name
    global net
    global order
    if len(sys.argv)>1 and sys.argv[1].endswith(".oldformat"):
        with open(sys.argv[1],"r") as codefile:
            code = codefile.read()
            all_tilings = dict()
            dictpart = code[code.index("{"):]
            namepart = code[code.index("'")+1:code.index("]")-1]
            print(namepart)
            shape_name = namepart
            print(dictpart)
            all_tilings[namepart]=eval(dictpart)
            for tilingname, tiling in all_tilings.items():
                net = tiling
                shape = net
                tilename = tilingname
                order = list(tiling.keys())
                drawn = visualise(p1, p2, 0, net[0][0], 2)
                fill_screen(p1, p2, order[0], color=3,refresh=False)
            Draw.refresh()
            Draw.wait_for_input()
    elif len(sys.argv)>1 and sys.argv[1].endswith(".py"):
        with open(sys.argv[1],"r") as codefile:
            code = codefile.read()
            dictpart = code[code.index("{"):]
            namepart = code[code.index("'")+1:code.index("]")-1]
            print(namepart)
            print(dictpart)
        tiling=eval(dictpart)
        import pygame
        pygame.init()
        screen = pygame.display.set_mode((800, 800), pygame.DOUBLEBUF)
        screen.fill((255, 255, 255, 255))
        outlines = pygame.Surface((800, 800), pygame.SRCALPHA)
        area = (0,0,1000,1000)

        mapping = map_screenspace(tiling, 0, area, p1, p2, 1)
        single = map_screenspace(tiling, 0, area, p1, p2, 1,limit=True)
        outlines = pygame.Surface((800, 800), pygame.SRCALPHA)
        outlines.fill((255, 0, 255, 0))
        print(mapping)
        draw_background(screen, mapping, (0,0,0))
        draw_background(screen, single, (0,0,0),6)
        draw_background(screen, single, (255,0,0))
        refresh()
        pygame.image.save(screen, os.path.dirname(sys.argv[1])+os.sep+namepart+".png")

        wait_for_input()
    else:
        # for shape_name in missing:
        # for shape_name in shapes_names:
        # convert_all_tiling(platonics, "platonic_tilings")
        # convert_all_tiling(archimedeans, "archimedean_tilings")
        # convert_all_tiling(isogonals, "isogonal_tilings")

        for tilename in platonics:
            net = platonics[tilename]
            tilename = "platonics_" + tilename
            print("]" * 50 + tilename)
            Draw.text_topleftalign(tilename, 2, 2, (0, 0, 0), 30)
            shape = net
            order = sorted(net.keys())
            visualise(p1, p2, 0, net[0][0], 2)
            fill_screen(p1, p2, order[0], color=None)
            Draw.text_topleftalign(tilename, 2, 2, (255, 0, 0), 30, bgcolor=(255, 255, 255))
            Draw.refresh()

            try:os.mkdir("platonic_tilings_images")
            except:pass
            Draw.save_screen("platonic_tilings_images/" + tilename + ".png")
            # Draw.wait_for_input()
            Draw.empty_shapes()
        isogonals['3.4^2.6;3.6.3.6)_2'] = \
            {0: [2, 8, 1, 13],
             1: [False, 29, 17, 3, 22, 34],
             2: [False, 16, 21],
             3: [1, 10, 4, 5],
             4: [3, 31, 26]}

        for tilename in isogonals:
            net = isogonals[tilename]
            tilename = "isogonal_" + tilename
            print("]" * 50 + tilename)
            Draw.text_topleftalign(tilename, 2, 2, (0, 0, 0), 30)
            shape = net
            order = sorted(net.keys())
            visualise(p1, p2, 0, net[0][0], 2)
            fill_screen(p1, p2, order[0], color=None)
            Draw.text_topleftalign(tilename, 2, 2, (255, 0, 0), 30, bgcolor=(255, 255, 255))
            Draw.refresh()
            try:os.mkdir("isogonal_tilings_images")
            except:pass
            Draw.save_screen("isogonal_tilings_images/" + tilename + ".png")
            # Draw.wait_for_input()
            Draw.empty_shapes()
        # exit()

        for tilename in archimedeans:
            net = archimedeans[tilename]
            tilename = "archimedean_" + tilename
            print("]" * 50 + tilename)
            Draw.text_topleftalign(tilename, 2, 2, (0, 0, 0), 30)
            shape = net
            order = sorted(net.keys())
            visualise(p1, p2, 0, net[0][0], 2)
            fill_screen(p1, p2, order[0], color=None)
            Draw.text_topleftalign(tilename, 2, 2, (255, 0, 0), 30, bgcolor=(255, 255, 255))
            Draw.refresh()
            try:os.mkdir("archimedean_tilings_images")
            except:pass
            Draw.save_screen("archimedean_tilings_images/" + tilename + ".png")
            # Draw.wait_for_input()
            Draw.empty_shapes()
