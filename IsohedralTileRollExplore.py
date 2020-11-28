#from main import *
import DrawingFunctions as Draw
from GeometryFunctions import *
from PolyAndNets import *
from time import sleep
ext=10
P1=Point(300,300)
P2=Point(300,300+ext)
DEBUG1=True
def get_face_points(p1, p2, sides):
    if(sides==3):
        points = triangle(p1, p2)
    elif(sides==4):
        points = square(p1, p2)
    elif(sides==6):
        points = hexagon(p1, p2)
    else:
        print(sides,"---")
    return points


def centeroftilestarting(p1, p2, prev, current, tile):
    listofshapes = extend_tile(p1, p2, current, prev, tile)

    return centerpoint([Point(centerpoint(shape)) for shape in listofshapes])

def find_matching(previous, current, tile):
    # previous: old
    # current: outside
    # symetrical: next
    previous_real = previous % len(tile)
    current_real = current % len(tile)
    current_p = int((current - current_real) // len(tile))

    symetrical_side = tile[current_real]
    possible_matches = []
    for symetrical in symetrical_side:
        symetrical_real = symetrical % len(tile)
        symetrical_p = int((symetrical - symetrical_real) // len(tile))
        print(previous,current,current_p,symetrical_p)
        if (symetrical_real == previous_real):  # go to back same case
            if (symetrical_p == -current_p):  # matching p paired signs
                possible_matches = [(current_real, symetrical)]  # end it there
                break;
            if (symetrical_p == current_p):  # matching same sign p
                # but beware of side connected to itself more than once
                possible_matches.insert(0, (current_real, symetrical))  # put it first
            else:  # not matching, but maybe I made a mistake
                possible_matches.append((current_real, symetrical))  # put it last
    return possible_matches[0]
def find_matching_offset(previous,current,tile):
    current,sym = find_matching(previous,current,tile)
    return tile[current].index(sym)

def extend_tile(p1, p2, currentcase, oldcase, tile):
    # Copy of visualize
    visitedcases = []
    tilepoints = list()


    to_visit = [(p1,p2,currentcase,oldcase)]
    while(to_visit):
        p1,p2,currentcase,oldcase = to_visit.pop()
        realcurrent = currentcase % len(tile)
        visitedcases.append(realcurrent)
        points = get_face_points(p1, p2, len(tile[realcurrent]))
        if(DEBUG1):Draw.polygon_shape(points, (255,0,0), alpha=0.1, outline=1)
        if(DEBUG1):Draw.text_center(str(realcurrent),*centerpoint(points),(0,0,0),12)
        if(DEBUG1):Draw.refresh()
        #sleep(0.01)
        tilepoints.append(points)
        currentborder = tile[realcurrent] #print(currentborder, 'of shape', realcurrent, ', coming from', oldcase)
        base,match = find_matching(oldcase,currentcase,tile)
        if(DEBUG1):print(match)
        shift=currentborder.index(match) #index = current.index(-oldcase + 2 * (oldcase % len(order)))
        if(DEBUG1):print("Aligned on %d index %d"%(oldcase,shift))
        #print(index)
        currentborder = currentborder[shift:] + currentborder[:shift+1]
        for index, nextcase in enumerate(currentborder):
            p1 = points[index % len(points)]
            p2 = points[(index + 1) % len(points)]
            if (nextcase not in visitedcases) and (nextcase % len(tile) == nextcase):
                to_visit.append([p2,p1,nextcase, currentcase])
                if(DEBUG1):print("De %d, index %d next %d"%(realcurrent, index,nextcase))
        if(DEBUG1):input()
    return tilepoints


def create_neighbour_coordinates(tile):
    neighbours_coords = dict()
    explored = list()
    ####PART 1 : explore and list all neighbouring tiles
    to_explore = [list((P1,P2,0))]
    while(to_explore):
        initial_p1,initial_p2,case = to_explore.pop() #the initial shape from which the exploration starts
        initial_points=get_face_points(initial_p1,initial_p2,len(tile[case]))
        Draw.polygon_shape(initial_points, (0,255,0), alpha=1, outline=1)
        initial_points=initial_points+initial_points
        if(DEBUG1):Draw.text_center(str(case),*centerpoint(initial_points),(0,0,255),12)
        if(DEBUG1):Draw.refresh()
        explored.append(case)
        if(DEBUG1):input()
        for index,next in enumerate(tile[case]):
            if(next%len(tile)==next and next!=case):
                #inside the net (excluding self-ref which are outside)
                if(next not in explored):
                    #Branch out inside
                    branch_p1=initial_points[index]
                    branch_p2=initial_points[index+1]
                    branch_points = 2*get_face_points(branch_p2, branch_p1, len(tile[case])) #the direction of the segment has to be reversed
                    side_offset = len(tile[next])-tile[next].index(case) #inside net so no p offset
                    #branch_points triangle starts at [case] as its origin
                    #but next triangle loop considers starts at 0 (forgets previous)
                    #rotate the triangle so that the origin side is 0
                    next_p1, next_p2 = branch_points[side_offset:side_offset+2]
                    to_explore.append([next_p1,next_p2,next])
            else:
                #outside the net= neighbour data
                branch_p1=initial_points[index]
                branch_p2=initial_points[index+1]
                #branch_points = 2*get_face_points(branch_p2, branch_p1, len(tile[case])) #the direction of the segment has to be reversed
                #side_offset = len(tile[next%len(tile)])-index#len(tile[next%len(tile)])-find_matching_offset(case,next,tile)
                #next_p1, next_p2 = branch_points[side_offset:side_offset+2]
                if(DEBUG1):print("Going outside: %d to %d index %d"%(case,next%len(tile),index))
                neighbour = centeroftilestarting(branch_p2,branch_p1,case,next,tile)
                neighbours_coords.setdefault(neighbour,[])
                neighbours_coords[neighbour].append((case,next))
    del explored

    ####PART 2 : look up how the neighbouring tiles connect with the main tile
    """
    Paires a b

    Priorité matching (parce que je n'ai pas été constant dans mes notations):
    (a kp) et b -kp
    (a kp) et b kp
    (a kp) et b np (includes n=0)
    pas de paire trouvée (mauvais input)"""
    print(neighbours_coords)
    print("How many neighbours? :",len(neighbours_coords))
    neighbours_matches = dict()
    for neighbour in neighbours_coords:
        initials = list()
        matches = list()
        #case = old
        #outside = current
        #symmetrical = next
        #match old and next from current
        for case_initial, outside in neighbours_coords[neighbour]:
            initials.append((case_initial,outside))
            possible_match = find_matching(case_initial,outside,tile)
            matches.append(possible_match) #if no match, this is bad       initials.sort()
        matches.sort()
        neighbours_matches[neighbour]=(initials,matches)

    ####PART 3 : create a coordinates system based on how they connect
    # conway criterion for isohedral tiling

    pair_axis = dict()
    #pair_axis[current_case,next_case] = axis, sign, inverter

    dimension = 0
    known_matches = list()
    known_dimensions = list()
    for n,neighbour in enumerate(neighbours_matches):
        initials, matches = neighbours_matches[neighbour]
        print(initials,matches)
        print(known_dimensions,known_matches)
        if(initials==matches):
            #paired neighbour is same neighbour: central symetry
            for pair in initials:
                #axis, sign, invert
                pair_axis[pair]=dimension,+1,True
            dimension+=1
        else:
            if(initials in known_matches):
                #the starting point matches another's ending point
                #paired eighbour is opposite direction
                dim = known_dimensions[known_matches.index(initials)]
                for pair in initials:
                    #axis, sign, invert
                    pair_axis[pair]=dim,-1,False
            else:
                #A new dimension
                known_matches.append(matches)
                known_dimensions.append(dimension)
                for pair in initials:
                    #axis, sign, invert
                    pair_axis[pair]=dimension,+1,False
                dimension+=1

    return pair_axis, dimension

def explore_rotations(tile,poly):
    Draw.initialise_drawing(640,640)
    Draw.empty_shapes()
    #Draw.polygon_shape((Point(0,0),Point(150,0),Point(150,150)), (255,0,0), alpha=1, outline=1)
    startcase = 0
    startface = 0
    face_ori = 0
    case_ori = 0
    #extend_tile(Point(300,300),Point(300,310),0,tile[0][0],tile)
    axis,dim = create_neighbour_coordinates(tile)
    print(axis)
    print(dim)
    if(DEBUG1):Draw.loop()

if __name__ == "__main__":
    explore_rotations(nets["cube"],polys["cube"])


#Usage:
#have a tuple of size dimension "pos", and a sign modifier "sign_modif"=1
#for each out-of-tile move, look up dim,sign,invert = pair_axis[(current,next)]
#pos[dim]+=sign*sign_modif
#if(invert): sign_modif=-sign_modif