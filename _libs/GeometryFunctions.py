from math import pi
from _libs.RollyPoint import RollyPoint


def pointAngle(a, b, c):
    # Course formula: [AB]x[BC] product
    return ((b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x))

def ptAngle(a, b, c):
    # Course formula: [AB]x[BC] product
    return ((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0]))
def ptAdd(a,b):
    return a[0]+b[0],a[1]+b[1]
def ptSub(a,b):
    return a[0]-b[0],a[1]-b[1]

def psign(number):
    return (number >= 0) * 2 - 1


def is_inside(point, points):
    initial_sign = psign(pointAngle(point, points[-1], points[0]))
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        angle = pointAngle(point, p1, p2)
        if (psign(angle) != initial_sign):
            return False
    return True


def floatcenterpoint(points):
    mx = 0
    my = 0
    for x, y in points:
        mx += x
        my += y
    return (((mx / len(points))), ((my / len(points))))

def centerpoint(points):
    mx = 0
    my = 0
    for x, y in points:
        mx += x
        my += y
    return (int(round(mx / len(points))), int(round(my / len(points))))

def distance(p1,p2):
    x,y = p1
    xx,yy = p2
    return ((x-xx)**2+(y-yy)**2)**0.5

def square(p1, p2):
    # creates a rectangle clockwise to p1,p2
    p1 = p1
    p2 = p2

    p34 = p1 - p2
    p3 = p2 + RollyPoint(p34.y, -p34.x)
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


def pentagon(p1, p2):
    # creates a hexagon clockwise to p1,p2
    # precision decreases as points are added to eachother
    p1 = p1
    p2 = p2
    sol = [(p1), (p2)]
    pa = p1
    pb = p2
    for i in range(3):
        pn = pb + (pa - pb).rotate(-108 * pi / 180)
        sol.append((pn))
        pa = pb
        pb = pn
    return sol

def hexagon(p1, p2):
    # creates a hexagon clockwise to p1,p2
    # precision decreases as points are added to eachother
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

def octagon(p1, p2):
    # creates an octagon clockwise to p1,p2
    # precision decreases as points are added to eachother
    p1 = p1
    p2 = p2
    sol = [(p1), (p2)]
    pa = p1
    pb = p2
    for i in range(6):
        pn = pb + (pa - pb).rotate(-3 * pi / 4)
        sol.append((pn))
        pa = pb
        pb = pn
    return sol


def decagon(p1, p2):
    # creates a dodecagon clockwise to p1,p2
    # precision decreases as points are added to eachother
    p1 = p1
    p2 = p2
    sol = [(p1), (p2)]
    pa = p1
    pb = p2
    for i in range(8):
        pn = pb + (pa - pb).rotate(-144 * pi / 180)
        sol.append((pn))
        pa = pb
        pb = pn
    return sol

def dodecagon(p1, p2):
    # creates a dodecagon clockwise to p1,p2
    # precision decreases as points are added to eachother
    p1 = p1
    p2 = p2
    sol = [(p1), (p2)]
    pa = p1
    pb = p2
    for i in range(10):
        pn = pb + (pa - pb).rotate(-5 * pi / 6)
        sol.append((pn))
        pa = pb
        pb = pn
    return sol

xname = (None, None, None, "triangle", "square", None, "hexagon", None, "octagon", None, None, None, "dodecagon")
def xgon(sides,p1,p2):
    #not ngon because limited to some only
    try:
        return (None, None, None, triangle, square, pentagon, hexagon, None, octagon, None, decagon, None, dodecagon)[sides](p1,p2)
    except Exception as e:
        print("Asked to make",sides)
        raise e


def roundedcenter(polygon,precision):
    ccenter = tuple(floatcenterpoint(polygon))
    ccenter = int(round(ccenter[0] / precision) * precision), int(round(ccenter[1] / precision) * precision)
    return ccenter