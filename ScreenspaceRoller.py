"""Rolls in the screen space and fills it (rectangle) and can produce images"""
import os
from datetime import datetime
from os.path import exists
from time import time

import svgwrite

from _resources.symmetry_classes.tiling_symmetries import canon_co
from _libs.GeometryFunctions import *
from _libs.GenPngScreenspaceRoller import draw_answer, draw_background, draw_polygon, refresh, draw_tiling, \
    map_screenspace, convertToTuples
from _resources.uniform_tiling_supertiles import uniform_tilings
from _resources.regular_faced_polyhedron_nets import all_nets
from _resources.symmetry_classes.poly_symmetries import poly_symmetries
from _resources.symmetry_classes.poly_symmetries import canon_fo
from _libs.FileManagementShortcuts import pickleThis, unpickleThis

"""Roll a shape in a space with a given tiling and starting position
"""
OUTPUT_SVG = False
TAKE_PICKLE = True
LOAD_PROGRESS = True

PREVIEW = False
COLOR_GRADATION = False  # True
PREVIEWPERIODICITY = 0  # 20
# SLOW=False
OPTIMISE_SYMMETRIES = True
SKIP_NOTFULL = False

PREVIEW_TILINGNAME = False
PREVIEW_POLYNAME = False

TAKE_PICTURES = False
DRAW_ANSWER = False
BIGGEST_PICTURE = True

PICTURE_TRESHOLD = 0  # 0.03
ROLL_ONLY_ONCE = False  # True
TIME_LIMIT = -1  # 3.5
WAIT_AT_END = False  # 0.5

SCREENSPACE = 1
NSPACE = 2
EXPLORATION_SPACE = SCREENSPACE

CHECK_UNUSED_FACES = False  # Will disable symmetry optimisations
CHECK_ALL_CELLS = True  # Only checking rollers: will go everywhere eventually
# CHECK_ALL_FACEROT = False

PAUSE_AT_BEGINNING = 0  # 3000
QUIT_PREVIEW_EARLY = False

LIMIT_TO_ROLLING_PAIRS = False
LIMIT_TO_SHOWCASE = False  # True
INSERT_FILL = False  # insert new areas to explore at the beginning. Only checking rollers

TESSELLATION_POLYHEDRON = False

# Modes
# Roller : OPTIMISE_SYMMETRIES = True, CHECK_ALL_CELLS = False, SKIP_NOTFULL = True, CHECK_UNUSED_FACES = False, QUIT_PREVIEW_EARLY = True
# Perfect Roller: OPTIMISE_SYMMETRIES = False, CHECK_ALL_CELLS = False, SKIP_NOTFULL = True, CHECK_UNUSED_FACES = True, QUIT_PREVIEW_EARLY = False
# Visitor: OPTIMISE_SYMMETRIES = True, CHECK_ALL_CELLS = True, SKIP_NOTFULL = False, QUIT_PREVIEW_EARLY = False


# QUIT_SEARCH_EARLY = False
#
TEMPORARY_GLOBAL_COUNTER = 0


skip_pairs = []
resume_counter = -1

all_tilings = {**uniform_tilings}

if (TESSELLATION_POLYHEDRON):
    from _resources.TessellationPolyhedronAndTilings import tessellation_polyhedrons, net_tessellations

    all_tilings = net_tessellations
    all_nets = tessellation_polyhedrons
    from _resources.symmetry_classes.TessPolySymmetries import TessPoly as poly_symmetries
#
# winning_pairs = {('(3^6;3^2x4x3x4)', 'j89'), ('(3^6)', 'j84'), ('(3^6)', 'j89'), ('(3^2x4x3x4)', 'j31'), ('(3^6;3^3x4^2)2', 'j87'), ('(3^6;3^3x4^2)2', 'j89'), ('(3^6)', 'j87'), ('(3x4x6x4)', 'j54'), ('(3^6;3^3x4^2)2', 'j50'), ('(3^6)', 'j13'), ('(3^6;3^2x4x3x4)', 'j87'), ('(3^6;3^2x4x3x4)', 'j50'), ('(3^6)', 'j51'), ('(3^6)', 'j50'), ('(3^6)', 'j11'), ('(3^6;3^3x4^2)1', 'j90'), ('3^2x4x3x4', 'j26'), ('(3^3x4^2)', 'j28'), ('(3^6;3^3x4^2)1', 'j14'), ('(3^6;3^4x6)1', 'j22'), ('(3^6;3^3x4^2)1', 'j10'), ('(3^6;3^4x6)2', 'hexagonal_antiprism'),  ('(3^6;3^3x4^2)1', 'j88'), ('(3^6)', 'octahedron'), ('(3^6;3^3x4^2)2', 'j86'), ('(3^3x4^2)', 'j27'), ('(3x4x6x4)', 'j56'), ('(3^6;3^2x6^2)', 'truncated_tetrahedron'), ('(3^6)', 'j86'), ('(4^4)', 'j8'), ('3^4x6;3^2x6^2', 'hexagonal_antiprism'), ('3^6;3^2x4x3x4', 'j86'), ('(3^3x4^2;3^2x4x3x4)1', 'j1'), ('(3^6;3^3x4^2)1', 'j16'), ('(3^6;3^3x4^2)1', 'j89'), ('3^3x4^2', 'square_antiprism'), ('4^4', 'j37'), ('3^2x4x3x4', 'j29'), ('(3^6;3^3x4^2)2', 'j90'), ('(3^6;3^3x4^2)1', 'j87'), ('3^6', 'j62'), ('3^6', 'j90'), ('(3^3x4^2;3^2x4x3x4)2', 'j26'), ('(3^6;3^3x4^2)2', 'j10'), ('3^6;3^2x4x3x4', 'j10'), ('3^6;3^2x4x3x4', 'j90'), ('4^4', 'cube'), ('(3^3x4^2;3^2x4x3x4)1', 'j27'), ('3^6', 'j10'), ('(3^6;3^3x4^2)1', 'j50'), ('3^3x4^2', 'j30'), ('(3^6;3^3x4^2)2', 'j85'), ('(3^6;3^3x4^2)2', 'j88'), ('3^6', 'j85'), ('3^6', 'j17'), ('3^2x4x3x4', 'j1'), ('3x6x3x6', 'j65'), ('3^6;3^2x4x3x4', 'j1'), ('3^6', 'j88'), ('3^6;3^2x4x3x4', 'j85'), ('3^6', 'tetrahedron'), ('(3^6;3^3x4^2)1', 'j15'), ('(3^6;3^4x6)1', 'hexagonal_antiprism'), ('3^6', 'icosahedron'), ('3^6', 'j12'), ('3^4x6', 'hexagonal_antiprism'), ('(3^6;3^3x4^2)1', 'j86')}
# TODO: rewrite the "winning pair" thing to import the Proof generated dict

