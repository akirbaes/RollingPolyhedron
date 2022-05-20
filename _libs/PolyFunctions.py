"""Draw flat polygonal faces"""

from math import atan2
from _libs.GeometryFunctions import *
from _libs.GeometryFunctions import RollyPoint
from _libs import DrawingFunctions as Draw

WIDTH = 800
HEIGHT = 800
EDGESIZE = 50
p1 = RollyPoint(300, 300)
p2 = RollyPoint(300 + EDGESIZE, 300)  # 350 300
textsize = int(round((EDGESIZE) / 2))


def make_shape(points, color, filling=0):
    Draw.polygon_shape(points, color, filling)
    Draw.polygon_shape(points, (0, 0, 0), 0, outline=1)
    return points


def make_cursor(points, color=5, filling=0.1):
    Draw.polygon_cursor(points, color, filling)
    Draw.polygon_cursor(points, color, 0, outline=1)
    return points

class RollyPoly:
    def __init__(self, id, points, color=None, full=False, alpha=1, p=None):
        self.n = []
        self.id = id
        self.points = points
        self.color = color
        if(p!=None):
            realid = id % p
        else:
            realid = id
        if (full):
            self.pid = make_shape(points, color, 1)
        elif (color == None):
            # self.pid = make_shape(points, (int((id - realid) / len(order))) ,0.7)
            self.pid = make_shape(points, (0, 0, 0), 0)
        else:
            self.pid = make_shape(points, color, 0)
        # print(points)

        #number(realid, sum(points, Point(0, 0)) / len(points))
        center = centerpoint(points)
        angle = 180.0*atan2(points[1].y-points[0].y,points[1].x-points[0].x)/pi
        Draw.text_rotated(str(realid),center[0],center[1],(0,0,0),textsize,angle,underline=str(realid) in "0,6,8,9")

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


def get_face_points(shapedict, p1, p2, face, noisy=True):
    faceid = face % len(shapedict)
    if (len(shapedict[faceid])) == 3:
        points = triangle(p1, p2)
        if (noisy): print(" triangle ", face)
    elif (len(shapedict[faceid])) == 4:
        points = square(p1, p2)
        if (noisy): print(" square ", face)
    elif(len(shapedict[faceid]))==5:
        points = pentagon(p1, p2)
        if (noisy): print(" pentagon ", face)
    elif(len(shapedict[faceid]))==6:
        points = hexagon(p1, p2)
        if (noisy): print(" hexagon ", face)
    elif(len(shapedict[faceid]))==8:
        points = octagon(p1, p2)
        if (noisy): print(" octagon ", face)
    elif(len(shapedict[faceid]))==10:
        points = decagon(p1, p2)
        if (noisy): print(" decagon ", face)
    elif(len(shapedict[faceid]))==12:
        points = dodecagon(p1, p2)
        if (noisy): print(" dodecagon ", face)
    else:
        raise IndexError(len(shapedict[faceid]))
    return points


def visualise(polydict, p1, p2, newshape, oldshape, color=(255,0,0), drawnshapes=None, shapespoly=None, fill=True, prints=False,surf=None,screen=None,shapes=None):
    global s
    try:
        print(s)
    except:
        if(surf!=None):
            Draw.set_s(surf,screen,shapes)
    # Copy of extend, but fills the whole space
    realshape = newshape % len(polydict)
    if (drawnshapes == None):
        drawnshapes = list()
    if(prints):print("Visualise---------", newshape, oldshape, "(%s)" % realshape, polydict[realshape])
    if (shapespoly == None):
        shapespoly = list()
    points = get_face_points(polydict,p1, p2, newshape, noisy=False)
    shapespoly.append(RollyPoly(newshape, points, color, fill, p=len(polydict)))
    current = polydict[realshape]
    if(prints):print(current, 'of shape', realshape, ', coming from', oldshape)
    try:
        #match with -k
        index = current.index(oldshape)
    except:
        #match with --k
        index = current.index(-oldshape + 2 * (oldshape % len(polydict)))
        if(prints):print("Matching", "%i[%i]"%(newshape,oldshape),"=",oldshape % len(polydict), "+%d(%i)" % (oldshape // len(polydict), len(polydict)))

    current = current[index:] + current[:index]
    shapespoly[-1].fill(current)
    drawnshapes.append(realshape)

    #Draw.refresh()
    # sleep(0.1)
    # print("I have",len(points),"points")
    # if(newshape==realshape):
    # print("Next ones:",current)
    for index, p in enumerate(current):
        # print("Looking",p)
        # print(index)
        p1 = points[index % len(points)]
        p2 = points[(index + 1) % len(points)]
        if (p not in drawnshapes) and (p % len(polydict) == p):
            visualise(polydict, p2, p1, p, newshape, color, drawnshapes, shapespoly, fill, prints=prints)
        """else:
			if(p in drawnshapes):
				print("P in drawn:",p,drawnshapes,p not in drawnshapes)
			if(p%len(order)!=p):
				print("P not to draw",p,p%len(order))"""
    return shapespoly
