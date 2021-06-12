"""Roll a shape in a space with a given tiling and starting position
"""
import os
from datetime import datetime
def make_timestamp():
    return datetime.now().strftime("[%Hh%Mm%S]")
from GeometryFunctions import *
from GenPngScreenspaceRoller import draw_answer, draw_background, draw_polygon, wait_for_input, refresh
from tiling_dicts.archimedean_tilings import archimedean_tilings
from tiling_dicts.platonic_tilings import platonic_tilings
from tiling_dicts.isogonal_tilings import biisogonal_tilings
from poly_dicts.prism_nets import prism_nets
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.johnson_nets import johnson_nets
from symmetry_classes.poly_symmetries import poly_symmetries


# import sys, getopt
#
# args = sys.argv[1:]
# try:
#     opts, args = getopt.getopt(args,"Pp:g:c:l:",["forcepreview","preview=","previewgap=","color=","loadprogress="])
# except getopt.GetoptError:
#     print("ScreenspaceRoller.py ")
#     sys.exit(2)

PREVIEW = False
GRADATION = True
PREVIEWPERIODICITY=500
# SLOW=False
OPTIMISE_SYMMETRIES = True
SKIP_NOTFULL = True
LOAD_PROGRESS = True
TAKE_PICTURES = False

CHECK_UNUSED_FACES = False #Will disable symmetry optimisations
CHECK_ALL_CELLS = False

QUIT_PREVIEW_EARLY = True

CHEAT_WINNING = False

winning_pairs = {('3^6;3^2x4x3x4', 'j89'), ('3^6', 'j84'), ('3^6', 'j89'), ('3^2x4x3x4', 'j31'), ('(3^6;3^3x4^2)2', 'j87'), ('(3^6;3^3x4^2)2', 'j89'), ('3^6', 'j87'), ('3x4x6x4', 'j54'), ('(3^6;3^3x4^2)2', 'j50'), ('3^6', 'j13'), ('3^6;3^2x4x3x4', 'j87'), ('3^6;3^2x4x3x4', 'j50'), ('3^6', 'j51'), ('3^6', 'j50'), ('3^6', 'j11'), ('(3^6;3^3x4^2)1', 'j90'), ('3^2x4x3x4', 'j26'), ('3^3x4^2', 'j28'), ('(3^6;3^3x4^2)1', 'j14'), ('(3^6;3^4x6)1', 'j22'), ('(3^6;3^3x4^2)1', 'j10'), ('(3^6;3^4x6)2', 'hexagonal_antiprism'), ('(3^6;3^3x4^2)1', 'j85'), ('(3^6;3^3x4^2)1', 'j88'), ('3^6', 'octahedron'), ('(3^6;3^3x4^2)2', 'j86'), ('3^3x4^2', 'j27'), ('3x4x6x4', 'j56'), ('3^6;3^2x6^2', 'truncated_tetrahedron'), ('3^6', 'j86'), ('4^4', 'j8'), ('3^4x6;3^2x6^2', 'hexagonal_antiprism'), ('3^6;3^2x4x3x4', 'j86'), ('(3^3x4^2;3^2x4x3x4)1', 'j1'), ('(3^6;3^3x4^2)1', 'j16'), ('(3^6;3^3x4^2)1', 'j89'), ('3^3x4^2', 'square_antiprism'), ('4^4', 'j37'), ('3^2x4x3x4', 'j29'), ('(3^6;3^3x4^2)2', 'j90'), ('(3^6;3^3x4^2)1', 'j87'), ('3^6', 'j62'), ('3^6', 'j90'), ('(3^3x4^2;3^2x4x3x4)2', 'j26'), ('(3^6;3^3x4^2)2', 'j10'), ('3^6;3^2x4x3x4', 'j10'), ('3^6;3^2x4x3x4', 'j90'), ('4^4', 'cube'), ('(3^3x4^2;3^2x4x3x4)1', 'j27'), ('3^6', 'j10'), ('(3^6;3^3x4^2)1', 'j50'), ('3^3x4^2', 'j30'), ('(3^6;3^3x4^2)2', 'j85'), ('(3^6;3^3x4^2)2', 'j88'), ('3^6', 'j85'), ('3^6', 'j17'), ('3^2x4x3x4', 'j1'), ('3x6x3x6', 'j65'), ('3^6;3^2x4x3x4', 'j1'), ('3^6', 'j88'), ('3^6;3^2x4x3x4', 'j85'), ('3^6', 'tetrahedron'), ('(3^6;3^3x4^2)1', 'j15'), ('(3^6;3^4x6)1', 'hexagonal_antiprism'), ('3^6', 'icosahedron'), ('3^6', 'j12'), ('3^4x6', 'hexagonal_antiprism'), ('(3^6;3^3x4^2)1', 'j86')}

