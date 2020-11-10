"""Tileset visualiser by Akira Baes
This version works with manually-inserted tile representations in the code.
Here I have: tetrahedron, cube, pyramid
A future version should interface with a tile-representation-generator directly

First, "extend" show the representation of a single tile with its neighbouring tiles infos

"fill_screen" then fill the screen with the given tile to verify that it is a tile

"explore" is supposed to find all the places that can be rolled into, with a stopping condition when reaching a position+orientation that has already been met,
but it is rather difficult to read to determine if it can roll in the space or not.

V1.1 I'm trying to look at one specific one in more details (hexagonal antiprism), but maximum recrsion depth gets in the way, must rewrite
But by symmetry, there is nothing exceptional to see, only that my algorithm stops too early before filling the screen.
V1.2 rewriting it in several files for pycharm
"""
from tkinter import *
from Point import Point
from time import sleep
from math import pi
from sys import setrecursionlimit
import pygame


pygame.init()
setrecursionlimit(10 ** 6)
root = Tk(className="Shapes representation")  # add a root window named Myfirst GUI
WIDTH = 600
HEIGHT = 600
p1 = Point(300, 300)
p2 = Point(320, 300)  # 350 300
graph = Canvas(root, width=WIDTH, height=HEIGHT)  # add a label to root window
graph.pack()

from PolyAndNets import shapes_names, nets, polys, missing





def pointAngle(a, b, c):
    # Course formula: [AB]x[BC] product
    return ((b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x))


def centerpoint(points):
    mx = 0
    my = 0
    for x, y in points:
        mx += x
        my += y
    return (int(round(mx / len(points))), int(round(my / len(points))))


def square(p1, p2):
    # creates a rectangle clockwise to p1,p2
    p1 = p1
    p2 = p2

    p34 = p1 - p2
    p3 = p2 + Point(p34.y, -p34.x)
    p4 = p3 + p34
    return (p1), (p2), (p3), (p4)


def triangle(p1, p2):
    # creates a triangle clockwise to p1,p2
    p1 = p1
    p2 = p2
    p3 = p1 + (p2 - p1).rotate(pi / 3)
    """pb = p1 + ((p2-p1)/2)
	ph = 
	dist = (p2-p1)"""
    return (p1), (p2), (p3)


def hexagon(p1, p2):
    # creates a triangle clockwise to p1,p2
    p1 = p1
    p2 = p2
    sol = [(p1), (p2)]
    pa = p1
    pb = p2
    for i in range(4):
        pn = pb + (pa - pb).rotate(-2 * pi / 3)
        sol.append((pn))
        pa = pb
        pb = pn
    """pb = p1 + ((p2-p1)/2)
	ph = 
	dist = (p2-p1)"""
    return sol


colors = ("grey", "red", "yellow", "cyan", "magenta", "pink", "orange", "white", "blue", "green", "black")


def make(points, color=0):
    # Creates a shape from given points
    list = []
    w = 2 + (color == 0) * 2
    # print(color)
    c = colors[color % len(colors)]
    for i, point in enumerate(points):
        next = points[(i + 1) % len(points)]
        list.append(graph.create_line((point.x, point.y), (next.x, next.y), fill=c, width=w))
    return list


def makefull(points, color=0):
    c = colors[color % len(colors)]
    return graph.create_polygon([(p.x, p.y) for p in points], fill=c)


def makefill(points, color=0, full=False):
    if (full):
        s = ""
    else:
        s = "gray50"
    c = colors[color % len(colors)]
    # print(colors,points)
    return graph.create_polygon([(p.x, p.y) for p in points], fill=c, stipple=s)


def number(id, point):
    graph.create_text((point.x, point.y), text=str(id))


def numcenter(id, points):
    number(id, sum(points, Point(0, 0)) / len(points))


