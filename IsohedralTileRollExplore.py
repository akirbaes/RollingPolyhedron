#from main import *
import DrawingFunctions as Draw
from GeometryFunctions import *
from PolyAndNets import *
from time import sleep
import pprint
pp = pprint.PrettyPrinter(indent=4)
ext=60
P1=Point(300,150)
P2=Point(300,150+ext)
WIDTH=800
HEIGHT=1000
DEBUG1=True
DEBUG2=False
DEBUG3=False
DEBUG4=False

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


def centeroftilestarting(p1, p2, prev, current, tile,draw=0):
    listofshapes = extend_tile(p1, p2, current, prev, tile)
    if(draw):
        #for shape in listofshapes:
        #    print("Centeroftiles using shape:",sorted([(p.x,p.y) for p in shape]))
        #    print(centerpoint(shape))
        #    Draw.text_center("o",*centerpoint(shape),(0,0,255),20)
        if(DEBUG4):print("Shapes received from extend:",len(listofshapes))
        if(DEBUG4):print("Coordinates of shapes used:")
        if(DEBUG4):print(sorted(centerpoint(shape) for shape in listofshapes))
        if(DEBUG4):print("big average:")
        if(DEBUG4):print(centerpoint([Point(centerpoint(shape)) for shape in listofshapes]))
    return centerpoint([Point(centerpoint(shape)) for shape in listofshapes])

def find_match(previous, current, tile):
    """Paires a b

    Priorité matching (parce que je n'ai pas été constant dans mes notations):
    (a kp) et b -kp
    (a kp) et b kp
    (a kp) et b np (includes n=0)
    pas de paire trouvée (mauvais input)"""
    p = len(tile)
    match = None
    try:
        match = tile[current].index(-previous + 2 * (previous % p))
    except:
        try:
            match = tile[current].index(previous)
        except:
            try:
                for index,case in enumerate(tile[current]):
                    if(case%p==current%p):
                        match = index
                        break;
            except:
                pass
    return match


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
        if(DEBUG1):print(previous,current,current_p,symetrical_p)
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
    #Previously a simple:
    # index = current.index(-oldcase + 2 * (oldcase % len(order)))
    #But now I want to be sure
    current,sym = find_matching(previous,current,tile)
    return tile[current].index(sym)

def extend_tile(p1, p2, currentcase, oldcase, tile):
    # Copy of visualize
    visitedcases = [currentcase%len(tile)]
    tilepoints = list()
    to_visit = [(p1,p2,currentcase,oldcase)]
    while(to_visit):
        p1,p2,currentcase,oldcase = to_visit.pop()
        realcurrent = currentcase % len(tile)
        #visitedcases.append(realcurrent) #too late! if two cases go to the same case that doesn't get explored until after
        points = get_face_points(p1, p2, len(tile[realcurrent]))
        if(DEBUG1):Draw.polygon_shape(points, (255,0,0), alpha=0.1, outline=1)
        if(DEBUG4):print("Extend",currentcase)
        if(DEBUG4):print(visitedcases)
        if(DEBUG1):Draw.text_center(str(realcurrent),*centerpoint(points),(0,0,0),12)
        if(DEBUG1):Draw.refresh()
        #sleep(0.01)
        tilepoints.append(points)
        currentborder = tile[realcurrent] #print(currentborder, 'of shape', realcurrent, ', coming from', oldcase)
        base,match = find_matching(oldcase,currentcase,tile)
        #if(DEBUG1):print(match)
        shift=currentborder.index(match) #index = current.index(-oldcase + 2 * (oldcase % len(order)))
        #if(DEBUG1):print("Aligned on %d index %d"%(oldcase,shift))
        #print(index)
        currentborder = currentborder[shift:] + currentborder[:shift+1]
        for index, nextcase in enumerate(currentborder):
            p1 = points[index % len(points)]
            p2 = points[(index + 1) % len(points)]
            if (nextcase not in visitedcases) and (nextcase % len(tile) == nextcase):
                to_visit.append([p2,p1,nextcase, currentcase])
                visitedcases.append(nextcase)
                #if(DEBUG1):print("De %d, index %d next %d"%(realcurrent, index,nextcase))
        if(DEBUG1 or DEBUG4):Draw.wait_for_input()
    return tilepoints


