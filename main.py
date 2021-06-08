"""Tileset visualiser by Akira Baes
A future version should interface with a tile-representation-generator directly

First, "extend" show the representation of a single tile with its neighbouring tiles infos

"fill_screen" then fill the screen with the given tile to verify that it is a tile

"explore" is supposed to find all the places that can be rolled into, with a stopping condition when reaching a position+orientation that has already been met,
but it is rather difficult to read to determine if it can roll in the space or not.

V1.1 I'm trying to look at one specific one in more details (hexagonal antiprism), but maximum recrsion depth gets in the way, must rewrite
But by symmetry, there is nothing exceptional to see, only that my algorithm stops too early before filling the screen.
V1.2 rewriting it in several files for pycharm
"""
from time import sleep
from GeometryFunctions import *
from sys import setrecursionlimit
import DrawingFunctions as Draw

setrecursionlimit(10 ** 4)
WIDTH = 800
HEIGHT = 800
EDGESIZE = 50
p1 = RollyPoint(300, 300)
p2 = RollyPoint(300 + EDGESIZE, 300)  # 350 300
textsize = int(round((EDGESIZE) / 2))

Draw.initialise_drawing(WIDTH, HEIGHT)
from PolyAndTessNets import polys

from PolyFunctions import RollyPoly, visualise, get_face_points, make_shape, make_cursor
from findPolySymmetries import canon_face, canon_fo, generate_FFOO_sym, generate_face_sym

"""
def number(id, point):
    # graph.create_text((point.x, point.y), text=str(id))
    Draw.text_center(str(id), point.x, point.y, (0, 0, 0), textsize)


def numcenter(id, points):
    number(id, sum(points, Point(0, 0)) / len(points))
"""

"""
def numbours(id, neighbours, points):
    print("Broken since the tiling sizes don't match anymore")
    m = sum(points, Point(0, 0)) / len(points)
    number(id, m)
    for i in range(len(neighbours)):
        p1 = points[i]
        p2 = points[(i + 1) % len(points)]
        p = ((p1 + p2) / 2 + m) / 2
        number(neighbours[i] % len(order), p)"""

from math import atan2
from math import pi


def extend(polydict, p1, p2, newshape, oldshape=None, drawnshapes=None, shapespoly=None, prints=False):
    # Visualize one tile and the neighbouring infos
    if (drawnshapes == None):
        drawnshapes = list()
    if (shapespoly == None):
        shapespoly = list()
    if(prints):print(end="Draw the")
    realshape = newshape % len(polydict)
    points = xgon(realshape)
    if(prints):print(" %s "%xname[realshape], newshape, "(%d)" % realshape)

    shapespoly.append(RollyPoly(newshape, points, 1, p=len(polydict)))
    current = polydict[realshape]
    if (oldshape != None and newshape == realshape):
        if(prints):print(oldshape, "in", current, newshape, realshape)
        index = current.index(oldshape)
        current = current[index:] + current[:index]
        if(prints):print("Previous:", oldshape, "Next:", current)
    shapespoly[-1].fill(current)
    drawnshapes.append(newshape)

    # sleep(0.1)
    # print("I have",len(points),"points")
    if (newshape == realshape):
        for index, s in enumerate(current):
            # print(index)
            p1 = points[index % len(points)]
            p2 = points[(index + 1) % len(points)]
            if not s in drawnshapes or s == newshape and not (newshape != s and s == oldshape):
                ###[TODO] ici pose problème de retourner à même shape
                # print(p,shapes)
                # print("Work",newshape)
                if (s == newshape):
                    s += len(polydict)
                extend(polydict, p2, p1, s, newshape, drawnshapes, shapespoly)

    Draw.refresh()


def point_outside(point):
    x, y = point.x, point.y
    if (x < 0 or y < 0 or x > WIDTH or y > HEIGHT):
        return True


def points_outside(points):
    for point in points:
        if (point_outside(point)):
            return True
    return False

"""
def swap(oldshape):
    return -oldshape + 2 * (oldshape % len(order))


def rest(oldshape):
    return oldshape - (oldshape % len(order))


def real(shape):
    return shape % len(order)"""


def rounded(pts):
    return tuple(round(x / 10) for x in pts)


from random import randint

tempshape = []


