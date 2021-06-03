"""Roll a shape in a space with a given tiling and starting position
"""
import os
from datetime import datetime
def make_timestamp():
    return datetime.now().strftime("[%Hh%Mm%S]")
from GeometryFunctions import *
from tiling_dicts.archimedean_tilings import archimedean_tilings
from tiling_dicts.platonic_tilings import platonic_tilings
from tiling_dicts.isogonal_tilings import biisogonal_tilings
from poly_dicts.prism_nets import prism_nets
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.johnson_nets import johnson_nets

all_tilings = {**platonic_tilings, **archimedean_tilings, **biisogonal_tilings}
all_nets = {**plato_archi_nets, **johnson_nets, **prism_nets}

all_tilings_names = list(all_tilings.keys()) #if you want to limit to a few, change this line
# all_tilings_names = []
#all_tilings_names=all_tilings_names[all_tilings_names.index("3^3x4^2"):]

all_nets_names = list(all_nets.keys()) #if you want to limit to a few, change this line
# all_nets_names = ["cube"]
#all_nets_names = all_nets_names[all_nets_names.index("cube"):]

resume_counter = -1


from findPolySymmetries import canon_face, canon_fo, generate_FFOO_sym, generate_face_sym


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


def map_screenspace(tiling, startcell, area, p1, p2, precision):
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


def area_explore(tiling, net, startcase, startface, startorientation, visualise=False,
                 FFOO = None, FaceSym = None,
                 area = (-100, -100, 900, 900), area2 = (0, 0, 800, 800), EDGESIZE = 50, precision = 7):
    #The main function to call if you want to use this
    xx = (area[0]+area[2])/2
    yy = (area[1]+area[3])/2
    p1 = RollyPoint(xx,yy)
    p2 = RollyPoint(xx + EDGESIZE, yy)  # 350 300
    # if(FFOO is None):
    #     FFOO = generate_FFOO_sym(net)  # Face-Face-Orientation-Orientation symmetries
    if(FaceSym is None):
        FaceSym = generate_face_sym(net)  # Face-Face-Orientation-Orientation symmetries
    visits = [(startface, startcase, startorientation, p1, p2)]
    mapping = map_screenspace(tiling, startcase, area, p1, p2, precision)
    visited_places = {coord: [] for coord in mapping.keys()}

    while (visits):
        face, case, orientation, p1, p2 = visits.pop()
        if (len(net[face]) != len(tiling[case])):
            "can't explore this"
            continue
        cface = xgon(len(net[face]), p1, p2)
        ccenter = list(floatcenterpoint(cface))
        ccenter = int(round(ccenter[0] / precision) * precision), int(round(ccenter[1] / precision) * precision)
        #cannot do [0][1] because list unhashable
        if not (area[0] < ccenter[0] < area[2]) or not (area[1] < ccenter[1] < area[3]):
            continue
        if (ccenter not in visited_places):
            print("Place not mapped exception:", ccenter)
            continue
        # face, orientation = canon_fo(face, orientation,FaceSym, FFOO)
        face = canon_face(face,FaceSym)
        if (face, orientation) in visited_places[ccenter]:
            continue
        visited_places[ccenter].append((face, orientation))

        cface = cface[orientation:] + cface[:orientation]
        neighbours_faces = net[face]
        neighbours_faces = neighbours_faces[orientation:] + neighbours_faces[:orientation]
        # align with cell

        for index, nextcellid in enumerate(tiling[case]):
            nextcell, id = nextcellid
            nextface = neighbours_faces[index]  # aligned with cell
            if(len(net[nextface])!=len(tiling[nextcell])):
                continue

            coorientation = co_orient_face(net,face,nextface,tiling,case,nextcellid)
            face_shift = net[nextface].index(face)
            # Create a stub nface at the edge of the current face
            nextface_stub = xgon(len(net[nextface]), cface[(index + 1) % len(cface)], cface[index])
            # Reorient it
            pa, pb = nextface_stub[-face_shift], nextface_stub[(-face_shift + 1) % len(nextface_stub)]
            visits.append((nextface, nextcell, coorientation, pa, pb))

    max_visitable = sum((area2[0] < ccenter[0] < area2[2]) and (area2[1] < ccenter[1] < area2[3]) for ccenter in visited_places)
    visited = sum(bool(visited_places[ccenter]) for ccenter in visited_places
        if ((area2[0] < ccenter[0] < area2[2]) and (area2[1] < ccenter[1] < area2[3])))
    if(visited<max_visitable):
        #print("Could not visit everything: %s/%i"%(visited,max_visitable))
        if(visited>1):
            print("Could not visit everything: %s/%i"%(visited,max_visitable), "(c%i f%i o%i)"%(startcase,startface,startorientation))
            visited_places = {center for center,visitors in visited_places.items() if visitors}
            return False, visited_places
        return False, None
    else:
        print("Visited everything: %s/%i"%(visited,max_visitable))
        return True, visited_places