def get_neighbours_positions(tile,p1=P1,p2=P2,startcase=0,recurse=0):
    neighbours_coords = dict()
    if(recurse):
        neighbours_neighbours = dict()
        if(DEBUG4):
            nn_debug=dict()
    explored = list()
    ####PART 1 : explore and list all neighbouring tiles
    to_explore = [list((p1,p2,startcase))]
    while(to_explore):
        initial_p1,initial_p2,case = to_explore.pop() #the initial shape from which the exploration starts
        if(recurse):
            c=centeroftilestarting(initial_p1,initial_p2,tile[case%len(tile)][0],case,tile,1)
            if(DEBUG4):
                print("Center received",c)
                Draw.text_center("_0_",*c,(128,0,0),30)
        initial_points=get_face_points(initial_p1,initial_p2,len(tile[case]))
        if(DEBUG1):Draw.polygon_shape(initial_points, (0,255*recurse,0), alpha=.5, outline=1)
        initial_points=initial_points+initial_points
        if(DEBUG1):Draw.text_center(str(case),*centerpoint(initial_points),(0,0,255),12)
        if(DEBUG1):Draw.refresh()
        explored.append(case)
        if(DEBUG1):Draw.wait_for_input()
        for index,next in enumerate(tile[case]):
            branch_p1=initial_points[index]
            branch_p2=initial_points[index+1]
            branch_points = 2*get_face_points(branch_p2, branch_p1, len(tile[next%len(tile)])) #the direction of the segment has to be reversed
            #branch_points triangle starts at [case] as its origin
            #but next triangle loop considers starts at 0 (forgets previous)
            #rotate the triangle so that the origin side is 0
            if(next%len(tile)==next and next!=case):
                side_offset = len(tile[next])-tile[next].index(case)
                next_p1, next_p2 = branch_points[side_offset:side_offset+2]
                #inside the net (excluding self-ref which are outside)
                if(next not in explored):
                    #Branch out inside
                    to_explore.append([next_p1,next_p2,next])
            else:
                #outside the net= neighbour data
                branch_p1=initial_points[index]
                branch_p2=initial_points[index+1]
                #branch_points = 2*get_face_points(branch_p2, branch_p1, len(tile[case])) #the direction of the segment has to be reversed
                #side_offset = len(tile[next%len(tile)])-index#len(tile[next%len(tile)])-find_matching_offset(case,next,tile)
                #next_p1, next_p2 = branch_points[side_offset:side_offset+2]
                if(DEBUG1):print("Going outside: %d to %d index %d"%(case,next%len(tile),index))
                neighbour = centeroftilestarting(branch_p2,branch_p1,case,next,tile) #this takes prev tile so no shift
                neighbours_coords.setdefault(neighbour,[])
                neighbours_coords[neighbour].append((case,next))

                if(recurse):
                    #current, sym = find_matching(case,next,tile)
                    side_offset = len(tile[next%len(tile)])-find_matching_offset(case,next,tile)
                    next_p1, next_p2 = branch_points[side_offset:side_offset+2]
                    nn = get_neighbours_positions(tile,next_p1,next_p2,next%len(tile),recurse=False)
                    for n in nn:
                        nn[n].sort()
                    if DEBUG4:
                        debug_data = (next_p1,next_p2,next%len(tile))
                        if(neighbour in neighbours_neighbours):
                            if(neighbours_neighbours[neighbour]!=nn):
                                print("Not matching when reading neighbour",neighbour,"'s neighbours from two different sides:\nOriginal:")
                                print(nn_debug[neighbour])
                                pp.pprint(neighbours_neighbours[neighbour])
                                print("New: (coming from %d to %d)"%(case,next))
                                print(debug_data)
                                pp.pprint(nn)
                        nn_debug.setdefault(neighbour,debug_data)
                    neighbours_neighbours.setdefault(neighbour, nn)
    del explored
    if(recurse):
        return neighbours_coords,neighbours_neighbours
    return neighbours_coords