#Modes
#Roller : OPTIMISE_SYMMETRIES = True, CHECK_ALL_CELLS = False, SKIP_NOTFULL = True, CHECK_UNUSED_FACES = False, QUIT_PREVIEW_EARLY = True
#Perfect Roller: OPTIMISE_SYMMETRIES = False, CHECK_ALL_CELLS = False, SKIP_NOTFULL = True, CHECK_UNUSED_FACES = True, QUIT_PREVIEW_EARLY = False
#Visitor: OPTIMISE_SYMMETRIES = True, CHECK_ALL_CELLS = True, SKIP_NOTFULL = False, QUIT_PREVIEW_EARLY = False


# QUIT_SEARCH_EARLY = False
#
TEMPORARY_GLOBAL_COUNTER = 0

progressfile = "exploration_results/PROGRESS_CHECKPOINT.txt"

#Those don't roll in the whole space but roll in a lot of it, enough to slow down the processing
#Plus they don't have a lot of symmetries to speed things up

skip_pairs = []
#    ("3^6","j87"),("3^6","j88"),("3^6","j89"),("(3^6;3^4x6)1","j87"),("3x4x6x4","j74"),("3x4x6x4","j76"),("3x4x6x4","j81"),
# ("(3^6;3^4x6)1","j88"),
# ("(3^6;3^4x6)1","j89"),("3^4x6","j87"),
# ("(3^6;3^4x6)1","j90"),
# ("(3^6;3^4x6)2","icosahedron"),
# ("(3^6;3^4x6)2","j10"),
# ("(3^6;3^4x6)2","j11"),
# ("(3^6;3^4x6)2","j13"),
# ("(3^6;3^4x6)2","j12"),
# ("(3^6;3^4x6)2","j17"),
# ("3^6;3^2x4x3x4" ,"j78"),
# ("3^6;3^2x4x3x4" ,"j81")
# ]

resume_counter = -1

all_tilings = {**platonic_tilings, **archimedean_tilings, **biisogonal_tilings}
all_nets = {**plato_archi_nets, **johnson_nets, **prism_nets}

#all_nets = {"testnet":{0:[3,4,5,6],3:[0,3,4],4:[0,3,4,5],5:[0,1,2,3,4],6:[0,9,9,9,9,9]}}

all_tilings_names = list(all_tilings.keys()) #if you want to limit to a few, change this line
# all_tilings_names = []
#all_tilings_names=all_tilings_names[all_tilings_names.index("3^3x4^2"):]
# all_tilings_names=all_tilings_names[all_tilings_names.index("4^4"):]
# all_tilings_names=all_tilings_names[all_tilings_names.index("(3^6;3^3x4^2)1"):]

all_nets_names = list(all_nets.keys()) #if you want to limit to a few, change this line
# all_nets_names = ["cube"]
#all_nets_names = all_nets_names[all_nets_names.index("j4"):]
#all_nets_names = all_nets_names[all_nets_names.index("cube"):]
# all_nets_names = all_nets_names[all_nets_names.index("snub_cube"):]
# all_nets_names = all_nets_names[all_nets_names.index("j10"):]
#all_nets_names = all_nets_names[all_nets_names.index("j50"):]

# print(all_tilings_names.index("(3^6;3^4x6)1"),"/",len(all_tilings_names),"    ","(3^6;3^4x6)1")
# print(all_nets_names.index("j87"),"/",len(all_nets_names),"    ","j87")
# exit()

