# from main import *
import os
import traceback

from _libs import DrawingFunctions as Draw
from _libs.GeometryFunctions import *
# from time import sleep
import pprint
from _resources.TessellationPolyhedronAndTilings import tessellation_polyhedrons, net_tessellations, tesspoly_order
for k in tesspoly_order:
    p=len(net_tessellations[k])
    for face,neighbours in net_tessellations[k].items():
        for i in range(len(neighbours)):
            neighbours[i] = neighbours[i][0]+p*neighbours[i][1]
    print(net_tessellations[k])
print(net_tessellations)

pp = pprint.PrettyPrinter(indent=4)
ext = 35
P1 = RollyPoint(300, 350)
P2 = RollyPoint(300, 350 + ext)
WIDTH = 800
HEIGHT = 1000
DEBUG1 = False
DEBUG2 = False
DEBUG3 = False
DEBUG4 = False
DEBUG5 = False
DEBUG6 = True
DEBUG7 = True


def get_face_points(p1, p2, sides):
    return xgon(sides,p1,p2)


def centeroftilestarting(p1, p2, prev, current, tile, draw=0):
    listofshapes = extend_tile(p1, p2, current, prev, tile)
    if draw:
        # for shape in listofshapes:
        #    print("Centeroftiles using shape:",sorted([(p.x,p.y) for p in shape]))
        #    print(centerpoint(shape))
        #    Draw.text_center("o",*centerpoint(shape),(0,0,255),20)
        if DEBUG4: print("Shapes received from extend:", len(listofshapes))
        if DEBUG4: print("Coordinates of shapes used:")
        if DEBUG4: print(sorted(centerpoint(shape) for shape in listofshapes))
        if DEBUG4: print("big average:")
        if DEBUG4: print(centerpoint([RollyPoint(centerpoint(shape)) for shape in listofshapes]))
    return centerpoint([RollyPoint(centerpoint(shape)) for shape in listofshapes])


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
                for index, case in enumerate(tile[current]):
                    if case % p == current % p:
                        match = index
                        break
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
        if DEBUG1: print(previous, current, current_p, symetrical_p)
        if symetrical_real == previous_real:  # go to back same case
            if symetrical_p == -current_p:  # matching p paired signs
                possible_matches = [(current_real, symetrical)]  # end it there
                break
            if symetrical_p == current_p:  # matching same sign p
                # but beware of side connected to itself more than once
                possible_matches.insert(0, (current_real, symetrical))  # put it first
            else:  # not matching, but maybe I made a mistake
                possible_matches.append((current_real, symetrical))  # put it last
    return possible_matches[0]


def find_matching_offset(previous, current, tile):
    # Previously a simple:
    # index = current.index(-oldcase + 2 * (oldcase % len(order)))
    # But now I want to be sure
    current, sym = find_matching(previous, current, tile)
    return tile[current].index(sym)


def extend_tile(p1, p2, currentcase, oldcase, tile):
    # Copy of visualize
    visitedcases = [currentcase % len(tile)]
    tilepoints = list()
    to_visit = [(p1, p2, currentcase, oldcase)]
    while to_visit:
        p1, p2, currentcase, oldcase = to_visit.pop()
        realcurrent = currentcase % len(tile)
        # visitedcases.append(realcurrent) #too late! if two cases go to the same case that doesn't get explored until after
        points = get_face_points(p1, p2, len(tile[realcurrent]))
        if DEBUG1: Draw.polygon_shape(points, (255, 0, 0), alpha=0.1, outline=1)
        if DEBUG4: print("Extend", currentcase)
        if DEBUG4: print(visitedcases)
        if DEBUG1: Draw.text_center(str(realcurrent), *centerpoint(points), (0, 0, 0), 12)
        if DEBUG1: Draw.refresh()
        # sleep(0.01)
        tilepoints.append(points)
        currentborder = tile[realcurrent]  # print(currentborder, 'of shape', realcurrent, ', coming from', oldcase)
        base, match = find_matching(oldcase, currentcase, tile)
        # if(DEBUG1):print(match)
        shift = currentborder.index(match)  # index = current.index(-oldcase + 2 * (oldcase % len(order)))
        # if(DEBUG1):print("Aligned on %d index %d"%(oldcase,shift))
        # print(index)
        currentborder = currentborder[shift:] + currentborder[:shift + 1]
        for index, nextcase in enumerate(currentborder):
            p1 = points[index % len(points)]
            p2 = points[(index + 1) % len(points)]
            if (nextcase not in visitedcases) and (nextcase % len(tile) == nextcase):
                to_visit.append([p2, p1, nextcase, currentcase])
                visitedcases.append(nextcase)
                # if(DEBUG1):print("De %d, index %d next %d"%(realcurrent, index,nextcase))
        if DEBUG1: Draw.wait_for_input()
    return tilepoints