def create_neighbour_coordinates(tile):
    neighbours_coords,neighbours_neighbours=get_neighbours_positions(tile,P1,P2,0,recurse=1)
    ####PART 2 : look up how the neighbouring tiles connect with the main tile
    if(DEBUG2):print("Neighbour coords:",neighbours_coords)
    if(DEBUG2):print("How many neighbours? :",len(neighbours_coords))

    center_coord=centeroftilestarting(P1,P2,tile[0][0],0,tile)
    print("Center:",center_coord)
    neighbours_matches = dict()

    for n in neighbours_neighbours:
        pp.pprint(n)
        pp.pprint(neighbours_neighbours[n])
    for n in neighbours_coords:
        print(n)
        print(neighbours_coords[n])
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
            #if(DEBUG2):print((case_initial,outside),possible_match)
            matches.append(possible_match) #if no match, this is bad       initials.sort()
        initials.sort()
        matches.sort()
        neighbours_matches[neighbour]=(initials,matches)
    print("Neighbours matches:", neighbours_matches)
    ####PART 3 : create a coordinates system based on how they connect
    # conway criterion for isohedral tiling
    if(DEBUG2):print("Neighbours matches:",neighbours_matches)
    pair_axis = dict()
    #pair_axis[current_case,next_case] = axis, sign, inverter

    dimension = 0
    known_matches = list()
    known_dimensions = list()
    print("Max dimensions:",len(neighbours_matches))
    for n,neighbour in enumerate(neighbours_matches):
        if(DEBUG2):print("------Neighbour %d------"%n)
        initials, matches = neighbours_matches[neighbour]
        if(DEBUG2):print("Comparing",initials,"and",matches)
        #if(DEBUG2):print(known_dimensions,known_matches)
        if(initials==matches):
            if(DEBUG2):print("Identical, adding a central symmetry dimension (%d)"%dimension)
            #paired neighbour is same neighbour: central symetry
            known_dimensions.append(dimension)
            known_matches.append(matches)
            for pair in initials:
                #axis, sign, invert
                pair_axis[pair]=dimension,+1,True
            dimension+=1
        else:
            if(DEBUG2):print("Different")
            if(DEBUG2):print("Looking for",initials,"in",known_matches)
            if(initials in known_matches):
                if(DEBUG2):print("Found")
                #the starting point matches another's ending point
                #paired eighbour is opposite direction
                dim = known_dimensions[known_matches.index(initials)]
                for pair in initials:
                    #axis, sign, invert
                    pair_axis[pair]=dim,-1,False
                if(DEBUG2):print("Found an existing dimension (%d)"%(dim))
            else:
                #A new dimension
                if(DEBUG2):print("Not found, new dimension (%d)" % dimension)
                known_matches.append(matches)
                known_dimensions.append(dimension)
                for pair in initials:
                    #axis, sign, invert
                    pair_axis[pair]=dimension,+1,False
                dimension+=1

    return pair_axis, dimension

import numpy as np
def is_known(cfo,tilecoord,positions, known_symmetries):
    #Solve linear equation with known symetries and return true if integer solution
    #If not integer,
    print("Entering is_known")
    known = positions[cfo] #tilecoords of same case, face, orientation reached
    for knowncoord in known:
        a = np.array(known_symmetries)
        b = np.array([tilecoord[i]-knowncoord[i] for i in range(len(tilecoord))])
        print(a)
        print(b)
        if(len(a)==len(b)):
            x = np.linalg.solve(a, b)
        else:
            x = np.linalg.lstsq(a, b, rcond=1)
        print(x)
        for c in x:
            if(int(c)!=c):
                print("Not a solution:",x)
                continue
        print(x,"is an integer solution! Known")
        return True

    return False

def add_new_symmetry(cfo,tilecoord,positions,known_symmetries):
    for existing_position in positions[cfo]:
        possible_symmetry = [tilecoord[i]-existing_position[i] for i in range(len(tilecoord))]
        known_symmetries.append(possible_symmetry)
    known_symmetries.append(tilecoord)
    positions[cfo].append(tilecoord)