import sys
import argparse
def str2bool(v):
    #https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse/43357954#43357954
    if isinstance(v, bool):
        return v
    if v.lower() in ('yes', 'true', 'True', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'False', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser(description="Roll polyhedrons in tilings, report the results")
parser.add_argument("-f","--skipnotfull", type=int, help="Skip looking when one of the face of the tiling is not in the polyhedron (when the space is not fully explorable). Only look for full rolling. (default=%i)"%SKIP_NOTFULL)
# parser.add_argument("-f","--skippartial", type=int, help="Skip looking when one of the face of the polyhedron is not in the tiling (Partial Roller, when one face of the poly will not be used). (default=%i)"%SKIP_NOTFULL)

parser.add_argument("-p","--preview", type=int, help="En/Disable preview for speed (default="+str(int(PREVIEW))+")")
parser.add_argument("-l","--load", type=int, help="En/Disable progress loading (default="+str(int(LOAD_PROGRESS))
    +")\nDon't forget to backup your PROGRESS_CHECKPOINT.txt file before turning this off!")
parser.add_argument("-c","--color", type=str, help="Choose [single] color or [gradation] for preview (default="
        +["single","gradation"][GRADATION]+")")
parser.add_argument("-s","--prevspeed", type=int, help="How many steps of preview are skipped between refreshes. Bigger number makes the app run faster, smaller number makes the animation prettier. (default=%s)"%PREVIEWPERIODICITY)
parser.add_argument("-t","--picture", type=int, help="Take pictures for every failed step. (default=%i)"%TAKE_PICTURES)
parser.add_argument("-u","--check_unused", type=int, help="Check unused faces for successful search. Disables optimisations. (default=%i)"%CHECK_UNUSED_FACES)
parser.add_argument("-k","--skip_current", action='store_true', help="Skip current face in counter order.")
args = parser.parse_args()

if(len(sys.argv)==1):
    parser.print_help()

if args.preview!=None:
    PREVIEW = args.preview
if args.color!=None:
    GRADATION = ["single","gradation"].index(args.color)
if args.prevspeed!=None:
    PREVIEWPERIODICITY=args.prevspeed
if args.load!=None:
    LOAD_PROGRESS = args.load
if args.skipnotfull!=None:
    SKIP_NOTFULL = args.skipnotfull
if args.picture!=None:
    TAKE_PICTURES = args.picture
if args.check_unused!=None:
    CHECK_UNUSED_FACES = args.check_unused
if(CHECK_UNUSED_FACES):
        OPTIMISE_SYMMETRIES=False

print(args)

if(PREVIEW):
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 800), pygame.DOUBLEBUF)
    screen.fill((255,255,255,255))
    outlines = pygame.Surface((800, 800), pygame.SRCALPHA)
    temp = pygame.Surface((800, 800), pygame.SRCALPHA)


def canon_fo(polyname,face,orientation):
    try:
        symmetries = poly_symmetries[polyname]
        for sym in symmetries:
            if (face,orientation) in sym:
                #print("Found a symmetry!")
                return min(sym)
    except:
        print("No symmetry info for this poly")
    return face, orientation
#from findPolySymmetries import canon_face, canon_fo, generate_FFOO_sym, generate_face_sym
import findPolySymmetries

def cell_match(tiling, previous_case, newcaseid):
    return case_match(tiling, previous_case, newcaseid)
def case_match(tiling, previous_case, newcaseid):
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
    print(previous_case,newcaseid,tiling)

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
        for face,orientation in res:
            # try:faces.remove(canon_fo(polyname,face,orientation)[0])
            try:faces.remove(face)
            except:pass
        if not faces:
            return faces
    return faces


def map_screenspace(tiling, startcell, area, p1, p2, precision):
    "visited areas[center points: (polygon, cell number)]"
    visited_areas = dict()
    visits = [(startcell, p1, p2)]
    while (visits):
        cell, p1, p2 = visits.pop()
        cface = xgon(len(tiling[cell]), p1, p2)
        ccenter = tuple(floatcenterpoint(cface))
        ccenter = int(round(ccenter[0] / precision) * precision), int(round(ccenter[1] / precision) * precision)

        if not (area[0] < ccenter[0] < area[2]) or not (area[1] < ccenter[1] < area[3]):
            continue
        if (ccenter in visited_areas):
            continue

        visited_areas[ccenter] = (cface, cell)  # later for drawing

        for index, nextcellid in enumerate(tiling[cell]):
            cell_shift = cell_match(tiling, cell, nextcellid)
            nextcell, id = nextcellid
            # Create a stub ncface at the edge of the current cface
            nextface_stub = xgon(len(tiling[nextcell]), cface[(index + 1) % len(cface)], cface[index])
            # Reorient it
            pa, pb = nextface_stub[-cell_shift], nextface_stub[(-cell_shift + 1) % len(nextface_stub)]
            visits.append((nextcell, pa, pb))
    return visited_areas