if __name__ == "__main__":
    folder = "exploration_results"+os.sep
    try:os.mkdir(folder)
    except:pass
    start_timestamp = make_timestamp()
    filename = folder+"exploration_logs"+start_timestamp+".txt"
    file = open(filename,"w")
    file.close()
    counter = 0

    successful_pairs = set()
    SKIP_IF_SUCCESSFUL = True

    for tilingname in all_tilings_names:
        tiling = all_tilings[tilingname]
        for polyname in all_nets_names:
            net = all_nets[polyname]
            print(end="(%i)%sExploring the tiling %s with the polyhedron %s" % (counter,make_timestamp(),tilingname, polyname))

            # Filter out repetitive faces and orientations to the bare essentials
            #if(polyname!="snub_dodecahedron" and )
            #else:
            faces = set()
            FaceSym = generate_face_sym(net)
            # FFOO = generate_FFOO_sym(net)
            for face in net:
                faces.add(canon_face(face,FaceSym))
            faceori = set()
            for face in faces:
                for orientation in range(len(net[face])):
                    # faceori.add(canon_fo(face,orientation,FaceSym, FFOO))
                    faceori.add((face,orientation))
            print("...")
            #Main loop
            for face,orientation in faceori:
                for case in tiling:
                    counter+=1
                    if(resume_counter>counter-1):
                        continue
                    if(SKIP_IF_SUCCESSFUL and (tilingname,polyname) in successful_pairs):
                        continue
                    #------------Run this with custom values if you want to without FFOO and FaceSym-----------
                    #result, visits = (area_explore(tiling,net,case,face,orientation,FFOO=FFOO,FaceSym=FaceSym))
                    #------------------------------------------------------------------------------------------
                    result, visits = (area_explore(tiling,net,case,face,orientation))

                    # Ouptut result

                    if(result):
                        #print("Could explore the tiling %s with the polyhedron %s"%(tilingname,polyname))
                        out=""
                        out+=("-"*16+make_timestamp()+"Resume counter: %i"%(counter)+"-"*16) + "\n"
                        out+=("Tiling: %s\nPolyhedron: %s"%(tilingname, polyname)) + "\n"
                        out+=("Cell: %i\nFace: %i\nOrientation: %i orientation"%(case,face,orientation))
                        if(SKIP_IF_SUCCESSFUL):
                            out+=("\nSkipping possible other positions in this pair")
                        file=open(filename,"a")
                        file.write(out+ "\n")
                        file.close()
                        print(out)

                        successful_pairs.add((tilingname,polyname))

                    elif not visits is None:
                        out=""
                        out+=("-"*16+make_timestamp()+"Resume counter: %i"%(counter)+"-"*16) + "\n"
                        out+=("Tiling: %s\nPolyhedron: %s"%(tilingname, polyname)) + "\n"
                        out+=("Cell: %i\nFace: %i\nOrientation: %i orientation"%(case,face,orientation)) + "\n"
                        out+=("Visited cells: %s"%len(visits))
                        secondfilename = folder + "partially_explored_of_interest" + start_timestamp + ".txt"
                        file = open(secondfilename, "a")
                        file.write(out + "\n")
                        file.close()