def explore_rotations(tile,poly):
    if(DEBUG1 or DEBUG2 or DEBUG3 or 1):Draw.initialise_drawing(WIDTH,HEIGHT)
    if(DEBUG1 or DEBUG2 or DEBUG3):Draw.empty_shapes()
    #Draw.polygon_shape((Point(0,0),Point(150,0),Point(150,150)), (255,0,0), alpha=1, outline=1)
    startcase = 0
    startface = 0
    face_ori = 0
    case_ori = 0
    #extend_tile(Point(300,300),Point(300,310),0,tile[0][0],tile)
    neighbour_coord,dim = create_neighbour_coordinates(tile)
    if(DEBUG2):print("-"*20)
    if(DEBUG2):print("Coordinate infos:",neighbour_coord)
    if(DEBUG2):print("Number of axes:",dim)
    for coord in sorted(neighbour_coord):
        if(DEBUG2):print(coord,":",neighbour_coord[coord])
    print(flush=True)
    positions = dict()
    symmetry_axis = list()
    for case in tile:
        for face in poly:
            for orientation in range(len(poly[face])):
                positions[(case,face,orientation)]=list()
    if(DEBUG3):print("Possible combinations: %d"%len(positions))

    pos = (P1,P2,0,0,0,[0 for x in range(dim)],1)
    to_explore = [pos]
    while(to_explore):
        p1,p2,case,face,orientation,tilecoord, tilecoordsign = to_explore.pop()
        #if(case%len(tile)!=case):
        #    continue
        #print("exploring",p1,p2,"case",case,"face",face,orientation,tilecoord, tilecoordsign )
        if(len(tile[case%len(tile)])!=len(poly[face])):
            continue
        #caseorientation = 0
        #orientation is tileorientation
        #print("Known positions for",case%len(tile),face,orientation)
        #print(positions[(case%len(tile),face,orientation)])
        if(tilecoord in positions[(case%len(tile),face,orientation)]):
            continue
        #if(not is_known((case,face,orientation),tilecoord,positions,symmetry_axis)):
        startpoints = get_face_points(p1,p2,len(poly[face]))
        color=Draw.colors[sum([abs(x*(n+1)) for n,x in enumerate(tilecoord)])%len(Draw.colors)]
        Draw.polygon_shape(startpoints,color,0.75,1)
        #Draw.text_center("%d/%d+%d"%(face,case%len(tile),(case-(case%len(tile)))//len(tile)),*centerpoint(startpoints),(255,255,255),int(ext/2))
        Draw.text_center(str(tilecoord)+str(tilecoordsign),*centerpoint(startpoints),(255,255,255),int(ext/4))
        #Draw.text_center("%d(%d)"%(case,(case-(case%len(tile)))//len(tile)),*centerpoint(startpoints),(255,255,255),int(ext/2))
        Draw.refresh()
        #Draw.wait_for_input()
        if(len(positions[(case%len(tile),face,orientation)])==0):
            #add_new_symmetry((case,face,orientation),tilecoord,positions,symmetry_axis)
            #Draw.wait_for_input()
            newcases = tile[case%len(tile)]
            faceshift = len(poly)-orientation
            newfaces = poly[face][orientation:]+poly[face][:orientation]
            if(DEBUG3):print(case%len(tile),newcases)
            if(DEBUG3):print(face%len(poly),newfaces)
            for i in range(len(newcases)):
                newface = newfaces[i]
                newcase = newcases[i]
                #if(newcase%len(tile)!=newcase):
                #    continue
                if(DEBUG3):print("index",i,"going to",newcase)
                if(len(tile[newcase%len(tile)])!=len(poly[newface])):
                    continue
                pa,pb=(startpoints*2)[i:i+2] #where to start to draw the new case
                branchpoints=get_face_points(pb,pa,len(poly[newface]))*2
                branchoffset = len(tile[newcase%len(tile)])-find_matching_offset(case,newcase,tile)
                p1p,p2p=branchpoints[branchoffset:branchoffset+2] #where to start the caseorientation=0
                newface_orientation = (poly[newface].index(face)+branchoffset)%len(poly[newface])
                newtilecoord = tilecoord.copy()
                newtilecoordsign=tilecoordsign
                if(newcase!=newcase%len(tile) or newcase==case):
                    #print("Neighbour moving",(case%len(tile),newcase),newcase%len(tile))
                    dim,increment,invertsign = neighbour_coord[(case%len(tile),newcase)]
                    newtilecoord[dim]+=increment*tilecoordsign
                    if(invertsign):
                        newtilecoordsign=-newtilecoordsign
                    #print(dim,increment,invertsign)
                    #print(tilecoord,tilecoordsign,"->",newtilecoord,newtilecoordsign)

                to_explore.append((p1p,p2p,newcase,newface,newface_orientation,newtilecoord,newtilecoordsign))
        positions[(case%len(tile),face,orientation)].append(tilecoord)
    if(DEBUG3):print(positions)
    if(DEBUG3):print("Done exploring everything!")
    if(DEBUG1 or DEBUG3):Draw.loop()
    Draw.wait_for_input()
    #Next: explore the space!

if __name__ == "__main__":
    explore_rotations(nets["j86"],polys["j86"])


#Usage:
#have a tuple of size dimension "pos", and a sign modifier "sign_modif"=1
#for each out-of-tile move, look up dim,sign,invert = pair_axis[(current,next)]
#pos[dim]+=sign*sign_modif
#if(invert): sign_modif=-sign_modif