def fill_screen(tiling, p1, p2, newshape, oldshape=None, exploredpoints=None, drawnpoly=None, color=None, prints=False):
    global tempshape

    if (exploredpoints == None):
        exploredpoints = list()
    if (drawnpoly == None):
        drawnpoly = list()
    realshape = newshape % len(tiling)
    if (realshape != newshape):
        print("Erreur de paramètre....", realshape, newshape)
    points = get_face_points(tiling,p1, p2, newshape, noisy=False)

    if (points_outside(points)):
        return
    if (centerpoint(points) in exploredpoints):
        return

    exploredpoints.append(centerpoint(points))
    current = tiling[realshape]
    if(prints):print("Oldshape:", oldshape)
    if (oldshape == None):
        # Turns a n+P number into n-P (find pair)
        oldshape = -current[0] + 2 * (current[0] % len(tiling))
        # n%P - (n-n%P) = -n + 2*(n%P)

    # if(oldshape!=None and newshape==realshape): #on explore même quand on est dehors
    # print(oldshape,"in",current,newshape,realshape)
    if(prints):print(current, "of shape", realshape, "coming from", oldshape, flush=True)
    try:
        index = current.index(oldshape)
    except:
        # Maybe the -P +P formula is not respected
        index = current.index(-oldshape + 2 * (oldshape % len(tiling)))
        if(prints):print("Exception matching", oldshape % len(tiling), "+%dP" % (oldshape // len(tiling)))
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
            drawnpoly += visualise(tiling, p1, p2, newshape, oldshape, c, fill=False, prints=prints)
        else:
            visualise(tiling, p1, p2, newshape, oldshape, color, fill=False, prints=prints)
        #print("Drawn")
    # print(drawnpoly[-1])
    # color+=1
    # print("Finished drawing")
    for index, p in enumerate(current):
        # print(index)
        p1 = points[index % len(points)]
        p2 = points[(index + 1) % len(points)]
        # print("Do I explore ",realshape," to ",p,"(",p%len(order),") ?")
        if ((p % len(tiling) == p) and (p % len(tiling) != realshape)):
            fill_screen(tiling, p2, p1, p%len(tiling), newshape - (p-(p%len(tiling))), exploredpoints, drawnpoly, color, prints=prints)

    for index, p in enumerate(current):
        # print(index)
        p1 = points[index % len(points)]
        p2 = points[(index + 1) % len(points)]
        if ((p % len(tiling) != p) or p % len(tiling) == realshape):
            # sleep(0.5)
            # color+=1
            # print(newshape,p,rest(p))
            # print(newshape + rest(p))
            fill_screen(tiling, p2, p1, p%len(tiling), newshape - (p-(p%len(tiling))), exploredpoints, drawnpoly, color, prints=prints)


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

def big_explore(tiling, rolling, p1, p2, case, face,prints=False):
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
    if(prints):print(case, face, tiling[case])
    polys = visualise(tiling, p1, p2, case, tiling[case][0], color=3, fill=True, prints=prints)
    for poly in polys:
        starting_area.add(tuple(poly.center())) #already tuple
    while (exploreA(tiling, rolling, p1, p2, case, face,prints=prints)):
        small_orientation = set()
    print("Finished exploring the area")


screenshot_counter = 0


def exploreA(tiling, rolling, p1, p2, case, face, previouscase=None, previousface=None,prints=False):
    global screenshot_counter
    # Draw.save_screen("scrsh/%s%d.png"%(shape_name,screenshot_counter))
    screenshot_counter += 1
    # copy of explore, try to fill in whole shapes
    # print("Exploring",previouscase,"to",case,"with face",previousface,"to",face)
    if (previouscase not in tiling[case] and previouscase != None):
        if (previouscase % len(tiling) - (previouscase - (previouscase % len(tiling))) in tiling[case]):
            previouscase = previouscase % len(tiling) - (previouscase - (previouscase % len(tiling)))
            # print("Had to fix this part for J8...")
    # else same shape
    points = xgon(len(rolling[face]),p1,p2)
    Draw.refresh()
    Draw.empty_cursor()

    current_cursor[:] = []

    if (len(tiling[case]) != len(rolling[face])):
        # print(current_cursor,points)
        current_cursor.extend(make_cursor(points, -3, 0.7))

        # current_cursor.append(make_cursor(points, color=-3,fill=True))
        # different shapes: incompatible
        return False

    currentCaseNeighbours = tiling[case]
    currentFaceNeighbours = rolling[face]
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

        case_count, max_count = Draw.create_orientation_data(case, tiling)
        face_count, max_count = Draw.create_orientation_data(face, rolling)
        outline = 0
        if (face == case):
            if (faceOrientation == caseOrientation):
                outline = 1
                # white outline
            else:
                outline = 2
                # black outline
        if(prints):print(len(points))
        Draw.polygon_orientation(points, (0 - caseOrientation + faceOrientation - caseOrientation) % len(points),
                                 face_count, max_count, outline, case_count)

        # previouscase == previousface marche aussi
        # caseOrientation==faceOrientation ne marche que si les orientations par défaut sont les mêmes
        if (face == case and caseOrientation == faceOrientation and centerpoint(points) not in starting_area):
            if (centerpoint(points) not in big_orientation):

                polys = visualise(tiling, p1, p2, case, previouscase, color=1, fill=True,prints=prints)
                ct = None
                for poly in polys:
                    ct = poly.center()
                    big_orientation.add(tuple(ct))
                    all_points.add(tuple(ct))
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
    elif (points_outside(points)):
        return False
    else:
        if(prints):Draw.empty_cursor()

        current_cursor[:] = make_cursor(points, -2, filling=0.1)
        for pti in range(len(points)):
            pp1, pp2 = points[pti], points[(pti + 1) % len(points)]
            facesize = len(rolling[currentFaceNeighbours[pti]])
            if (facesize == 3):
                current_cursor.extend(make_cursor(triangle(pp2, pp1), -2, filling=0.1))
            elif (facesize == 4):
                current_cursor.extend(make_cursor(square(pp2, pp1), -2, filling=0.1))
            elif (facesize == 6):
                current_cursor.extend(make_cursor(hexagon(pp2, pp1), -2, filling=0.1))

        if (centerpoint(points) not in all_points):
            make_shape(points, 1, filling=0.5)
            all_points.add(tuple(centerpoint(points)))
        # numbours(case,currentCaseNeighbours,points)
        # orientations[case].append(orientation)
        small_orientation.add((cent, tuple(orientation)))
        for i in range(len(currentFaceNeighbours)):
            nextcasereal = currentCaseNeighbours[i]
            nextface = currentFaceNeighbours[i]
            p1 = points[i % len(points)]
            p2 = points[(i + 1) % len(points)]
            nextcase = nextcasereal % len(tiling)
            difference = nextcasereal - nextcase
            if (nextface != previousface):
                # root.update()
                # sleep(0.75)
                # input()
                if (exploreA(tiling, rolling, p2, p1, nextcase, nextface, case - difference, face)):
                    return True

from tilings_oldformat import *
if __name__ == "__main__":
    global shape_name
    global net
    global order
    # for shape_name in missing:
    # for shape_name in shapes_names:
    tiles = list(archimedeans)+list(platonics)
    for shape_name in ["hexagonal_antiprism"]:
        for tiling_name in ["3^4x6"]:
            global order
            global shape
            global shapes
            global tilecases
            global roll
            global net
            roll = polys[shape_name]
            #roll=polys["hexagonal_antiprism"]
            if (roll == None):
                continue
            #net = nets[shape_name]
            tiling = archimedeans[tiling_name]
            net = tiling
            shape = tiling
            order = sorted(shape)
            shapes = []
            tilecases = []
            Draw.empty_shapes()
            Draw.empty_cursor()
            Draw.refresh()
            #visualise(tiling, p1, p2, 0, net[0][0], 2)
            #Draw.refresh()
            #print("EXTEND")
            #sleep(2) ;
            #extend(p1,p2,order[0])
            # Draw.save_screen("net_%s.png" % shape_name)
            #Draw.refresh()
            #Draw.empty_shapes()
            #sleep(2) ;
            fill_screen(tiling,p1,p2,0,color=None) ;
            Draw.refresh()

            # Commented to gain time

            # Draw.empty_shapes()
            print("#" * 30)

            # p2 = Point(330,300) #350 300
            big_explore(tiling, roll, p1, p2, 0, 2)
            Draw.refresh()

            Draw.save_screen(shape_name+"_rolling_in_"+tiling_name+".png")
            Draw.refresh()
            sleep(1)
            # for c in current_cursor:
            #    graph.delete(c)
            Draw.empty_cursor()
            current_cursor[:] = []
            Draw.refresh()
            # input("Finished")
    print("Done!", flush=True)
    Draw.loop()
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
    # Draw.refresh()