def get_neighbours_positions(tile, p1=P1, p2=P2, startcase=0, recurse=0):
    neighbours_coords = dict()
    if recurse:
        neighbours_neighbours = dict()
        if DEBUG4:
            nn_debug = dict()
    explored = list()
    ####PART 1 : explore and list all neighbouring tiles
    to_explore = [list((p1, p2, startcase))]
    while to_explore:
        initial_p1, initial_p2, case = to_explore.pop()  # the initial shape from which the exploration starts
        if recurse:
            c = centeroftilestarting(initial_p1, initial_p2, tile[case % len(tile)][0], case, tile, 1)
            if DEBUG4:
                print("Center received", c)
                Draw.text_center("_0_", *c, (128, 0, 0), 30)
        initial_points = get_face_points(initial_p1, initial_p2, len(tile[case]))
        if DEBUG1: Draw.polygon_shape(initial_points, (0, 255 * recurse, 0), alpha=.5, outline=1)
        initial_points = initial_points + initial_points
        if DEBUG1: Draw.text_center(str(case), *centerpoint(initial_points), (0, 0, 255), 12)
        if DEBUG1: Draw.refresh()
        explored.append(case)
        if DEBUG1: Draw.wait_for_input()
        for index, next in enumerate(tile[case]):
            branch_p1 = initial_points[index]
            branch_p2 = initial_points[index + 1]
            branch_points = 2 * get_face_points(branch_p2, branch_p1, len(
                tile[next % len(tile)]))  # the direction of the segment has to be reversed
            # branch_points triangle starts at [case] as its origin
            # but next triangle loop considers starts at 0 (forgets previous)
            # rotate the triangle so that the origin side is 0
            if next % len(tile) == next and next != case:
                side_offset = len(tile[next]) - tile[next].index(case)
                next_p1, next_p2 = branch_points[side_offset:side_offset + 2]
                # inside the net (excluding self-ref which are outside)
                if next not in explored:
                    # Branch out inside
                    to_explore.append([next_p1, next_p2, next])
            else:
                # outside the net= neighbour data
                branch_p1 = initial_points[index]
                branch_p2 = initial_points[index + 1]
                # branch_points = 2*get_face_points(branch_p2, branch_p1, len(tile[case])) #the direction of the segment has to be reversed
                # side_offset = len(tile[next%len(tile)])-index#len(tile[next%len(tile)])-find_matching_offset(case,next,tile)
                # next_p1, next_p2 = branch_points[side_offset:side_offset+2]
                if DEBUG1: print("Going outside: %d to %d index %d" % (case, next % len(tile), index))
                neighbour = centeroftilestarting(branch_p2, branch_p1, case, next,
                                                 tile)  # this takes prev tile so no shift
                neighbours_coords.setdefault(neighbour, [])
                neighbours_coords[neighbour].append((case, next))

                if recurse:
                    # current, sym = find_matching(case,next,tile)
                    side_offset = len(tile[next % len(tile)]) - find_matching_offset(case, next, tile)
                    next_p1, next_p2 = branch_points[side_offset:side_offset + 2]
                    nn = get_neighbours_positions(tile, next_p1, next_p2, next % len(tile), recurse=False)
                    for n in nn:
                        nn[n].sort()
                    if DEBUG4:
                        debug_data = (next_p1, next_p2, next % len(tile))
                        if neighbour in neighbours_neighbours:
                            if neighbours_neighbours[neighbour] != nn:
                                print("Not matching when reading neighbour", neighbour,
                                      "'s neighbours from two different sides:\nOriginal:")
                                print(nn_debug[neighbour])
                                pp.pprint(neighbours_neighbours[neighbour])
                                print("New: (coming from %d to %d)" % (case, next))
                                print(debug_data)
                                pp.pprint(nn)
                        nn_debug.setdefault(neighbour, debug_data)
                    neighbours_neighbours.setdefault(neighbour, nn)
    del explored
    if recurse:
        return neighbours_coords, neighbours_neighbours
    return neighbours_coords