# if(LIMIT_TO_ROLLING_PAIRS):
#     if(TESSELLATION_POLYHEDRON):
#         with open("saved_results/tessellation_polyhedron/rollers.txt","r") as f:
#             winning_pairs = [tuple(line.split()[:2]) for line in f.readlines()]
#     else:
#         with open("saved_results/rollers/rollers.txt","r") as f:
#             winning_pairs = [tuple(line.split()[:2]) for line in f.readlines()]
# print(winning_pairs)

showcase = []
showcase += [("(3^3x4^2;3^2x4x3x4)2", "j26"), ("(4^4)", "j37"), ("(3^3x4^2;3^2x4x3x4)1", "j27"),
             ("(3^3x4^2;3^2x4x3x4)1", "j27"), ("(3^6;3^4x6)1", "j22"), ("(3^6;3^4x6;3x6x3x6)2", "hexagonal_antiprism"),
             ("(3^6;3^3x4^2;3^2x4x3x4)", "j1"), ("(3^6;3^2x6^2)", "truncated_tetrahedron"),
             ("(3^6;3^4x6)2", "hexagonal_antiprism")]  # ,("15-3^6;3^2x4x3x3x4;3x4^2x6","j3")
showcase += [("(3^3x4^2;4^4)1", "j23"), ("(3^3x4^2;3^2x4x3x4)1", "j7"), ("(3^3x4^2;3^2x4x3x4)1", "j26"),
             ("(3^6;3^4x6)1", "j46"), ("(3^3x4^2;3^2x4x3x4)2", "snub_cube"), ("(3^3x4^2;3^2x4x3x4)2", "j86"),
             ("(3^3x4^2;4^4)2", "j28"), ("(3^3x4^2;3^2x4x3x4)1", "j90")]  # , ("(3^3x4^2;3^2x4x3x4)1","j49")
showcase += [("(3^3x4^2;3^2x4x3x4)1", "j46"), ("(3^3x4^2;3^2x4x3x4)1", "j18"), ("(3^3x4^2;3^2x4x3x4)1", "j22"),
             ("(3^3x4^2;3^2x4x3x4)1", "j23"), ("(3^3x4^2;3^2x4x3x4)1", "j29"), ("(3^3x4^2;3^2x4x3x4)1", "j44"),
             ("(3^6;3^3x4^2)2", "j23"), ("(3^4x6)", "j88"), ("(3^6;3^4x6)2", "j22")]
showcase += [("(3^6;3^3x4^2;3x4x6x4)", "j1"), ("(3^6;3^2x4x3x4;3x4x6x4)1", "j3"), ("(3^3x4^2)", "j89"),
             ("(3^6;3^2x4x3x4;3x4x6x4)2", "j3"), ("4^4", "j28"), ("(3^3x4^2;3^2x4x3x4)1", "triangular_prism"),
             ("(3^2x6^2;3x6x3x6;6^3)2", "truncated_tetrahedron"), ("(3^2x6^2;3x6x3x6;6^3)1", "truncated_tetrahedron"),
             ("(3^6;3^2x4x3x4;3x4x6x4)2", "j44"), ("(3^2x4x3x4;3x4x6x4)", "j18")]
showcase += [("(3^3x4^2;3^2x4x12;3x4x6x4)", "j30"), ("(3^6;3^2x4x3x4;3x4x6x4)2", "j90"),
             ("(3x4^2x6;3x6x3x6))_2", "hexagonal_prism"), ("(3^6;3^2x6^2)", "truncated_icosahedron"),
             ("(4x8^2)", "truncated_cube"), ("(3^6;3^4x6)2", "tetrahedron")]

if (LIMIT_TO_SHOWCASE):
    # LIMIT_TO_ROLLING_PAIRS=True
    showcase_update = []
    for tiling_s, p in showcase:
        for tiling in all_tilings:
            if tiling.endswith(tiling_s):
                showcase_update.append((tiling, p))
                break
    showcase = showcase_update

all_tilings_names = list(all_tilings.keys())  # if you want to limit to a few, change this line
# all_tilings_names=all_tilings_names[all_tilings_names.index("(3^6;3^3x4^2)1"):]
# all_tilings_names = ["4^4"]
# all_tilings_names = ["3^6"]
# all_tilings_names=["3^6;3^2x4x3x4"]
# all_tilings_names=["02-(3^6;3^4x6;3^2x6^2)2"]

all_nets_names = list(all_nets.keys())  # if you want to limit to a few, change this line


# all_nets_names = all_nets_names[all_nets_names.index("j50"):]
# all_nets_names = ["cube"]
# all_nets_names = ["snub_cube"]
# all_nets_names=["j89"]
# all_nets_names=["hexagonal_antiprism"]

def outputfolder(*parts):
    print(parts)
    name = os.sep.join(parts) + os.sep
    try:
        os.makedirs(name, exist_ok=True)
    except:
        pass
    return name

progressfile = outputfolder("_results")+"PROGRESS_CHECKPOINT.txt"

import sys
import argparse


def str2bool(v):
    # https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse/43357954#43357954
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 'True', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'False', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


parser = argparse.ArgumentParser(description="Roll polyhedrons in tilings, report the results")
parser.add_argument("-f", "--skipnotfull", type=int,
                    help="Skip looking when one of the face of the tiling is not in the polyhedron (when the space is not fully explorable). Only look for full rolling. (default=%i)" % SKIP_NOTFULL)