def numbours(id, neighbours, points):
    m = sum(points, Point(0, 0)) / len(points)
    number(id, m)
    for i in range(len(neighbours)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        p = ((p1 + p2) / 2 + m) / 2
        number(neighbours[i] % len(order), p)


"""i = w.create_line(xy, fill="red")
w.coords(i, new_xy) # change coordinates
w.itemconfig(i, fill="blue") # change color

w.delete(i) # remove"""


class Poly:
    def __init__(self, id, points, color=None, full=False):
        self.n = []
        self.id = id
        self.points = points
        realid = id % len(order)
        if (full):
            self.pid = makefull(points, color)
        elif (color == None):
            self.pid = make(points, (int((id - realid) / len(order))) % len(colors))
        else:
            self.pid = make(points, color % len(colors))
        # print(points)
        number(realid, sum(points, Point(0, 0)) / len(points))

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

    def remplis(self, color="red"):
        graph.create_polygon([(p.x, p.y) for p in self.points], fill=color, stipple="gray50")

    def __repr__(self):
        return str(self.points)

    def center(self):
        return centerpoint(self.points)


def get_face_points(p1, p2, face, noisy=True):
    faceid = face % len(order)
    if (len(shape[faceid])) == 3:
        points = triangle(p1, p2)
        if (noisy): print(" triangle ", face)
    elif (len(shape[faceid])) == 4:
        points = square(p1, p2)
        if (noisy): print(" square ", face)
    else:
        points = hexagon(p1, p2)
        if (noisy): print(" hexagon ", face)
    return points


def visualise(p1, p2, newshape, oldshape, color=0, drawnshapes=None, shapespoly=None, fill=True):
    # Copy of extend, but fills the whole space
    realshape = newshape % len(order)
    if (drawnshapes == None):
        drawnshapes = list()
    print("Visualise---------",newshape,oldshape,"(%s)"%realshape,shape[realshape])
    if (shapespoly == None):
        shapespoly = list()
    points = get_face_points(p1, p2, newshape, False)
    shapespoly.append(Poly(newshape, points, color, fill))
    current = shape[realshape]
    print(current, 'of shape', realshape, ', coming from', oldshape)
    index = current.index(oldshape)
    current = current[index:] + current[:index]
    shapespoly[-1].fill(current)
    drawnshapes.append(realshape)

    root.update()
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



def extend(p1, p2, newshape, oldshape=None, drawnshapes=None, shapespoly=None):
    # Visualize one tile and the neighbouring infos
    if (drawnshapes == None):
        drawnshapes = list()
    if (shapespoly == None):
        shapespoly = list()
    print(end="Draw the")
    realshape = newshape % len(order)
    if (len(shape[realshape])) == 3:
        points = triangle(p1, p2)
        print(" triangle ", newshape, "(%d)"%realshape)
    elif (len(shape[realshape])) == 4:
        points = square(p1, p2)
        print(" square ", newshape, "(%d)"%realshape)
    else:
        points = hexagon(p1, p2)
        print(" hexagon ", newshape, "(%d)"%realshape)

    shapespoly.append(Poly(newshape, points))
    current = shape[realshape]
    if (oldshape != None and newshape == realshape):
        print(oldshape,"in",current,newshape,realshape)
        index = current.index(oldshape)
        current = current[index:] + current[:index]
        print("Previous:", oldshape, "Next:", current)
    shapespoly[-1].fill(current)
    drawnshapes.append(newshape)

    root.update()
    # sleep(0.1)
    # print("I have",len(points),"points")
    if (newshape == realshape):
        for index, p in enumerate(current):
            # print(index)
            p1 = points[index % len(points)]
            p2 = points[(index + 1) % len(points)]
            if not p in drawnshapes or p == newshape and not (newshape != p and p == oldshape):
                ###[TODO] ici pose problème de retourner à même shape
                # print(p,shapes)
                # print("Work",newshape)
                if (p == newshape):
                    p += len(order)
                extend(p2, p1, p, newshape, drawnshapes, shapespoly)


def point_outside(point):
    x, y = point.x, point.y
    if (x < 0 or y < 0 or x > WIDTH or y > HEIGHT):
        return True


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


def fill_screen(p1, p2, newshape, oldshape=None, exploredpoints=None, drawnpoly=None, color=None):
    global tempshape

    if (exploredpoints == None):
        exploredpoints = list()
    if (drawnpoly == None):
        drawnpoly = list()
    realshape = newshape % len(order)
    if (realshape != newshape):
        print("Erreur de paramètre....", realshape, newshape)
    points = get_face_points(p1, p2, newshape, False)
    # Poly(newshape,points)
    if (points_outside(points)):
        return
    if (centerpoint(points) in exploredpoints):
        return
    """for face in exploredpoints:
		if(centerpoint(face)==centerpoint(points)):
			return
		else:

			if(len(points)==len(face)):
				print("Compare",centerpoint(face),"and",centerpoint(points))"""
    """
				d=0
				for i in range(len(points)):
					d+=(face[i]-points[i]).length()
				print(d)
				if(d<len(points)*5):
					print("This",sorted(rounded(face)),"and this",sorted(rounded(points)))"""
    # print("FINISHED")
    for elem in tempshape:
        graph.delete(elem)
    # tempshape = make(points,0)
    exploredpoints.append(centerpoint(points))
    current = shape[realshape]
    print("Oldshape:",oldshape)
    if (oldshape == None):
        oldshape = -current[0] + 2 * (current[0] % len(order))
    # if(oldshape!=None and newshape==realshape): #on explore même quand on est dehors
    # print(oldshape,"in",current,newshape,realshape)
    print(current, "of shape", realshape, "coming from", oldshape,flush=True)
    index = current.index(oldshape)
    current = current[index:] + current[:index]
    # print("Previous:",oldshape,"Next:",current)
    root.update()
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
            c = randint(0, len(colors) - 2)
            drawnpoly += visualise(p1, p2, newshape, oldshape, c, fill=True)
        else:
            visualise(p1, p2, newshape, oldshape, color, fill=False)
        print("Drawn")
    # print(drawnpoly[-1])
    # color+=1
    # print("Finished drawing")
    for index, p in enumerate(current):
        # print(index)
        p1 = points[index % len(points)]
        p2 = points[(index + 1) % len(points)]
        """if not p in drawnshapes or p==newshape and not (newshape != p and p==oldshape):
			###[TODO] ici pose problème de retourner à même shape
			#print(p,shapes)
			#print("Work",newshape)
			if(p==newshape):
				p+=len(order)"""
        # print("Do I explore ",realshape," to ",p,"(",p%len(order),") ?")
        if ((p % len(order) == p) and (p % len(order) != realshape)):
            # sleep(0.5)
            # print("Yes")
            #print(newshape - rest(p))
            fill_screen(p2, p1, real(p), newshape - rest(p), exploredpoints, drawnpoly, color)

    for index, p in enumerate(current):
        # print(index)
        p1 = points[index % len(points)]
        p2 = points[(index + 1) % len(points)]
        """if not p in drawnshapes or p==newshape and not (newshape != p and p==oldshape):
			###[TODO] ici pose problème de retourner à même shape
			#print(p,shapes)
			#print("Work",newshape)
			if(p==newshape):
				p+=len(order)"""
        if ((p % len(order) != p) or p % len(order) == realshape):
            # sleep(0.5)
            # color+=1
            #print(newshape,p,rest(p))
            #print(newshape + rest(p))
            fill_screen(p2, p1, real(p), newshape - rest(p), exploredpoints, drawnpoly, color)


"""
Two things:
the face, and the orientation
The orientation = current face (its shape) and order

For example, we went 2-3 on the net, and 4-1 on the shape

So on face 3, if face 3 is 2,4,6, we note, 4,X,X (the important part is the 4 at the beginning of the 1 face, matching the order in face 3)
We re-order them from the smallest face, so that it always matches

Same orientation as beginning: fill the normal set
Then go into a new set: until meet an orientation that we already met before, then stop


Algo:
If orientation is not in face
	Add orientation in face (and draw it)
	Try out possible rolls (same shape, adjacent)
else:
	found (draw it differently)
"""



def big_explore(p1, p2, case, face):
    global big_orientation
    global starting_area
    global small_orientation
    global all_points
    global current_cursor
    current_cursor = []
    starting_area = set()
    big_orientation = set()
    small_orientation = set()
    all_points = set()
    print(case,face,net[case])
    polys = visualise(p1, p2, case, net[case][0], color=3)
    for poly in polys:
        starting_area.add(poly.center())
    while (exploreA(p1, p2, case, face)):
        small_orientation = set()
    print("Finished exploring the area")


def exploreA(p1, p2, case, face, previouscase=None, previousface=None):
    # copy of explore, try to fill in whole shapes
    # print("Exploring",previouscase,"to",case,"with face",previousface,"to",face)
    if (previouscase not in net[case] and previouscase != None):
        if (previouscase % len(net) - (previouscase - (previouscase % len(net))) in net[case]):
            previouscase = previouscase % len(net) - (previouscase - (previouscase % len(net)))
            print("Had to fix this part for J8...")
    # else same shape
    if (len(roll[face]) == 3):
        points = triangle(p1, p2)
    # print("triangle de",face,"venant de",previousface)
    elif (len(roll[face]) == 4):
        points = square(p1, p2)
    # print("carré",face,"venant de",previousface)
    else:
        points = hexagon(p1, p2)

    for c in current_cursor:
        graph.delete(c)
    current_cursor[:] = []

    if (len(net[case]) != len(roll[face])):
        # print(current_cursor,points)
        current_cursor.extend(make(points, -3))

        current_cursor.append(makefill(points, color=-3))
        # different shapes: incompatible
        return False

    currentCaseNeighbours = net[case]
    currentFaceNeighbours = roll[face]
    # print(currentCaseNeighbours,currentFaceNeighbours)
    orientation = currentFaceNeighbours
    if (previouscase != None):
        # décalage : previouscase n'est pas le bas, le bas réel l'est: on fait l'inverse de la rotation pour qu'elle y soit
        # print(currentCaseNeighbours)
        caseOrientation = currentCaseNeighbours.index(previouscase)  # décalage actuel par rapport à la normale
        # print("Orientation de case:",caseOrientation)
        # points = points[caseOrientation:]+points[:caseOrientation]
        currentCaseNeighbours = currentCaseNeighbours[caseOrientation:] + currentCaseNeighbours[:caseOrientation]

        # décalage : previousface doit être le bas: on fait une rotation pour qu'elle y soit
        faceOrientation = currentFaceNeighbours.index(previousface)
        # décalage: la face du bas doit être la même que celle de l'orientation que la case
        # faceOrientation = (faceOrientation - caseOrientation)%len(order)
        currentFaceNeighbours = currentFaceNeighbours[faceOrientation:] + currentFaceNeighbours[:faceOrientation]
        # print(caseOrientation,faceOrientation)

        # print(currentCaseNeighbours,currentFaceNeighbours)
        orientation = currentFaceNeighbours
        # previouscase == previousface marche aussi
        # caseOrientation==faceOrientation ne marche que si les orientations par défaut sont les mêmes
        if (face == case and caseOrientation == faceOrientation and centerpoint(points) not in starting_area):
            if (centerpoint(points) not in big_orientation):

                polys = visualise(p1, p2, case, previouscase, color=1)
                ct = None
                for poly in polys:
                    ct = poly.center()
                    big_orientation.add(ct)
                # small_orientation.add(ct,currentFaceNeighbours)
                # instead of continuing, return and restart from beginning
                # so those orientations are a special case
                return False
            return False
    # print("My orientation is",orientation)
    cent = centerpoint(points)
    if (cent in big_orientation or (cent, tuple(orientation)) in small_orientation):
        # already visited this
        return False
        """if(orientation in orientations[case]):
		#already visited like this
		makefill(points,-1,True)
		make(points,2)
		numbours(case,currentCaseNeighbours,points)
		return"""
    elif (points_outside(points)):
        return False
    else:
        for c in current_cursor:
            graph.delete(c)
        current_cursor[:] = make(points)
        for pti in range(len(points)):
            pp1, pp2 = points[pti], points[(pti + 1) % len(points)]
            facesize = len(roll[currentFaceNeighbours[pti]])
            if (facesize == 3):
                current_cursor.extend(make(triangle(pp2, pp1), 6))
            elif (facesize == 4):
                current_cursor.extend(make(square(pp2, pp1), 6))
            elif (facesize == 6):
                current_cursor.extend(make(hexagon(pp2, pp1), 6))

        if (centerpoint(points) not in all_points):
            makefill(points, 1)
            make(points, 1)
            all_points.add(centerpoint(points))
        # numbours(case,currentCaseNeighbours,points)
        # orientations[case].append(orientation)
        small_orientation.add((cent, tuple(orientation)))
        for i in range(len(currentFaceNeighbours)):
            nextcasereal = currentCaseNeighbours[i]
            nextface = currentFaceNeighbours[i]
            p1 = points[i % len(points)]
            p2 = points[(i + 1) % len(points)]
            nextcase = nextcasereal % len(order)
            difference = nextcasereal - nextcase
            if (nextface != previousface):
                root.update()
                # sleep(0.75)
                # input()
                if (exploreA(p2, p1, nextcase, nextface, case - difference, face)):
                    return True



if __name__ == "__main__":
    #for shape_name in missing:
    #for shape_name in shapes_names:
    for shape_name in ["j10"]:
        global order
        global shape
        global shapes
        global shapespoly
        global roll
        global net
        roll = polys[shape_name]
        net = nets[shape_name]

        shape = net
        order = sorted(shape)
        shapes = []
        shapespoly = []
        graph.delete("all")
        visualise(p1, p2, 0, net[0][0], 2)

        sleep(2)
        print("EXTEND")	
        extend(p1,p2,order[0])
        sleep(2)
        graph.delete("all")
        fill_screen(p1,p2,order[0],color=None)
    
        #Commented to gain time
    
        root.update()
        sleep(2)


        graph.delete("all")
        print("#" * 30)
        # p2 = Point(330,300) #350 300
        big_explore(p1, p2, 0, 0)

        for c in current_cursor:
            graph.delete(c)
        current_cursor[:] = []
        root.update()
        # input()
        print("", flush=True)
        root.mainloop()
        exit()
    # sleep(2)

    # case = part of J1 net on which we are rolling
    # face = part of J1R polyhedron which is looking at the floor
    """
    orientations = dict()
    for face in roll:
        orientations[face] = []
    explore(p1,p2,0,0)
    print("Finished!")
    for face in sorted(orientations):
        print("orientations found for face",face,":", len(orientations[face]))
        print(orientations[face])
    """

    root.mainloop()