def create_neighbour_coordinates(tile):
    neighbours_coords, neighbours_neighbours = get_neighbours_positions(tile, P1, P2, 0, recurse=1)
    ####PART 2 : look up how the neighbouring tiles connect with the main tile
    if DEBUG2: print("Neighbour coords:", neighbours_coords)
    if DEBUG2: print("How many neighbours? :", len(neighbours_coords))

    center_coord = centeroftilestarting(P1, P2, tile[0][0], 0, tile)
    print("Center:", center_coord)
    neighbours_matches = dict()
    if DEBUG5:
        print("Neighbour neighbours:")
        for n in neighbours_neighbours:
            pp.pprint(n)
            pp.pprint(neighbours_neighbours[n])
        print("Neighbour coords:")
        for n in neighbours_coords:
            print(n)
            print(neighbours_coords[n])
    for neighbour in neighbours_coords:
        initials = list()
        matches = list()
        # case = old
        # outside = current
        # symmetrical = next
        # match old and next from current
        for case_initial, outside in neighbours_coords[neighbour]:
            initials.append((case_initial, outside))
            possible_match = find_matching(case_initial, outside, tile)
            # if(DEBUG2):print((case_initial,outside),possible_match)
            matches.append(possible_match)  # if no match, this is bad       initials.sort()
        initials.sort()
        matches.sort()
        neighbours_matches[neighbour] = (initials, matches)  # to find more easily with who it matches

    tag = ord("A")
    neighbour_tags = dict()
    for i, n in enumerate(neighbours_coords):
        neighbour_tags[chr(i + tag)] = n
        neighbour_tags[n] = chr(i + tag)
        for pair in neighbours_coords[n]:
            if pair in neighbour_tags:
                print("Error pair", pair, "is same as existing coord")
                # be careful not to overwrite a coordinate
            neighbour_tags[pair] = chr(i + tag)
    if DEBUG5:
        print("Neighbour tags:")
        pp.pprint(neighbour_tags)
    adjacent_matches = dict()
    for neighbour in neighbours_neighbours:
        self_tag = neighbour_tags[neighbour]
        for nnc in neighbours_neighbours[neighbour]:
            # look for existing coordinates in neighbour's neighbours
            if nnc in neighbours_coords:
                arrival_tag = neighbour_tags[nnc]
                for adjacent in neighbours_coords:
                    # look for one arbitrary matching case
                    if neighbours_neighbours[neighbour][nnc][0] in neighbours_coords[adjacent]:
                        adjacent_tag = neighbour_tags[adjacent]
                        break
                adjacent_matches[(self_tag, adjacent_tag)] = arrival_tag
    if DEBUG5:
        print("Adjacent matches:")
        pp.pprint(adjacent_matches)
    ####PART 3 : create a coordinates system based on how they connect
    # conway criterion for isohedral tiling
    if DEBUG2: print("Neighbours matches:", neighbours_matches)
    pair_axis = dict()
    # pair_axis[current_case,next_case] = axis, sign, inverter
    centrosymmetries = list()
    translations = list()
    translation_pairing = list()
    dimension = 0
    known_matches = list()
    known_dimensions = list()
    known_tags = list()
    if DEBUG5:
        print("Max dimensions:", len(neighbours_matches))
    for n, neighbour in enumerate(neighbours_matches):
        if DEBUG2: print("------Neighbour %d------" % n)
        initials, matches = neighbours_matches[neighbour]
        if DEBUG2: print("Comparing", initials, "and", matches)
        # if(DEBUG2):print(known_dimensions,known_matches)
        if initials == matches:
            if DEBUG2: print("Identical, adding a central symmetry dimension (%d)" % dimension)
            # paired neighbour is same neighbour: central symetry
            centrosymmetries.append(neighbour_tags[neighbour])
            known_dimensions.append(dimension)
            known_matches.append(matches)
            known_tags.append(neighbour_tags[neighbour])
            for pair in initials:
                # axis, sign, invert
                pair_axis[pair] = dimension, +1, True
            dimension += 1
        else:
            if DEBUG2: print("Different")
            if DEBUG2: print("Looking for", initials, "in", known_matches)
            if initials in known_matches:
                if DEBUG2: print("Found")
                # the starting point matches another's ending point
                # paired eighbour is opposite direction
                dim = known_dimensions[known_matches.index(initials)]
                for pair in initials:
                    # axis, sign, invert
                    pair_axis[pair] = dim, -1, False
                if DEBUG2: print("Found an existing dimension (%d)" % dim)
                translation_pairing.append((neighbour_tags[neighbour], known_tags[known_matches.index(initials)]))
                translations.append(neighbour_tags[neighbour])
                translations.append(known_tags[known_matches.index(initials)])
            else:
                # A new dimension
                if DEBUG2: print("Not found, new dimension (%d)" % dimension)
                known_matches.append(matches)
                known_dimensions.append(dimension)
                known_tags.append(neighbour_tags[neighbour])
                for pair in initials:
                    # axis, sign, invert
                    pair_axis[pair] = dimension, +1, False
                dimension += 1

    # return pair_axis, dimension
    if DEBUG5:
        print("Known tags:", known_tags)
        print("Adjacent pairings")
        print("Centrosymmetries:", centrosymmetries)
        print("Translations:", translations)
        print("Translation pairings:", translation_pairing)

    coordinates_system = create_coordinates_system(adjacent_matches, centrosymmetries, translations,
                                                   translation_pairing)

    pair_axis = dict()
    for neighbour in neighbours_coords:
        tag = neighbour_tags[neighbour]
        for coord in neighbours_coords[neighbour]:
            invert = tag in centrosymmetries
            pair_axis[coord] = (coordinates_system[tag], invert)
    return pair_axis


