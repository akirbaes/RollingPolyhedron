from main import *

def get_face_points(p1, p2, sides):
    if(len(sides)==3):
        points = triangle(p1, p2)
    elif(len(sides)==4):
        points = square(p1, p2)
    elif(len(sides)==6):
        points = hexagon(p1, p2)
    return points


def centeroftilestarting(p1, p2, prev, current):
    listofshapes = visualise(p1, p2, current, prev)
    return centerpoint([Point(shape.center) for shape in listofshapes])


def create_neighbour_coordinates(tile):
    neighbours_coords = dict()
    explored = list()
    ####PART 1 : explore and list all neighbouring tiles
    to_explore = list((Point(0,0),Point(0, 100),0))
    while(to_explore):
        initial_p1,initial_p2,case = to_explore.pop() #the initial shape from which the exploration starts
        initial_points=2*get_face_points(initial_p1,initial_p2,len(tile[case]))
        explored.append(case)
        for index,next in enumerate(tile[case]):
            if(next%len(tile)==next and next!=case):
                #inside the net (excluding self-ref which are outside)
                if(next not in explored):
                    #Branch out inside
                    branch_p1=initial_points[index]
                    branch_p2=initial_points[index+1]
                    branch_points = 2*get_face_points(branch_p1, branch_p2, len(tile[case]))
                    side_offset = len(tile[next])-tile[next].index(case) #inside net so no p offset
                    #branch_points triangle starts at [case] as its origin
                    #but next triangle loop considers starts at 0 (forgets previous)
                    #rotate the triangle so that the origin side is 0
                    next_p1, next_p2 = branch_points[side_offset:side_offset+2]
                    to_explore.append(next_p1,next_p2,next)
            else:
                #outside the net= neighbour data
                branch_p1=initial_points[index]
                branch_p2=initial_points[index+1]
                neighbour = centeroftilestarting(branch_p1,branch_p2,case,next)
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

    neighbours_matches = dict()
    for neighbour in neighbours_coords:
        initials = list()
        matches = list()
        for case_initial, outside in neighbours_coords[neighbour]:
            initials.append((case_initial,outside))

            outside_initial = outside%len(tile)
            outside_p = int((outside-outside_initial)//len(tile))

            symetrical_side = tile[outside_initial]
            possible_matches = []
            for symetrical in symetrical_side:
                symetrical_initial = symetrical%len(tile)
                symetrical_p = int((symetrical-symetrical_initial)//len(tile))
                if(symetrical_initial==case_initial): #go to back same case
                    if(symetrical_p == -outside_p): #matching p paired signs
                        possible_matches=[(outside_initial,symetrical)]#end it there
                        break;
                    if(symetrical_p == outside_p): #matching same sign p
                        #but beware of side connected to itself more than once
                        possible_matches.insert(0,(outside_initial,symetrical))#put it first
                    else: #not matching, but maybe I made a mistake
                        possible_matches.append((outside_initial,symetrical))   #put it last
            matches.append(possible_matches[0]) #if no match, this is bad       initials.sort()
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
#Usage:
#have a tuple of size dimension "pos", and a sign modifier "sign_modif"=1
#for each out-of-tile move, look up dim,sign,invert = pair_axis[(current,next)]
#pos[dim]+=sign*sign_modif
#if(invert): sign_modif=-sign_modif