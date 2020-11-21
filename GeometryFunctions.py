from math import pi
from Point import Point
def pointAngle(a, b, c):
    # Course formula: [AB]x[BC] product
    return ((b.x - a.x) * (c.y - b.y) - (b.y - a.y) * (c.x - b.x))
def psign(number):
    return (number>=0)*2-1

def is_inside(point,points):
    initial_sign = psign(pointAngle(point,points[-1],points[0]))
    for i in range(len(points)-1):
        p1=points[i]
        p2=points[i+1]
        angle=pointAngle(point,p1,p2)
        if(psign(angle)!=initial_sign):
            return False
    return True

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