def evaluate(rules, formula, centrosymmetries, translation_get_pair):
    lenbase = len(tuple(rules.values())[0])
    res = [0] * lenbase
    sign = +1
    i = 0
    print("rules:",rules)
    print("formula:",formula)
    print("transation_get_pair=",translation_get_pair)
    while i < len(formula):
        sym = formula[i]
        if sym == "-":
            i += 1
            sym = translation_get_pair[formula[i]]
        if sym not in rules:
            jump = [-x for x in rules[translation_get_pair[sym]]]
        else:
            jump = rules[sym]
        res = [res[i] + sign * jump[i] for i in range(lenbase)]
        if sym in centrosymmetries:
            sign = -sign
        i += 1
    return res


def create_coordinates_system(neighbour_rules, centrosymmetries, translations, translation_pairs):
    if DEBUG6:
        print("Received rules:")
        pp.pprint(neighbour_rules)
        print("Translation pairs:")
        print(translation_pairs)
    undetermined = set(neighbour_rules.values())
    determined = set(centrosymmetries + translations) - undetermined
    translation_get_pair = dict()
    base_potential = sorted(undetermined)
    for p, q in translation_pairs:
        if q in base_potential:
            base_potential.remove(q)
        translation_get_pair[p] = q
        translation_get_pair[q] = p
    if DEBUG6:
        print("Create coordinates system based on rules:")
        pp.pprint(neighbour_rules)
        print("Centrosymmetries:")
        print(centrosymmetries)
    solved = False
    evaluated_base = dict()
    while not solved:
        for i, x in enumerate(base_potential):
            evaluated_base[x] = [0] * len(base_potential)
            evaluated_base[x][i] = 1
        if DEBUG6:
            print("Evaluated base step 1")
            pp.pprint(evaluated_base)

        # while any([y not in evaluated_base for y in undetermined]):
        rulescopy = neighbour_rules.copy()
        did_something = True
        while rulescopy and did_something:
            did_something = False
            for rule in sorted(rulescopy):
                y = neighbour_rules[rule]
                if y in evaluated_base:
                    rulescopy.pop(rule)
                    did_something = True
                    continue
                elif y in translations and translation_get_pair[y] in evaluated_base:
                    evaluated_base[y] = [-x for x in evaluated_base[translation_get_pair[y]]]
                    did_something = True
                elif all([x in evaluated_base for x in rule]):
                    evaluated_base[y] = evaluate(evaluated_base, rule, centrosymmetries, translation_get_pair)
        if rulescopy:
            if DEBUG6:
                print("Could not process those rules:")
                pp.pprint(rulescopy)

        for y in undetermined:
            if y not in evaluated_base:
                if DEBUG6: print("Could not resolve", y)
        if DEBUG6:
            print("Evaluated base step 2")
            pp.pprint(evaluated_base)
        solved = True
        for r in neighbour_rules:
            sym = evaluate(evaluated_base, neighbour_rules[r], centrosymmetries, translation_get_pair)
            ans = evaluate(evaluated_base, r, centrosymmetries, translation_get_pair)
            # print(neighbour_rules[r],sym,r,ans)
            if sym != ans:
                solved = False
                if DEBUG6:
                    print("Not equal:")
                    print(neighbour_rules[r], "=", sym)
                    print(neighbour_rules[r], "=", r, "=", ans)
                break
        if not solved:
            if DEBUG6: print("Not solved with base potential", base_potential)
            base_potential.pop()
            evaluated_base = dict()

    if DEBUG6:
        print("Solved with base potential", base_potential)
        print("Partial solution:")
        print(evaluated_base)
        print("Remaining:", determined)
    extralength = 0
    for base in sorted(determined):
        """if(base in evaluated_base):
        #should never be true
            determined.remove(base)
        elif base in translations and (translation_get_pair[base] in evaluated_base):
            evaluated_base[base]=[-x for x in evaluated_base[translation_get_pair[base]]]
            determined.remove(base)"""
        if base in translations:
            if (base, translation_get_pair[base]) in translation_pairs:
                # only for the firt one
                if DEBUG6: print("Translation pair", (base, translation_get_pair[base]))
                extralength += 1
            else:
                determined.remove(base)
                if DEBUG6: print("Translation half", base)
        else:
            extralength += 1
    if DEBUG6: print("Extra length to add:", extralength)
    for base in evaluated_base:
        evaluated_base[base].extend([0] * extralength)
    for i, base in enumerate(determined):
        extra = [0] * extralength
        extra[i] = 1
        evaluated_base[base] = [0] * len(base_potential) + extra
        if base in translations:
            extra[i] = -1
            evaluated_base[translation_get_pair[base]] = [0] * len(base_potential) + extra

    if DEBUG6:
        print("Solved with base potential", base_potential)
        print("Solution:")
        print(evaluated_base)
    return evaluated_base