def drawtemp(points,color,outline=0):
    temp.fill((255, 255, 255, 0))
    draw_polygon(temp, color, points, outline)
    screen.blit(temp, (0, 0))

def drawdir(p1,p2,color=(128,128,128)):
    points = triangle(p1,p2)
    drawtemp(points,color,3)


def area_explore(tiling, net, startcase, startface, startorientation, mapping, polyname,
                 area = (-100, -100, 900, 900), area2 = (-25, -25, 825, 825), EDGESIZE = 50, precision = 7):
    #The main function to call if you want to use this
    xx = (area[0]+area[2])/2
    yy = (area[1]+area[3])/2
    p1 = RollyPoint(xx,yy)
    p2 = RollyPoint(xx + EDGESIZE, yy)  # 350 300
    if(CHECK_UNUSED_FACES and CHEAT_WINNING):
        faces = set(net.keys())

    if(PREVIEW):
        previewcounter=0
    # if(FFOO is None):
    #     FFOO = generate_FFOO_sym(net)  # Face-Face-Orientation-Orientation symmetries
    #if(FaceSym is None):
        #FaceSym = findPolySymmetries.generate_face_sym(net)  # Face-Face-Orientation-Orientation symmetries
    visits = [(startface, startcase, startorientation, p1, p2)]
    #mapping = map_screenspace(tiling, startcase, area, p1, p2, precision)
    "mapping= visited areas[center points: (polygon, cell number)]"
    visited_places = {coord: [] for coord in mapping.keys()}
    max_visitable = sum((area2[0] < ccenter[0] < area2[2]) and (area2[1] < ccenter[1] < area2[3]) for ccenter in visited_places)
    once = True
    while (visits):
        #print(len(visits))
        if(QUIT_PREVIEW_EARLY):
            edgeadd = 0
        else:
            edgeadd = EDGESIZE/2
        visited = sum(bool(visited_places[ccenter]) for ccenter in visited_places
            if ((area2[0]-edgeadd < ccenter[0] < area2[2]+edgeadd) and (area2[1]-edgeadd < ccenter[1] < area2[3]+edgeadd)))
        if(visited==max_visitable):
            break
        face, case, orientation, p1, p2 = visits.pop(0)


        if (len(net[face]) != len(tiling[case])):
        #     if(PREVIEW):
        #         # cface = xgon(len(net[face]), p1, p2)
        #         # drawtemp(cface,(0,0,0),outline=1)
        #         refresh()
                #if(SLOW):
                #    wait_for_input()
            "can't explore this"
            continue
        cface = xgon(len(net[face]), p1, p2)
        ccenter = list(floatcenterpoint(cface))
        ccenter = int(round(ccenter[0] / precision) * precision), int(round(ccenter[1] / precision) * precision)
        #cannot do [0][1] because list unhashable
        if not (area[0] < ccenter[0] < area[2]) or not (area[1] < ccenter[1] < area[3]):
            continue #out of screen
        if (ccenter not in visited_places):
            print("Place not mapped exception:", ccenter)
            continue #weird error

        if(OPTIMISE_SYMMETRIES):
            face, orientation = canon_fo(polyname,face, orientation)
            # face = findPolySymmetries.canon_face(face, FaceSym)

        if (face, orientation) in visited_places[ccenter]:
            # if (PREVIEW):
                # screen.fill((255,255,255)
                # drawtemp(cface,(0,255,0),2)
                #drawdir(p1,p2)
                #refresh()
                # screen.blit(outlines, (0, 0))
                # if(SLOW):
                #     wait_for_input()
            continue #already visited

        visited_places[ccenter].append((face, orientation))

        if(CHECK_UNUSED_FACES and CHEAT_WINNING):
            faces-= {face}
            if not(faces):
                return True, visited_places

        if(PREVIEW):
            if(GRADATION):
                grade = len(visited_places[ccenter])
                color = (min(int(255/grade)+min(max(0,grade*32-255-128-10*32),128),255),min(255,max(0,grade*16-192-10*16-max(0,grade*2-70*2))),max(0,min(255,grade*12-10*12)-max(0,grade*3-40*3)))

                try:
                    drawtemp(cface,color)
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
        if(once):
            for index, nextcellid in enumerate(tiling[case]):
                nextcell, id = nextcellid
                nextface = neighbours_faces[index]  # aligned with cell
                if(len(net[nextface])!=len(tiling[nextcell])):
                    continue

                #coorientation = co_orient_face(net,face,nextface,tiling,case,nextcellid)
                face_shift = net[nextface].index(face)
                case_shift = case_match(tiling,case,nextcellid)
                # Create a stub nface at the edge of the current face
                nextface_stub = xgon(len(net[nextface]), cface[(index + 1) % len(cface)], cface[index])

                # Reorient it to fit the tile
                pa, pb = nextface_stub[-case_shift], nextface_stub[(-case_shift + 1) % len(nextface_stub)]
                visits.append((nextface, nextcell, -case_shift+face_shift, pa, pb))


                # if(PREVIEW):
                #     drawtemp(nextface_stub,(0,255,255),1)
                    #drawdir(pa,pb)
        # once=False
        # print(visits)
        if(PREVIEW):
            previewcounter+=1
            if(previewcounter%PREVIEWPERIODICITY==0):
                refresh()
                screen.blit(outlines, (0, 0))


        # if(PREVIEW and SLOW):
           #wait_for_input()



    visited = sum(bool(visited_places[ccenter]) for ccenter in visited_places
        if ((area2[0] < ccenter[0] < area2[2]) and (area2[1] < ccenter[1] < area2[3])))
    if(visited<max_visitable):
        #print("Could not visit everything: %s/%i"%(visited,max_visitable))
        if(visited>2):
            print("Could not visit everything: %s/%i"%(visited,max_visitable), "(c%i f%i o%i)"%(startcase,startface,startorientation))
            visited_places = {center for center,visitors in visited_places.items() if visitors}
            return False, visited_places
        #print("failure")
        return False, None
    else:
        print("Visited everything: %s/%i"%(visited,max_visitable))
        return True, visited_places