# parser.add_argument("-f","--skippartial", type=int, help="Skip looking when one of the face of the polyhedron is not in the tiling (Partial Roller, when one face of the poly will not be used). (default=%i)"%SKIP_NOTFULL)

parser.add_argument("-p", "--preview", type=int,
                    help="En/Disable preview for speed (default=" + str(int(PREVIEW)) + ")")
parser.add_argument("-l", "--load", type=int, help="En/Disable progress loading (default=" + str(int(LOAD_PROGRESS))
                                                   + ")\nDon't forget to backup your PROGRESS_CHECKPOINT.txt file before turning this off!")
parser.add_argument("-c", "--color", type=str, help="Choose [single] color or [gradation] for preview (default="
                                                    + ["single", "gradation"][COLOR_GRADATION] + ")")
parser.add_argument("-s", "--prevspeed", type=int,
                    help="How many steps of preview are skipped between refreshes. Bigger number makes the app run faster, smaller number makes the animation prettier. (default=%s)" % PREVIEWPERIODICITY)
parser.add_argument("-t", "--picture", type=int,
                    help="Take pictures for every failed step. (default=%i)" % TAKE_PICTURES)
parser.add_argument("-u", "--check_unused", type=int,
                    help="Check unused faces for successful search. Disables optimisations. (default=%i)" % CHECK_UNUSED_FACES)
parser.add_argument("-k", "--skip_current", action='store_true', help="Skip current face in counter order.")
args = parser.parse_args()

if (len(sys.argv) == 1):
    parser.print_help()

if args.preview != None:
    PREVIEW = args.preview
if args.color != None:
    COLOR_GRADATION = ["single", "gradation"].index(args.color)
if args.prevspeed != None:
    PREVIEWPERIODICITY = args.prevspeed
if args.load != None:
    LOAD_PROGRESS = args.load
if args.skipnotfull != None:
    SKIP_NOTFULL = args.skipnotfull
if args.picture != None:
    TAKE_PICTURES = args.picture
if args.check_unused != None:
    CHECK_UNUSED_FACES = args.check_unused
if (CHECK_UNUSED_FACES):
    OPTIMISE_SYMMETRIES = False

print(args)

if (PREVIEW):
    import pygame

    pygame.init()
    screen = pygame.display.set_mode((800, 800), pygame.DOUBLEBUF)
    screen.fill((255, 255, 255, 255))
    outlines = pygame.Surface((800, 800), pygame.SRCALPHA)
    temp = pygame.Surface((800, 800), pygame.SRCALPHA)


def make_timestamp():
    return datetime.now().strftime("[%Hh%Mm%S]")


def cell_match(tiling, previous_case, newcaseid):
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
    print(previous_case, newcaseid, tiling)


case_match = cell_match


def is_outside(previouscase, newcaseid):
    newcase, id = newcaseid
    if (previouscase == newcase):
        return True
    if id != 0:
        return True
    return False


def co_orient_face(net, prevface, newface, tiling, prevcase, newcaseid):
    # align the face on the cell/case
    # this is by how much the face is shifted compared to the cell
    face_shift = net[newface].index(prevface)
    case_shift = case_match(tiling, prevcase, newcaseid)
    common_orientation = face_shift - case_shift
    return common_orientation


def get_unused_faces(result, poly, polyname):
    faces = set(poly.keys())
    # for face in poly:
    #     for ori in range(len(poly[face])):
    #         faces.add(canon_fo(polyname,face,ori)[0])
    for res in result.values():
        for face, orientation in res:
            # try:faces.remove(canon_fo(polyname,face,orientation)[0])
            try:
                faces.remove(face)
            except:
                pass
        if not faces:
            return faces
    return faces


def map_nspace(tiling, startcell, area, p1, p2, precision, N):
    "visited areas[center points: (polygon, cell number)]"
    visited_areas = dict()
    visits = [(startcell, p1, p2, 0, 0)]
    while (visits):
        cell, p1, p2, tiledistance, celldistance = visits.pop(0)
        cface = xgon(len(tiling[cell]), p1, p2)
        ccenter = roundedcenter(cface, precision)

        if (tiledistance > N):
            continue
        # if(celldistance>N):
        #     continue
        if (ccenter in visited_areas and visited_areas[ccenter][2] <= tiledistance):
            continue

        visited_areas[ccenter] = (cface, cell, tiledistance, celldistance)  # later for drawing

        for index, nextcellid in enumerate(tiling[cell]):
            cell_shift = cell_match(tiling, cell, nextcellid)
            nextcell, id = nextcellid
            # Create a stub ncface at the edge of the current cface
            nextface_stub = xgon(len(tiling[nextcell]), cface[(index + 1) % len(cface)], cface[index])
            # Reorient it
            pa, pb = nextface_stub[-cell_shift], nextface_stub[(-cell_shift + 1) % len(nextface_stub)]
            ncenter = roundedcenter(nextface_stub, precision)
            tdistance = tiledistance + is_outside(cell, nextcellid)
            ndistance = celldistance + 1
            # if(ncenter in visited_areas):
            #     print(visited_areas[ncenter])
            if ndistance <= N and not (ncenter in visited_areas and visited_areas[ncenter][2] > ndistance):
                visits.append((nextcell, pa, pb, tdistance, ndistance))
    return visited_areas

"""
def comparepoints(pts1,pts2):
    if(len(pts1)!=len(pts2)):
        return False
    for i in range(min(len(pts1,pts2))):
        is_equal = True
        for xy in pts1[i:]+pts1[:i]:
            for xxyy in pts2:
                for j in range(2):
                    if abs(xy[j]-xxyy[j])>1:
                        is_equal = False
            if not is_equal:
                break
    return is_equal
"""

def draw_lines_svg(svg,lineslist):
    area = (RollyPoint(0,0),RollyPoint(800,0),RollyPoint(800,800),RollyPoint(0,800))
    #maybe optimize them
    for segment in lineslist:
        if is_inside(RollyPoint(segment[0]),area) or is_inside(RollyPoint(segment[1]),area):
            svg.add(svg.line(*segment, stroke="black", stroke_width=2))
    return svg