import numpy as np


def is_known(cfo, tilecoord, positions, known_symmetries):
    # Solve linear equation with known symetries and return true if integer solution
    # If not integer,
    print("Entering is_known")
    known = positions[cfo]  # tilecoords of same case, face, orientation reached
    for knowncoord in known:
        a = np.array(known_symmetries)
        b = np.array([tilecoord[i] - knowncoord[i] for i in range(len(tilecoord))])
        print(a)
        print(b)
        if len(a) == len(b):
            x = np.linalg.solve(a, b)
        else:
            x = np.linalg.lstsq(a, b, rcond=1)
        print(x)
        for c in x:
            if int(c) != c:
                print("Not a solution:", x)
                continue
        print(x, "is an integer solution! Known")
        return True

    return False


def add_new_symmetry(cfo, tilecoord, positions, known_symmetries):
    for existing_position in positions[cfo]:
        possible_symmetry = [tilecoord[i] - existing_position[i] for i in range(len(tilecoord))]
        known_symmetries.append(possible_symmetry)
    known_symmetries.append(tilecoord)
    positions[cfo].append(tilecoord)


def explore_inside(tile, poly):
    classes = list()
    for start_case in tile:
        for start_face in poly:
            if len(tile[start_case]) == len(poly[start_face]):
                for orientation in range(len(poly[start_face])):
                    ###For every compatible CFO, start an exploration class
                    pos = (start_case, start_face, orientation)
                    if any(pos in existing_class for existing_class in classes):
                        continue
                    current_class = set()
                    to_explore = set()
                    to_explore.add(pos)

                    while to_explore:
                        case, face, orientation = to_explore.pop()
                        sides = len(poly[face])
                        if len(poly[case]) != sides:
                            continue
                        if (case, face, orientation) in current_class:
                            continue
                        current_class.add((case, face, orientation))

                        newcases = tile[case]
                        newfaces = poly[face][orientation:] + poly[face][:orientation]
                        for i in range(sides):
                            # for new areas to explore
                            newcase = newcases[i]
                            newface = newfaces[i]
                            if newcase % len(tile) == newcase:
                                # still inside
                                nextfaces = poly[newface]
                                nextcases = tile[newcase]
                                nextsides = len(nextfaces)
                                if len(tile[newcase]) != nextsides:
                                    continue
                                # look back for orientation
                                neworientation = (nextfaces.index(face) - nextcases.index(case)) % nextsides
                                if (newcase, newface, neworientation) not in current_class:
                                    to_explore.add((newcase, newface, neworientation))
                    classes.append(current_class)
    return classes


def explore_borders(tile, poly):
    borders = dict()
    for case in tile:
        for i, newcase in enumerate(tile[case]):
            if newcase % len(tile) != newcase:
                ###For every case pairs at the border
                startpair = (case, newcase)
                startsides = len(poly[case])
                nextcases = tile[newcase % len(tile)]
                nextsides = len(nextcases)
                # borders[startpair]=dict()
                for face in poly:
                    if len(tile[case]) == len(poly[face]):
                        for orientation in range(len(poly[face])):
                            # For  every (C)FO
                            newface = poly[face][(orientation + i) % startsides]
                            nextfaces = poly[newface]
                            if len(nextfaces) == nextsides:
                                caseindex = find_matching_offset(case, newcase, tile)
                                neworientation = (nextfaces.index(face) - caseindex) % nextsides
                                # borders[startpair][(case,face,orientation)]=(newcase%len(tile),newface,neworientation)
                                # borders.setdefault((case,face,orientation),set())
                                borders.setdefault((case, face, orientation), dict())
                                # borders[(case,face,orientation)].add((newcase%len(tile),newface,neworientation))
                                borders[(case, face, orientation)][startpair] = (
                                    newcase % len(tile), newface, neworientation)
    return borders