progress_tiling = None
progress_poly = None
progress_counter = None
progress_skip = 0

if __name__ == "__main__":
    if(LOAD_PROGRESS):
        try:
            prog=open(progressfile)
            progress = [x.strip() for x in prog.readlines()]
            progress_tiling = progress.pop(0)
            progress_poly = progress.pop(0)
            progress_counter = int(progress.pop(0))
            progress_skip = int(progress.pop(0))
        except:
            pass
        print("Skip current=",args.skip_current)
        if (args.skip_current):
            skip_pairs.append((progress_tiling,progress_poly))
    folder = "exploration_results"+os.sep
    try:os.mkdir(folder)
    except:pass
    start_timestamp = make_timestamp()
    filename = folder+"exploration_logs"+start_timestamp+".txt"
    try:os.mkdir(folder+"/partial_coverage")
    except:pass
    secondfilename = "exploration_results/partial_coverage/" + start_timestamp + ".txt"
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
    p2 = RollyPoint(xx + 50, yy)


    for tilingname in all_tilings_names:
        if(LOAD_PROGRESS and progress_tiling!=None):
            if(progress_tiling!=tilingname):
                continue
            else:
                progress_tiling=None
        #Skip to
        tiling = all_tilings[tilingname]

        for polyname in all_nets_names:
            if(LOAD_PROGRESS and progress_poly!=None):
                if(progress_poly!=polyname):
                    continue
                else:
                    progress_poly=None
                    resume_counter=progress_counter
            #Skip to
            net = all_nets[polyname]



            skip_pair = False
            if (SKIP_NOTFULL):
                cellsizes = set(len(neigh) for neigh in tiling.values())
                facesizes = set(len(neigh) for neigh in net.values())
                for cellsize in cellsizes:
                    if cellsize not in facesizes:
                        skip_pair = True
                        print("(%i)"%counter+"Skipping",(tilingname, polyname),"as the tiling has a face with %i sides which is not present in the net and --skipnotfull=%i"%(cellsize,SKIP_NOTFULL))
                        break

            if (CHEAT_WINNING and ((tilingname, polyname) not in winning_pairs)):
                print("(%i)"%counter+"Skipping not winning pair", (tilingname, polyname))
                skip_pair = True

            if(skip_pair==False):
                print("(%i)%sExploring the tiling %s with the polyhedron %s" % (
                counter, make_timestamp(), tilingname, polyname), flush=True)
            # Filter out repetitive faces and orientations to the bare essentials
            #if(polyname!="snub_dodecahedron" and )
            #else:
            faces = list()
            # FaceSym = None
            # if(OPTIMISE_SYMMETRIES):
            #     FaceSym = findPolySymmetries.generate_face_sym(net)
            #     print("...")
            #     print(FaceSym)
            # else:
            #print("...")
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
                    faceori.add(canon_fo(polyname,face,orientation))
                    # faceori.append((face,orientation))
            #Main loop
            for case in (CHECK_ALL_CELLS and tiling or [0]):
                #make an algo that chooses better the only tile
                screenspace = None
                for face,orientation in faceori:
                    counter+=1
                    if(LOAD_PROGRESS and progress_skip>0):
                        progress_skip-=1
                        continue
                    if(resume_counter>=counter):
                        continue
                    if(SKIP_IF_SUCCESSFUL and (tilingname,polyname) in successful_pairs):
                        continue
                    if((tilingname,polyname) in skip_pairs):
                        continue
                    if(CHEAT_WINNING and skip_pair):
                        continue
                    if(SKIP_NOTFULL and skip_pair):
                        continue
                    if (PREVIEW):
                        screen.blit(outlines,(0,0))

                    if(screenspace==None):
                        screenspace = map_screenspace(tiling, case, area, p1, p2, 7)
                        if (PREVIEW):
                            outlines.fill((255, 255, 255, 0))
                            draw_background(outlines, screenspace)
                    #------------Run this with custom values if you want to without FFOO and FaceSym-----------
                    #result, visits = (area_explore(tiling,net,case,face,orientation,FFOO=FFOO,FaceSym=FaceSym))
                    #------------------------------------------------------------------------------------------
                    result, visits = (area_explore(tiling,net,case,face,orientation,screenspace,polyname=polyname,
                                                   area=area,area2=area2))
                    # ,FaceSym=FaceSym))

                    # Ouptut result
                    if(PREVIEW):
                        refresh()

                    if(result):
                        if(SKIP_IF_SUCCESSFUL):
                            print("Skipping possible other positions in this pair")
                        outputfilename =filename
                        keyword = "total"
                        if(CHECK_UNUSED_FACES):
                            unused = get_unused_faces(visits, net, polyname) or None
                        else:
                            unused = None
                    elif not (visits is None):
                        outputfilename = secondfilename
                        keyword = "partial"
                    if(result):
                        out=""
                        out+=("-"*16+make_timestamp()+"Resume_counter: %i"%(counter)+"-"*16) + "\n"
                        out+=("Tiling: %s\nPolyhedron: %s"%(tilingname, polyname)) + "\n"
                        out+=("Cell: %i\nFace: %i\nOrientation: %i orientation"%(case,face,orientation))
                        outputfile = open(outputfilename,"a")
                        outputfile.write(out+ "\n")
                        outputfile.close()
                        print(out,flush=True)
                        if(result and TAKE_PICTURES):
                            filename="exploration_results/"+str(TEMPORARY_GLOBAL_COUNTER).zfill(2)+" "+polyname+" rolls the "+tilingname+" tiling"+'.png'
                            TEMPORARY_GLOBAL_COUNTER+=1
                            draw_answer(filename,tilingname,polyname,visits,screenspace,net,p1,p2,face,orientation,area2[2],area2[3])
                        successful_pairs.add((tilingname,polyname))

                        outputfile = open("exploration_results/rollers.txt","a")
                        if(CHECK_UNUSED_FACES):
                            outputfile.write("%s %s %i %i %i %s\n"%(tilingname,polyname,case,face,orientation,
                                                                    str(unused).replace(" ","")))
                        else:
                            outputfile.write("%s %s %i %i %i\n"%(tilingname,polyname,case,face,orientation))
                        outputfile.close()
                    if(PREVIEW):
                        refresh()
                        if(visits and TAKE_PICTURES):
                            try:os.mkdir("exploration_results/%s_coverage/"%keyword)
                            except:pass
                            pygame.image.save(screen,"exploration_results/%s_coverage/"%keyword
                                              +tilingname+"@"+polyname+"@"+keyword
                                              +"@(%i,%i,%i)"%(case,face,orientation)+'.png')
                    if(PREVIEW):
                        screen.fill((255,255,255))
                    try:os.mkdir("exploration_results")
                    except:pass
                    with open("exploration_results/PROGRESS_CHECKPOINT.txt","w") as progress_output:
                        progress_output.write("%s\n%s\n%i"%(tilingname,polyname,counter))