def draw_polygons_svg(svg,polylist):
    #maybe optimize them
    area = (RollyPoint(0,0),RollyPoint(800,0),RollyPoint(800,800),RollyPoint(0,800))
    for poly in polylist:
        if(any(is_inside(RollyPoint(point),area) for point in poly)):
            svg.add(svg.polygon(poly, fill="red"))
    return svg

def draw_filled_result_svg(filename, mapping, visited):
    def comparesegments(s1,s2):
        return sum((abs(s1[s][xy]-s2[s-1][xy])<=1 for s in range(2) for xy in range(2)))==4
    segments = set()
    # print(mapping.values())
    for visitedplace in mapping.values():
        # print(visitedplace)
        # for cface, cell, tiledistance, celldistance in visitedplace:
        cface = convertToTuples(visitedplace[0])
        for i in range(len(cface)):
            segment = cface[i-1],cface[i]
            if not any(comparesegments(segment,other_segment) for other_segment in segments):
                segments.add(segment)
    polys = list()
    for visitedplace in visited.values():
        if(visitedplace):
            c, f, o, poly = visitedplace[0] #there can be several, I didn't really do a good job with poly's duplication
            polys.append(convertToTuples(poly))

    svg = svgwrite.Drawing(filename+'.svg', profile='tiny',height=800, width=800)
    draw_polygons_svg(svg,polys)
    draw_lines_svg(svg,segments)
    svg.save()
    return


def drawtemp(points, color, outline=0):
    temp.fill((255, 255, 255, 0))
    draw_polygon(temp, color, points, outline)
    screen.blit(temp, (0, 0))


def drawdir(p1, p2, color=(128, 0, 0)):
    points = triangle(p1, p2)
    phalf = (p1 + p2) / 2
    points = (phalf, (phalf + points[2]) / 2)
    # draw_polygon(temp,color,,3)
    drawtemp(points, color, 3)


from _libs import CFOClassGenerator


def determine_n(tiling, net, polyname):  # ,startcase,startface,startorientation):
    # classes = CFOClassGenerator.explore_inside(tiling,net,polyname,canon_fo)
    # borders = CFOClassGenerator.explore_borders(tiling,net)
    N = sum(len(net[face]) == len(tiling[cell]) and (face, o) == canon_fo(polyname, face, o)
            for face in net for cell in tiling for o in range(len(net[face])))
    classes = CFOClassGenerator.explore_inside(tiling, net, polyname, canon_fo)
    N2 = len(classes)
    # print(classes)
    # print("N=",N)
    size = max(len(elem) for elem in poly_symmetries[polyname])
    # if(size==1):
    #     input("Biggest symmetry class for %s:\n:::%i"%(polyname,size))
    # else:
    print("Biggest symmetry class for %s:\n:::%i" % (polyname, size))
    if (N2 > N):
        print("[Error]Amount of classes bigger than amount of positions, N=%i<%i" % (N2, N))
    elif (N2 < N):
        print("[Optimisation]Amount of classes smaller than amount of positions, N=%i<%i" % (N2, N))
    else:
        #     print("Amount of states smaller than amount of classes,
        print("[No optimisation]N=%i==%i" % (N, N2))
    return min(N + 1, N2 + 1)


def n_explore(tiling, net, startcase, startface, startorientation, mapping, sp1, sp2, polyname, precision):
    # mapping= visited areas[center points: (polygon, cell number, distance in tile to center)]
    visited_places = {coord: [] for coord in mapping.keys()}
    quickcheckcenter = list()
    quickcheck = list()
    if (OPTIMISE_SYMMETRIES):
        startface, startorientation = canon_fo(polyname, startface, startorientation)
    if (PREVIEW):
        previewcounter = 0
    for place in mapping.values():
        coords = place[0]
        cell = place[1]
        # print(place)
        tiledistance = place[2]
        celldistance = place[3]
        if tiledistance == 1:
            if (cell == startcase):
                quickcheckcenter.append(roundedcenter(coords, precision))
            else:
                quickcheck.append(roundedcenter(coords, precision))
    quickcheckcentersum = 0
    quickchecksum = 0
    visits = [(startface, startcase, startorientation, sp1, sp2)]
    while visits:
        # can return true already, filled all neighbouring tiles and visited them with same CFO
        face, case, orientation, p1, p2 = visits.pop(0)
        # if(polyname=="j10"):
        #     print("Visits left:",visits)
        if (len(net[face]) != len(tiling[case])):
            continue  # can't explore this

        cface = xgon(len(net[face]), p1, p2)
        ccenter = roundedcenter(cface, precision)
        if ccenter not in visited_places:
            continue  # Out of bounds
        if (OPTIMISE_SYMMETRIES):
            face, orientation = canon_fo(polyname, face, orientation)
        if (case, face, orientation) in visited_places[ccenter]:
            continue  # already reached

        # print(OPTIMISE_SYMMETRIES,case,face,orientation)
        # print(canon_fo(polyname,face, orientation))
        if (case, face, orientation) == (startcase, startface, startorientation):
            drawtemp(cface, (255, 0, 0))
            drawdir(p1, p2)
            # refresh()
        elif (len(visited_places[ccenter]) == 0):
            drawtemp(cface, (255, 180, 180))
            # refresh()
        visited_places[ccenter].append((case, face, orientation))

        neighbours_faces = net[face]
        neighbours_faces = neighbours_faces[orientation:] + neighbours_faces[:orientation]

        for index, nextcellid in enumerate(tiling[case]):
            nextcell, id = nextcellid
            nextface = neighbours_faces[index]  # aligned with cell
            if (len(net[nextface]) != len(tiling[nextcell])):
                continue
            face_shift = net[nextface].index(face)
            case_shift = case_match(tiling, case, nextcellid)
            # Create a stub nface at the edge of the current face
            nextface_stub = xgon(len(net[nextface]), cface[(index + 1) % len(cface)], cface[index])
            pa, pb = nextface_stub[-case_shift], nextface_stub[(-case_shift + 1) % len(nextface_stub)]
            nextorientation = (-case_shift + face_shift) % len(nextface_stub)
            if (OPTIMISE_SYMMETRIES):
                nextface, nextorientation = canon_fo(polyname, nextface, nextorientation)
            nextcenter = roundedcenter(nextface_stub, precision)
            if (nextcenter in visited_places and (nextface, nextorientation) not in visited_places[nextcenter]):
                if (len(visited_places[nextcenter]) == 0 and INSERT_FILL):
                    visits.insert(0, (nextface, nextcell, nextorientation, pa, pb))
                else:
                    visits.append((nextface, nextcell, nextorientation, pa, pb))

        if (PREVIEW):
            previewcounter += 1
            if (previewcounter % PREVIEWPERIODICITY == 0):
                refresh()
                screen.blit(outlines, (0, 0))

        quickcheckcentersum = sum((startface, startorientation) in visited_places[coord] for coord in quickcheckcenter)
        quickchecksum = sum(bool(visited_places[coord]) for coord in quickcheck)
        # if(quickchecksum==len(quickcheck) and quickcheckcentersum==len(quickcheckcenter)):
        #     if (PREVIEW):
        #         screen.blit(outlines, (0, 0))
        #         refresh()
        #
        #     print("Visited all neighbours")
        # return True, visited_places
    if (PREVIEW):
        screen.blit(outlines, (0, 0))
        refresh()
    visits_sum = sum(bool(place) for place in visited_places.values())
    visited_ratio = visits_sum / len(visited_places)
    if (quickchecksum == len(quickcheck) and quickcheckcentersum == len(quickcheckcenter)):
        visited_ratio = 1
    if (visited_ratio > PICTURE_TRESHOLD):
        print("Visits result: %i/%i" % (visits_sum, len(visited_places)))
    return visited_ratio, visited_places


