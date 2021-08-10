from statistics import mean

from GeometryFunctions import xgon, roundedcenter
from RollyPoint import RollyPoint
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
    print(previous_case,newcaseid,tiling)

def yield_borders(tiling, startcell, p1, p2, precision=7):
    visited_areas = list()
    visits = [(startcell, p1, p2)]
    while (visits):
        cell, p1, p2 = visits.pop(0)
        cgon = xgon(len(tiling[cell]), p1, p2)
        ccenter = roundedcenter(cgon, precision)
        if (ccenter in visited_areas):
            continue
        visited_areas.append(ccenter)

        for index, nextcellid in enumerate(tiling[cell]):
            cell_shift = cell_match(tiling, cell, nextcellid)
            nextcell, id = nextcellid
            # Create a stub ncgon at the edge of the current cgon
            nextcgon = xgon(len(tiling[nextcell]), cgon[(index + 1) % len(cgon)], cgon[index])
            # Reorient it
            pa, pb = nextcgon[-cell_shift], nextcgon[(-cell_shift + 1) % len(nextcgon)]

            if id != 0 or (id == 0 and nextcell == cell):
                # cellgon = cgon[index:]+cgon[:index]
                yield (cell, nextcellid, cgon, nextcgon, pa, pb)
            else:
                visits.append((nextcell, pa, pb))


"""
def yield_outsides(tiling,startcell,p1,p2,precision=7):
    visited_areas = list()
    visits = [(startcell, p1, p2)]
    outsides = list()
    while (visits):
        cell, p1, p2 = visits.pop(0)
        cgon = xgon(len(tiling[cell]), p1, p2)
        ccenter = roundedcenter(cgon,precision)
        if (ccenter in visited_areas):
            continue
        visited_areas.append(ccenter)

        for index, nextcellid in enumerate(tiling[cell]):
            cell_shift = cell_match(tiling, cell, nextcellid)
            nextcell, id = nextcellid
            # Create a stub ncgon at the edge of the current cgon
            nextcgon = xgon(len(tiling[nextcell]), cgon[(index + 1) % len(cgon)], cgon[index])
            # Reorient two points of it
            pa, pb = nextcgon[-cell_shift], nextcgon[(-cell_shift + 1) % len(nextcgon)]

            if id != 0 or (id == 0 and nextcell == cell):
                nextcenter = roundedcenter(nextcgon,precision)
                if nextcenter in outsides:
                    continue
                outsides.append(nextcenter)
                #cellgon = cgon[index:]+cgon[:index]
                yield (cell,nextcellid, cgon, nextcgon, pa, pb)
            else:
                visits.append((nextcell, pa, pb))
"""


def yield_insides(tiling, startcell, p1, p2, precision=7):
    visited_areas = list()
    visits = [(startcell, p1, p2)]
    while (visits):
        cell, p1, p2 = visits.pop(0)
        cgon = xgon(len(tiling[cell]), p1, p2)
        ccenter = roundedcenter(cgon, precision)
        if (ccenter in visited_areas):
            continue
        visited_areas.append(ccenter)
        yield (cell, p1, p2, cgon, ccenter)

        for index, nextcellid in enumerate(tiling[cell]):
            cell_shift = cell_match(tiling, cell, nextcellid)
            nextcell, id = nextcellid
            if (id != 0 or (id == 0 and nextcell == cell)):
                continue
            # Create a stub ncgon at the edge of the current cgon
            nextcgon = xgon(len(tiling[nextcell]), cgon[(index + 1) % len(cgon)], cgon[index])
            # Reorient it
            pa, pb = nextcgon[-cell_shift], nextcgon[(-cell_shift + 1) % len(nextcgon)]
            # ncenter = roundedcenter(nextcgon,precision)
            visits.append((nextcell, pa, pb))


def supertile_center(tiling, startcell, p1, p2, precision=7):
    "visited areas[center points: (polygon, cell number)]"
    visited_areas = list()
    for cell, p1, p2, cgon, ccenter in yield_insides(tiling, startcell, p1, p2):
        visited_areas.append(ccenter)
    xav = mean([p[0] for p in visited_areas])
    yav = mean([p[1] for p in visited_areas])
    return xav, yav


def close_rounded(p1, p2, precision=7):
    return abs(p1[0] - p2[0]) <= precision and abs(p1[1] - p2[1]) <= precision


def generate_supertile_coordinate_helpers(tiling, tilingname):
    # for cell in tile:
    #     for neigh,neighid in tile[cell]:
    #         if cell == neigh:
    #             print(tilingname,cell,neighid)
    p1 = RollyPoint(500, 500)
    EDGESIZE = 50
    p2 = RollyPoint(500 + EDGESIZE, 500)
    neighbours = dict()
    d = 0
    borders = set()
    cx, cy = supertile_center(tiling, 0, p1, p2, precision=7)

    for cell, nextcellid, cellgon, nextgon, pa, pb in yield_borders(tiling, 0, p1, p2):
        nextcell, nextid = nextcellid
        neigh = supertile_center(tiling, nextcell, pa, pb, precision=7)
        neighbours[(cell, nextcellid)] = neigh
        borders.add((cell, nextcellid))

    neighbours_classes = list()
    for (cell, nextcellid), neighbour in list(neighbours.items()):
        nx, ny = neighbour
        nx -= cx
        ny -= cy
        neighbours[(cell, nextcellid)] = nx, ny
        for bx, by in neighbours_classes:
            if close_rounded((nx, ny), (bx, by), precision=7):
                neighbours[(cell, nextcellid)] = bx, by
                nx, ny = bx, by
                break
            if close_rounded((-nx, -ny), (bx, by), precision=7):
                neighbours[(cell, nextcellid)] = -bx, -by
                nx, ny = -bx, -by
                break
        # else
        if (nx, ny) not in neighbours_classes and (-nx, -ny) not in neighbours_classes:
            neighbours_classes.append((nx, ny))

    tcoords = dict()
    tcoords[neighbours_classes[0]] = (1, 0)
    tcoords[neighbours_classes[1]] = (0, 1)
    if len(neighbours_classes) == 3:
        x1, y1 = neighbours_classes[0]
        x2, y2 = neighbours_classes[1]
        x, y = neighbours_classes[2]
        for i, j in [(1, 1), (1, -1), (-1, 1), (-1, -1)]:
            if close_rounded((x, y), (x1 * i + x2 * j, y1 * i + y2 * j)):
                tcoords[(x, y)] = i, j
    for (nx, ny), (cx, cy) in tuple(tcoords.items()):
        tcoords[-nx, -ny] = (-cx, -cy)

    if len(neighbours_classes) > 3:
        print("Error! Too many neighbour classes")
        print(neighbours_classes)
        raise (OverflowError)
    if len(neighbours_classes) * 2 != len(tcoords):
        print("Error! Not enough translation coordinates")
        print(neighbours_classes)
        print(tcoords)
        raise (OverflowError)

    for bordercells, neighbour_coordinates in tuple(neighbours.items()):
        x, y = neighbour_coordinates
        try:
            new_coords = tcoords[neighbour_coordinates]
        except:
            for ncoords in tcoords.keys():
                if close_rounded((x, y), ncoords, precision=7):
                    new_coords = tcoords[ncoords]
        try:
            neighbours[bordercells] = new_coords
        except:
            print(neighbour_coordinates, "not found in")
            print(tcoords)

        neighbours[bordercells] = new_coords
    return neighbours