def explore_rotations(tile, poly,polyname):
    if DEBUG1 or DEBUG2 or DEBUG3 or 1: Draw.initialise_drawing(WIDTH, HEIGHT)
    if DEBUG1 or DEBUG2 or DEBUG3: Draw.empty_shapes()
    # Draw.polygon_shape((Point(0,0),Point(150,0),Point(150,150)), (255,0,0), alpha=1, outline=1)
    startcase = 0
    startface = 0
    face_ori = 0
    case_ori = 0
    # extend_tile(Point(300,300),Point(300,310),0,tile[0][0],tile)
    neighbour_coord = create_neighbour_coordinates(tile)
    dim = len(tuple(neighbour_coord.values())[0][0])
    if DEBUG2: print("-" * 20)
    if DEBUG2: print("Coordinate infos:", neighbour_coord)
    if DEBUG2: print("Number of axes:", dim)
    for coord in sorted(neighbour_coord):
        if DEBUG2:
            print(coord, ":", neighbour_coord[coord])
    # print("Dimensions:",dim)
    # print(flush=True)
    positions = dict()
    symmetry_axis = list()
    for case in tile:
        for face in poly:
            for orientation in range(len(poly[face])):
                positions[(case, face, orientation)] = list()
    if DEBUG3: print("Possible combinations: %d" % len(positions))

    pos = (P1, P2, 0, 0, 0, [0 for x in range(dim)], 1)
    to_explore = [pos]
    while to_explore:
        p1, p2, case, face, orientation, tilecoord, tilecoordsign = to_explore.pop()
        # if(case%len(tile)!=case):
        #    continue
        # print("exploring",p1,p2,"case",case,"face",face,orientation,tilecoord, tilecoordsign )
        if len(tile[case % len(tile)]) != len(poly[face]):
            continue
        # caseorientation = 0
        # orientation is tileorientation
        # print("Known positions for",case%len(tile),face,orientation)
        # print(positions[(case%len(tile),face,orientation)])
        if tilecoord in positions[(case % len(tile), face, orientation)]:
            continue
        # if(not is_known((case,face,orientation),tilecoord,positions,symmetry_axis)):
        startpoints = get_face_points(p1, p2, len(poly[face]))
        color = Draw.colors[sum([abs(x * (n + 1)) for n, x in enumerate(tilecoord)]) % len(Draw.colors)]
        Draw.polygon_shape(startpoints, color, 0.75, 1)
        # Draw.text_center("%d/%d+%d"%(face,case%len(tile),(case-(case%len(tile)))//len(tile)),*centerpoint(startpoints),(255,255,255),int(ext/2))
        Draw.text_center(str(tilecoord) + str(tilecoordsign), *centerpoint(startpoints), (255, 255, 255), int(ext / 4))
        # Draw.text_center("%d(%d)"%(case,(case-(case%len(tile)))//len(tile)),*centerpoint(startpoints),(255,255,255),int(ext/2))
        Draw.refresh()
        # Draw.wait_for_input()
        if len(positions[(case % len(tile), face, orientation)]) == 0:
            # add_new_symmetry((case,face,orientation),tilecoord,positions,symmetry_axis)
            # Draw.wait_for_input()
            newcases = tile[case % len(tile)]
            newfaces = poly[face][orientation:] + poly[face][:orientation]
            if DEBUG3: print(case % len(tile), newcases)
            if DEBUG3: print(face % len(poly), newfaces)
            for i in range(len(newcases)):
                newface = newfaces[i]
                newcase = newcases[i]
                # if(newcase%len(tile)!=newcase):
                #    continue
                if DEBUG3: print("index", i, "going to", newcase)
                if len(tile[newcase % len(tile)]) != len(poly[newface]):
                    continue
                pa, pb = (startpoints * 2)[i:i + 2]  # where to start to draw the new case
                branchpoints = get_face_points(pb, pa, len(poly[newface])) * 2
                branchoffset = len(tile[newcase % len(tile)]) - find_matching_offset(case, newcase, tile)
                p1p, p2p = branchpoints[branchoffset:branchoffset + 2]  # where to start the caseorientation=0
                newface_orientation = (poly[newface].index(face) + branchoffset) % len(poly[newface])
                newtilecoord = tilecoord.copy()
                newtilecoordsign = tilecoordsign
                if newcase != newcase % len(tile) or newcase == case:
                    # print("Neighbour moving",(case%len(tile),newcase),newcase%len(tile))
                    axis, invertsign = neighbour_coord[(case % len(tile), newcase)]
                    newtilecoord = [newtilecoord[x] + axis[x] * tilecoordsign for x in range(len(newtilecoord))]
                    if invertsign:
                        newtilecoordsign = -newtilecoordsign
                    # print(dim,increment,invertsign)
                    # print(tilecoord,tilecoordsign,"->",newtilecoord,newtilecoordsign)

                to_explore.append((p1p, p2p, newcase, newface, newface_orientation, newtilecoord, newtilecoordsign))
        positions[(case % len(tile), face, orientation)].append(tilecoord)
    if DEBUG3 or DEBUG7: pp.pprint(positions)
    print("Done exploring everything!")
    # Draw.wait_for_input()
    # Next: explore the space!
    #def CFO_adjacency_matrix(tile,poly,polyname):
    classes = explore_inside(tile, poly)
    # print(len(classes),"classes found:")
    # pp.pprint(classes)
    transformations = explore_borders(tile, poly)
    borders = set(transformations)
    # print("Borders:",len(transformations))
    # pp.pprint(transformations)

    for clas in classes:
        if (0, 0, 0) in clas:
            initial_class = classes.index(clas)
            break

    def class_index(cfo):
        for i, clas in enumerate(classes):
            if cfo in clas:
                return i
    print("Classes:")
    pp.pprint(classes)
    # input()

    class_transfo = [[list() for clas in classes] for clas in classes]
    for cfo in transformations:
        class_start = class_index(cfo)
        for bordercase in transformations[cfo]:
            coordinate = neighbour_coord[bordercase]
            cfo_arrival = transformations[cfo][bordercase]
            class_end = class_index(cfo_arrival)
            # print(transformations[cfo][bordercase])
            # print(cfo,cfo_arrival)
            if coordinate:
                print("C1,C2,coord", class_start, class_end, coordinate)
                class_transfo[class_start][class_end].append(coordinate)
    print("Class transformations:")

    pp.pprint(class_transfo)
    # input()

    def print_matrix(mat, explored=None):
        if explored is None:
            explored = []
        for ind, line in enumerate(mat):
            print()
            for index, elem in enumerate(line):
                if elem:
                    if elem < 10:
                        print(end=str(int(elem)))
                    elif elem - 10 < 52:
                        print(end=chr(ord("A") + elem - 10))
                    else:
                        print(end="#")
                    """if(len(str(int(elem)))>1):
                        try:
                            print(end=chr(ord("A")+elem))
                        except:
                            print(end="X")"""
                else:
                    print(end=str(int(elem)))
        print()

    def print_matrix_limited(mat, limitations):
        for i, line in enumerate(mat):
            if not (i in limitations):
                continue
            print()
            for j, elem in enumerate(line):
                if not (j in limitations):
                    continue
                if elem:
                    print(end="X")
                    """if(len(str(int(elem)))>1):
                        try:
                            print(end=chr(ord("A")+elem))
                        except:
                            print(end="X")"""
                else:
                    print(end=str(int(elem)))
        print()

    size = len(classes)
    class_transfo_matshow = [[bool(class_transfo[i][j]) for i in range(size)] for j in range(size)]

    def print_classmat(class_transfo):
        for line in class_transfo:
            print()
            for index, element in enumerate(line):
                if element:
                    if index == initial_class:
                        print(end="I")
                    else:
                        print(end="X")
                else:
                    print(end=" ")

    def add_matr(ma1, ma2):
        m = len(ma1[0])
        p = len(ma2)
        ma3 = [[ma1[i][j] or ma2[i][j] for i in range(m)] for j in range(p)]
        return ma3

    def mul_matr(ma1, ma2):
        m = len(ma1[0])
        p = len(ma2)
        n = len(ma1)  # and len(ma2[0])
        ma3 = [[bool(sum((ma1[i][k] * ma2[k][j] for k in range(n)))) for i in range(m)] for j in range(p)]
        """for i in range(p):
            for j in range(m):
                for k in range(n):
                    #ma3[i][j]+=ma1[i][k]*ma2[k][j]
                    ma3[i][j] = ma3[i][j]  or ma1[i][k] * ma2[k][j]"""
        return ma3

    all_classes = set(range(len(classes)))
    all_explored = list()
    explore = [initial_class]
    explored = [initial_class]
    while all_classes:
        # print(all_classes)
        while explore:
            new = explore.pop()
            for next, elem in enumerate(class_transfo[new]):
                if elem and not (next in explored):
                    explore.append(next)
                    explored.append(next)
        all_classes = all_classes.difference(set(explored))
        all_explored.append(explored)
        if all_classes:
            explore = [list(all_classes).pop()]
            explored = [explore[0]]

    print()
    print("Classes:", len(classes))
    print("Reachable classes from initial:", len(all_explored[0]))
    print(all_explored[0])
    print("Reachability groups:", len(all_explored))
    print("Their sizes:")
    print(", ".join(str(len(e)) for e in all_explored if len(e) > 1))
    print("And", sum(1 for e in all_explored if len(e) == 1), "of size 1")
    # pp.pprint(all_explored)
    ma = class_transfo_matshow

    print("Limited form by", all_explored[0])
    print_matrix_limited(ma, all_explored[0])
    # print_matrix(ma)

    for i in range(size):
        print("Step", i)
        ma2 = mul_matr(ma, ma)
        if ma2 == ma:
            break
        ma = add_matr(ma2, ma)
    print("Full form:")
    print_matrix(ma, all_explored[0])

    for y, line in enumerate(ma):
        for x, elem in enumerate(ma):
            c = ma[y][x]
            if c:  # or x==y):
                for index, group in enumerate(all_explored):
                    # print(x,y,group,x in group or y in group)
                    if x in group or y in group:
                        c = index + 1
                        if len(group) == 1:
                            c = -1
            ma[y][x] = c

    print(all_explored)
    explore_order = list()
    for x in all_explored:
        explore_order.extend(x)

    ordered = [[0 for i in range(size)] for j in range(size)]
    for index, clas in enumerate(explore_order):
        for index2, clas2 in enumerate(explore_order):
            ordered[index][index2] = ma[clas][clas2]

    print_matrix(ordered)
    try:os.mkdir(".archives/CFO_ajdacency_matrixes/")
    except:pass
    try:os.mkdir(".archives/CFO_ajdacency_matrixes/tessellation_polyhedron/")
    except:pass

    Draw.turn_into_image(ordered,"CFO_ajdacency_matrixes/tessellation_polyhedron/"+polyname+".png")
    # pp.pprint(classes)
    # explored_classes = list()
    """"
    to_explore = [([initial_class],[0]*dim,1)]
    pp.pprint(transformations)
    while to_explore:
        pathclasses,coord,coordsign=to_explore.pop()
        currentclass = pathclasses[-1]
        possible_transformations = borders.intersection(currentclass)
        for transformation_border in possible_transformations:
            for transformation_path in transformations[transformation_border]:
                coordshift,invertsign = neighbour_coord[transformation_path]
                newcoord = [coord[i] + coordsign*coordshift[i] for i in range(dim)]
                newcoordsign = coordsign*(1-invertsign*2)
                #if()
                #for clas in classes:
    """

    # Draw.wait_for_input()