def area_explore(tiling, net, startcase, startface, startorientation, mapping, sp1, sp2, polyname,
                 area=(-100, -100, 900, 900), area2=(-25, -25, 825, 825), EDGESIZE=50, precision=7):
    global PAUSE_AT_BEGINNING
    # print(PAUSE)
    # input()
    if (PAUSE_AT_BEGINNING):
        pygame.time.wait(PAUSE_AT_BEGINNING)
        PAUSE_AT_BEGINNING = False
    TIMERSTART = time()
    if (CHECK_UNUSED_FACES and LIMIT_TO_ROLLING_PAIRS):
        faces = set(net.keys())
    if (PREVIEW):
        previewcounter = 0
        if (PREVIEW_TILINGNAME or PREVIEW_POLYNAME):
            text = pygame.font.SysFont(None, 30).render(
                (tilingname + "    ") * PREVIEW_TILINGNAME + polyname * PREVIEW_POLYNAME, True, (0, 0, 0),
                (255, 255, 255))
            titlecard = text.copy()
            titlecard.fill((255, 255, 255))
            titlecard.blit(text, (0, 0))
    visits = [(startface, startcase, startorientation, sp1, sp2)]
    "mapping= visited areas[center points: (polygon, cell number)]"
    visited_places = {coord: [] for coord in mapping.keys()}
    if (QUIT_PREVIEW_EARLY):
        edgeadd = 0
    else:
        edgeadd = EDGESIZE / 2
    poly_compatibility = set(len(neigh) for neigh in net.values())
    # print(mapping)
    max_visitable = sum((area2[0] - edgeadd < ccenter[0] < area2[2] + edgeadd) and (
            area2[1] - edgeadd < ccenter[1] < area2[3] + edgeadd) for ccenter in visited_places if
                        (len(mapping[ccenter][0]) in poly_compatibility))
    once = True
    while (visits):
        # print(len(visits))
        visited = sum(bool(visited_places[ccenter]) for ccenter in visited_places
                      if ((area2[0] - edgeadd < ccenter[0] < area2[2] + edgeadd) and (
                area2[1] - edgeadd < ccenter[1] < area2[3] + edgeadd)))
        if (visited == max_visitable):
            print("Visited max visitable space")
            break
        face, case, orientation, p1, p2 = visits.pop(0)

        # print(len(net[face]),len(tiling[case]))
        # print(net[face],tiling[case])
        if (len(net[face]) != len(tiling[case])):
            #     if(PREVIEW):
            #         # cface = xgon(len(net[face]), p1, p2)
            #         # drawtemp(cface,(0,0,0),outline=1)
            #         refresh()
            # if(SLOW):
            #    wait_for_input()
            "can't explore this"
            continue
        cface = xgon(len(net[face]), p1, p2)
        ccenter = list(floatcenterpoint(cface))
        ccenter = int(round(ccenter[0] / precision) * precision), int(round(ccenter[1] / precision) * precision)
        # cannot do [0][1] because list unhashable
        if not (area[0] < ccenter[0] < area[2]) or not (area[1] < ccenter[1] < area[3]):
            continue  # out of screen
        if (ccenter not in visited_places):
            print("Place not mapped exception:", ccenter)
            continue

        if (OPTIMISE_SYMMETRIES):
            face, orientation = canon_fo(polyname, face, orientation)
            # face = findPolySymmetries.canon_face(face, FaceSym)

        if (case, face, orientation, convertToTuples(cface)) in visited_places[ccenter]:
            # if (PREVIEW):
            # screen.fill((255,255,255)
            # drawtemp(cface,(0,255,0),2)
            # # drawdir(p1,p2)
            # refresh()
            # screen.blit(outlines, (0, 0))
            # if(SLOW):
            #     wait_for_input()
            continue  # already visited

        visited_places[ccenter].append((case, face, orientation, convertToTuples(cface)))
        #print(sum(bool(val) for val in visited_places.values()))
        if (CHECK_UNUSED_FACES and LIMIT_TO_ROLLING_PAIRS):
            faces -= {face}
            if not (faces):
                print("No faces")
                return True, visited_places

        if (PREVIEW):
            if (COLOR_GRADATION):
                grade = len(visited_places[ccenter])
                color = (min(int(255 / grade) + min(max(0, grade * 32 - 255 - 128 - 10 * 32), 128), 255),
                         min(255, max(0, grade * 16 - 192 - 10 * 16 - max(0, grade * 2 - 70 * 2))),
                         max(0, min(255, grade * 12 - 10 * 12) - max(0, grade * 3 - 40 * 3)))
                colorlinks = [(256, 0, -32), (-128, 0, 256), (0, 256 + 64, 128), (256, 64, 128), (256, 256, 0),
                              (28, 145, 48)]
                grade -= 1
                steps = 6 + 18 * CHECK_UNUSED_FACES

                delta = (grade % steps) / steps
                gamma = 1 - delta
                c1 = int(grade // steps) % len(colorlinks)
                c2 = (c1 + 1) % len(colorlinks)
                color = tuple(min(255, max(0, int(value2 * delta + value1 * gamma))) for value1, value2 in
                              zip(colorlinks[c1], colorlinks[c2]))

                try:
                    drawtemp(cface, color)
                except Exception as e:
                    print(color)
                    raise e
            else:
                if (len(visited_places[ccenter]) == 1):
                    # screen.fill((255,255,255))
                    drawtemp(cface, (255, 0, 0))

        # cface = cface[orientation:] + cface[:orientation]
        cface = cface
        neighbours_faces = net[face]
        neighbours_faces = neighbours_faces[orientation:] + neighbours_faces[:orientation]
        # align with cell
        # print(visits)
        # print(face,net[face], neighbours_faces)
        if (once):
            for index, nextcellid in enumerate(tiling[case]):
                nextcell, id = nextcellid
                # print(face,neighbours_faces)
                # print(case,tiling[case])
                nextface = neighbours_faces[index]  # aligned with cell
                if (len(net[nextface]) != len(tiling[nextcell])):
                    continue

                # coorientation = co_orient_face(net,face,nextface,tiling,case,nextcellid)
                face_shift = net[nextface].index(face)
                case_shift = case_match(tiling, case, nextcellid)
                # Create a stub nface at the edge of the current face
                nextface_stub = xgon(len(net[nextface]), cface[(index + 1) % len(cface)], cface[index])
                pa, pb = nextface_stub[-case_shift], nextface_stub[(-case_shift + 1) % len(nextface_stub)]

                # visits.append((nextface, nextcell, -case_shift + face_shift, pa, pb))

                # drawtemp(nextface_stub, (255, 255, 0), 10)
                # refresh()
                #
                nextorientation = (-case_shift + face_shift) % len(nextface_stub)
                nextcenter = list(floatcenterpoint(nextface_stub))
                nextcenter = int(round(nextcenter[0] / precision) * precision), int(
                    round(nextcenter[1] / precision) * precision)
                if (nextcenter in visited_places and len(visited_places[nextcenter]) == 0):
                    if (PREVIEW):
                        if (CHECK_UNUSED_FACES):
                            drawtemp(nextface_stub, (0, 0, 0), 0)
                        elif PREVIEWPERIODICITY:
                            drawtemp(nextface_stub, (255, 255, 0), 0)
                        # refresh() #wait for periodicity
                    if (INSERT_FILL):
                        visits.insert(0, (nextface, nextcell, nextorientation, pa, pb))
                    else:
                        visits.append((nextface, nextcell, nextorientation, pa, pb))
                else:
                    visits.append((nextface, nextcell, nextorientation, pa, pb))
                #     # Reorient it to fit the tile
                #     visits.insert(0,(nextface, nextcell, -case_shift+face_shift, pa, pb))
                # else:
                #     # Reorient it to fit the tile
                #     visits.append((nextface, nextcell, -case_shift+face_shift, pa, pb))

                # drawdir(pa,pb)
        # once=False
        # print(visits)
        if (PREVIEW):
            previewcounter += 1
            if (PREVIEWPERIODICITY and previewcounter % PREVIEWPERIODICITY == 0):
                if (PREVIEW_POLYNAME or PREVIEW_TILINGNAME):
                    screen.blit(titlecard, (0, 0))
                refresh()

                screen.blit(outlines, (0, 0))
        if (TIMERSTART + TIME_LIMIT < time() and TIME_LIMIT > 0):
            if (PREVIEW_POLYNAME or PREVIEW_TILINGNAME):
                screen.blit(titlecard, (0, 0))
            refresh()
            return True, visited_places

        # if(PREVIEW and SLOW):
        # wait_for_input()
    # print(visits)
    # input("%i visits left"%len(visits))

    if (PREVIEW):
        screen.blit(outlines, (0, 0))
        if (PREVIEW_POLYNAME or PREVIEW_TILINGNAME):
            screen.blit(titlecard, (0, 0))
        refresh()
    visited = sum(bool(visited_places[ccenter]) for ccenter in visited_places
                  if (((area2[0] - edgeadd < ccenter[0] < area2[2] + edgeadd) and (
            area2[1] - edgeadd < ccenter[1] < area2[3] + edgeadd))))
    # if ((area2[0] < ccenter[0] < area2[2]) and (area2[1] < ccenter[1] < area2[3])))
    if (
            TIMERSTART + TIME_LIMIT > time() and TIME_LIMIT > 0 and visited / max_visitable > PICTURE_TRESHOLD and WAIT_AT_END and visited > 4):
        if (WAIT_AT_END):
            pygame.time.wait(int((TIMERSTART + TIME_LIMIT - time()) * WAIT_AT_END * 1000))
        else:
            pygame.time.wait(int((TIMERSTART + TIME_LIMIT - time()) * visited / max_visitable) * 1000)

    if (visited < max_visitable):
        # print("Could not visit everything: %s/%i"%(visited,max_visitable))
        if (visited > 2):
            print("Could not visit everything: %s/%i" % (visited, max_visitable),
                  "(c%i f%i o%i)" % (startcase, startface, startorientation))
            visited_places = {center: visitors for center, visitors in visited_places.items() if visitors}
            return visited / max_visitable, visited_places
        # print("failure")
        return False, visited_places
    else:
        print("Visited everything: %s/%i" % (visited, max_visitable))
        return True, visited_places


progress_tiling = None
progress_poly = None
progress_counter = None
progress_skip = 0

biggest_picture = -1

if __name__ == "__main__":
    if (LOAD_PROGRESS):
        try:
            prog = open(progressfile)
            progress = [x.strip() for x in prog.readlines()]
            progress_tiling = progress.pop(0)
            progress_poly = progress.pop(0)
            progress_counter = int(progress.pop(0))
            progress_skip = int(progress.pop(0))
        except:
            pass
        print("Skip current=", args.skip_current)
        if (args.skip_current):
            skip_pairs.append((progress_tiling, progress_poly))
    folder = outputfolder("_results", "exploration_results")

    start_timestamp = make_timestamp()
    filename = folder + "exploration_logs" + start_timestamp + ".txt"
    secondfolder = outputfolder("_results", "exploration_results", "partial_coverage")
    secondfilename = secondfolder + start_timestamp + ".txt"
    # file = open(filename,"w")
    # file.close()
    counter = 0

    successful_pairs = set()
    SKIP_IF_SUCCESSFUL = True

    area = (-200, -200, 1000, 1000)
    area2 = (0, 0, 800, 800)
    xx = (area[0] + area[2]) / 2
    yy = (area[1] + area[3]) / 2
    p1 = RollyPoint(xx, yy)
    EDGESIZE = 50
    p2 = RollyPoint(xx + EDGESIZE, yy)
    precision = 7

    last_mapping = "", 0

    for tilingname in all_tilings_names:
        if (LOAD_PROGRESS and progress_tiling != None):
            if (progress_tiling != tilingname):
                continue
            else:
                progress_tiling = None
        # Skip to
        tiling = all_tilings[tilingname]
        for polyname in all_nets_names:
            result = 0
            biggest_picture = -1
            if (LIMIT_TO_SHOWCASE):
                tilingname, polyname = showcase.pop(0)
                tiling = all_tilings[tilingname]
            if (TESSELLATION_POLYHEDRON):
                if (polyname != tilingname):
                    continue

            if (LOAD_PROGRESS and progress_poly != None):
                if (progress_poly != polyname):
                    continue
                else:
                    progress_poly = None
                    resume_counter = progress_counter
            # Skip to
            net = all_nets[polyname]

            if (EXPLORATION_SPACE == NSPACE):
                mapping = None

            skip_pair = False
            if (SKIP_NOTFULL):
                cellsizes = set(len(neigh) for neigh in tiling.values())
                facesizes = set(len(neigh) for neigh in net.values())
                for cellsize in cellsizes:
                    if cellsize not in facesizes:
                        skip_pair = True
                        print("(%i)" % counter + "Skipping", (tilingname, polyname),
                              "as the tiling has a face with %i sides which is not present in the net and --skipnotfull=%i" % (
                                  cellsize, SKIP_NOTFULL))
                        break

            if (LIMIT_TO_ROLLING_PAIRS and ((tilingname, polyname) not in winning_pairs)):
                print("(%i)" % counter + "Skipping not winning pair", (tilingname, polyname))
                skip_pair = True

            if (skip_pair == False):
                print("(%i)%sExploring the tiling %s with the polyhedron %s" % (
                    counter, make_timestamp(), tilingname, polyname), flush=True)

            exploration_results = outputfolder("_results", "exploration_results")
            # Filter out repetitive faces and orientations to the bare essentials
            # if(polyname!="snub_dodecahedron" and )
            # else:
            faces = list()
            # FaceSym = None
            # if(OPTIMISE_SYMMETRIES):
            #     FaceSym = findPolySymmetries.generate_face_sym(net)
            #     print("...")
            #     print(FaceSym)
            # else:
            # print("...")
            # FFOO = generate_FFOO_sym(net)
            # for face in sorted(net):
            #     if(OPTIMISE_SYMMETRIES):
            #         f = findPolySymmetries.canon_face(face,FaceSym)
            #         if f not in faces:
            #             faces.append(f)
            #     else:
            #         faces.append(face)

            faceori = set()
            for face in sorted(net):
                for orientation in range(len(net[face])):
                    # if (OPTIMISE_SYMMETRIES): Doesn't change the visited faces thing
                    faceori.add(canon_fo(polyname, face, orientation))
                    # faceori.append((face,orientation))
            # Main loop
            explored_canon_cfo = set()
            explored_canon_cells = set()
            for case in (CHECK_ALL_CELLS and tiling or [0]):
                # make an algo that chooses better the only tile
                if (EXPLORATION_SPACE == SCREENSPACE):
                    # if(last_mapping != tilingname): #need something to align p1, p2 with the starting tile in the right orientation
                    mapping = None
                for face, orientation in sorted(faceori):
                    counter += 1
                    if (LOAD_PROGRESS and progress_skip > 0):
                        progress_skip -= 1
                        continue
                    if (resume_counter >= counter):
                        continue
                    if (SKIP_IF_SUCCESSFUL and (tilingname, polyname) in successful_pairs):
                        continue
                    if ((tilingname, polyname) in skip_pairs):
                        continue
                    if (LIMIT_TO_ROLLING_PAIRS and skip_pair):
                        continue
                    if (SKIP_NOTFULL and skip_pair):
                        continue
                    canon_cell = canon_co(tilingname, case, orientation)
                    if canon_cell != None:
                        canon_cfo = canon_cell + (face,)
                        if canon_cfo in explored_canon_cfo:
                            # print("CFO already explored")
                            continue
                        if canon_cfo in explored_canon_cells:
                            # print("Tiling symmetry already explored")
                            continue
                        explored_canon_cells.add(canon_cfo)
                    if len(tiling[case]) != len(net[face]):
                        continue
                    if not any(len(net[net[face][index]]) == len(tiling[tiling[case][index][0]]) for index in
                               range(len(tiling[case]))):
                        print("Cannot escape first tile")
                        continue
                    if (mapping == None):
                        if (EXPLORATION_SPACE == SCREENSPACE):
                            print("Regenerating mapping", tilingname)
                            mapping = map_screenspace(tiling, case, area, p1, p2, precision)
                            last_mapping = tilingname
                        else:
                            N = determine_n(tiling, net, polyname)  # ,case,face,orientation)
                            # continue
                            mapping = map_nspace(tiling, case, area, p1, p2, precision, N)
                        if (PREVIEW):
                            outlines.fill((255, 255, 255, 0))
                            draw_background(outlines, mapping)
                    if (PREVIEW):
                        screen.fill((255, 255, 255))
                        screen.blit(outlines, (0, 0))
                    # ------------Run this with custom values if you want to without FFOO and FaceSym-----------
                    # result, visits = (area_explore(tiling,net,case,face,orientation,FFOO=FFOO,FaceSym=FaceSym))
                    # ------------------------------------------------------------------------------------------
                    if EXPLORATION_SPACE == SCREENSPACE:
                        result, visits = (
                            area_explore(tiling, net, case, face, orientation, mapping, p1, p2, polyname=polyname,
                                         area=area, area2=area2))
                    else:
                        result, visits = n_explore(tiling, net, case, face, orientation, mapping, p1, p2, polyname,
                                                   precision)
                    # print(result)
                    # ,FaceSym=FaceSym))

                    # Ouptut result
                    if (type(visits) == dict):
                        print(visits)
                        for visitor in visits.values():
                            for c, f, o, poly in visitor:
                                f, o = canon_fo(polyname, f, o)
                                c, o = canon_co(tilingname, c, o)
                                explored_canon_cfo.add((c, f, o))
                    if (PREVIEW and not (PREVIEW_POLYNAME or PREVIEW_TILINGNAME)):
                        screen.blit(outlines, (0, 0))
                        refresh()

                    if (result == True):
                        if (SKIP_IF_SUCCESSFUL):
                            print("Skipping possible other positions in this pair")
                        outputfilename = filename
                        keyword = "total"
                        if (CHECK_UNUSED_FACES):
                            unused = get_unused_faces(visits, net, polyname) or None
                        else:
                            unused = None
                    elif not (visits is None):
                        outputfilename = secondfilename
                        keyword = "partial"
                    if (result == True):
                        out = ""
                        out += ("-" * 16 + make_timestamp() + "Resume_counter: %i" % (counter) + "-" * 16) + "\n"
                        out += ("Tiling: %s\nPolyhedron: %s" % (tilingname, polyname)) + "\n"
                        out += ("Cell: %i\nFace: %i\nOrientation: %i orientation" % (case, face, orientation))
                        outputfile = open(outputfilename, "a")
                        outputfile.write(out + "\n")
                        outputfile.close()
                        print(out, flush=True)

                        if (result and DRAW_ANSWER):
                            filename = exploration_results + str(TEMPORARY_GLOBAL_COUNTER).zfill(
                                2) + " " + polyname + " rolls the " + tilingname + " tiling" + '.png'
                            TEMPORARY_GLOBAL_COUNTER += 1
                            draw_answer(filename, tilingname, polyname, visits, mapping, net, p1, p2, face, orientation,
                                        area2[2], area2[3], unused)
                        successful_pairs.add((tilingname, polyname))

                        outputfile = open(exploration_results + "rollers.txt", "a")
                        if (CHECK_UNUSED_FACES):
                            outputfile.write("%s %s %i %i %i %s\n" % (tilingname, polyname, case, face, orientation,
                                                                      str(unused).replace(" ", "")))
                        else:
                            outputfile.write("%s %s %i %i %i\n" % (tilingname, polyname, case, face, orientation))
                        outputfile.close()
                    if (PREVIEW):
                        refresh()
                    if visits and TAKE_PICKLE:
                        visits_count = len([1 for center, visitors in visits.items() if visitors])
                        pickleFolder = outputfolder("_output","pickle")
                        filename =  pickleFolder+polyname + "[on]" + tilingname + ".pickle"
                        if exists(filename):
                            previous_visit = unpickleThis(filename)
                            previous_count = len([1 for center, visitors in previous_visit.items() if visitors])
                            if(visits_count>previous_count):
                                pickleThis(visits, filename)
                        else:
                            pickleThis(visits,filename)


                    if (visits and TAKE_PICTURES and (result >= PICTURE_TRESHOLD)):
                        coveragetypefolder = outputfolder("_output", "exploration_results", "%s_coverage" % keyword)

                        if (BIGGEST_PICTURE):
                            # input(str(len(visits))+str(biggest_picture))
                            if (visits):
                                visits_count = len([1 for center, visitors in visits.items() if visitors])
                            else:
                                visits_count = 0
                            if (visits_count > biggest_picture):
                                # pygame.image.save(screen,".image_output/bigpics/"+polyname+"[on]"+tilingname+'.png')
                                biggest_picture = visits_count
                                if(PREVIEW):
                                    picturesfolder = outputfolder("_output", "bigpics")
                                    pygame.image.save(screen, picturesfolder + polyname + "[on]" + tilingname + '.png')
                                if(OUTPUT_SVG):
                                    svgfolder = outputfolder("_output", "bigsvgs")
                                    draw_filled_result_svg(svgfolder + polyname + "[on]" + tilingname ,mapping,visits)

                        else:
                            draw_tiling(p1, p2, screen, case, 0, tiling, 1, [(0, 255, 0), (192, 192, 192)])
                            pygame.image.save(screen, coveragetypefolder
                                              + tilingname + "@" + polyname + "@" + keyword
                                              + "@(%i,%i,%i)" % (case, face, orientation) + '.png')
                    if (PREVIEW):
                        screen.fill((255, 255, 255))
                    with open(progressfile, "w") as progress_output:
                        progress_output.write("%s\n%s\n%i" % (tilingname, polyname, counter))

                    if (ROLL_ONLY_ONCE and result >= PICTURE_TRESHOLD):
                        print(result, "picture treshold met")
                        break
                if (ROLL_ONLY_ONCE and result >= PICTURE_TRESHOLD):
                    print(result, "picture treshold met")
                    break