tesspoly_order = ['tetrahedron', 'cube', 'octahedron', 'icosahedron', 'j1', 'j8', 'j10', 'j12', 'j13', 'j14', 'j15', 'j16', 'j17', 'j49', 'j50', 'j51', 'j84', 'j86', 'j87', 'j88', 'j89', 'j90', 'hexagonal_antiprism']

# tesspoly_order = ["hexagonal_antiprism","j10","j88"] #fails to create a base for these three, too many removed
tesspoly_order = ['cube']
if __name__ == "__main__":
    erratum = list()
    for polyname in tesspoly_order:
        print(polyname)
        try:explore_rotations(net_tessellations[polyname], tessellation_polyhedrons[polyname], polyname)
        except Exception as e:
            traceback.print_exc()
            erratum.append(polyname)
    print("The following could not work:")
    print(erratum)
        # explore_rotations(nets[polyname], polys[polyname], polyname)
    # explore_rotations(nets["octahedron"], polys["octahedron"], polyname)
    # explore_rotations(nets["tetrahedron"],polys["tetrahedron"])
    # explore_rotations(nets["j1"],polys["j1"])
    #explore_rotations(nets["octahedron"], polys["octahedron"])

# Usage:
# have a tuple of size dimension "pos", and a sign modifier "sign_modif"=1
# for each out-of-tile move, look up dim,sign,invert = pair_axis[(current,next)]
# pos[dim]+=sign*sign_modif
# if(invert): sign_modif=-sign_modif
