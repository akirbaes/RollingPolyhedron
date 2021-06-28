bits = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"

def prettyprint_adjacency(matrix):
    print("\n".join(["".join([it and "X" or " " for it in line]) for line in matrix]))

def prettierformat_adjacency(matrix):
    w = len(matrix[0])
    h = len(matrix)
    chars = ""
    for j in range(0, h, 2):
        for i in range(0, w, 2):
            number = matrix[i][j]
            try:
                number += matrix[i + 1][j] * 2
            except:
                pass
            try:
                number += matrix[i][j + 1] * 4
            except:
                pass
            try:
                number += matrix[i + 1][j + 1] * 8
            except:
                pass
            chars += bits[number]
        chars += "\n"
    return chars[:-1]

def prettierprint_adjacency(matrix):
    print(prettierformat_adjacency(matrix))

def prettierprint_FFOOmatrix(FFOO,borders = True):
    #Matrix of matrices
    for li,line in enumerate(FFOO):
        if(borders):
            if(li==0):
                print("┏"+"┳".join("━"*(len(line[0][0])//2) for x in line)+"┓")
            else:
                print("┣"+"╋".join("━"*(len(line[0][0])//2) for x in line)+"┫")
            outlines = ["┃" for line in range(len(line[0])//2)]
        else:
            outlines = ["" for line in range(len(line[0])//2)]
        for block in line:
            # prettierprint_adjacency(block)
            blocklines = prettierformat_adjacency(block).split("\n")
            for i, seg in enumerate(blocklines):
                if(borders):
                    outlines[i]=outlines[i]+seg+"┃"
                else:
                    outlines[i]=outlines[i]+seg

        for outline in outlines:
            print(outline)
    if(borders):
        print("┗"+"┻".join("━"*(len(line[0][0])//2) for x in line)+"┛")

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


def explore_inside(tile, poly, polyname, canon_fo=None):
    classes = list()
    for start_case in tile:
        for start_face in poly:
            if len(tile[start_case]) == len(poly[start_face]):
                for orientation in range(len(poly[start_face])):
                    if(canon_fo):
                        start_face,orientation=canon_fo(polyname,start_face,orientation)
                    ###For every compatible CFO, start an exploration class
                    pos = (start_case, start_face, orientation)
                    # input("%s\n%s\n%s\n"%(pos,str(classes),any([pos in existing_class for existing_class in classes])))

                    if any(pos in existing_class for existing_class in classes):
                        continue
                    current_class = set()
                    to_explore = set()
                    to_explore.add(pos)

                    while to_explore:
                        case, face, orientation = to_explore.pop()
                        sides = len(poly[face])
                        if canon_fo:
                            face, orientation = canon_fo(polyname,face,orientation)
                        if len(tile[case]) != sides:
                            continue
                        if (case, face, orientation) in current_class:
                            continue
                        current_class.add((case, face, orientation))

                        newcasesid = tile[case]
                        newfaces = poly[face][orientation:] + poly[face][:orientation]
                        for i in range(sides):
                            # for new areas to explore
                            newcase,newid = newcasesid[i]
                            newface = newfaces[i]
                            if newid==0 and case!=newcase:
                                # still inside
                                nextfaces = poly[newface]
                                nextcases = tile[newcase]
                                nextsides = len(nextfaces)
                                if len(tile[newcase]) != nextsides:
                                    continue
                                # look back for orientation
                                neworientation = (nextfaces.index(face) - case_match(tile,case,(newcase,newid)))%nextsides
                                if canon_fo:
                                    newface, neworientation = canon_fo(polyname,newface,neworientation)
                                if (newcase, newface, neworientation) not in current_class:
                                    to_explore.add((newcase, newface, neworientation))
                    classes.append(current_class)
    print(classes)
    return classes


def explore_borders(tile, poly):
    borders = dict()
    for case in tile:
        for i, newcaseid in enumerate(tile[case]):
            newcase,newid = newcaseid
            if newid!=0  or case == newcase:
                ###For every case pairs at the border
                startpair = (case, newcase)
                startsides = len(poly[case])
                nextcases = tile[newcase]
                nextsides = len(nextcases)
                # borders[startpair]=dict()
                for face in poly:
                    if len(tile[case]) == len(poly[face]):
                        for orientation in range(len(poly[face])):
                            # For  every (C)FO
                            newface = poly[face][(orientation + i) % startsides]
                            nextfaces = poly[newface]
                            if len(nextfaces) == nextsides:
                                caseindex = case_match(tile, case, newcaseid)
                                neworientation = (nextfaces.index(face) - caseindex) % nextsides
                                # borders[startpair][(case,face,orientation)]=(newcase%len(tile),newface,neworientation)
                                # borders.setdefault((case,face,orientation),set())
                                borders.setdefault((case, face, orientation), dict())
                                # borders[(case,face,orientation)].add((newcase%len(tile),newface,neworientation))
                                borders[(case, face, orientation)][startpair] = (
                                    newcase, newface, neworientation)
    return borders

from pprint import pprint

def CFO_class_adjacency(start_cfo, tile,poly,polyname,canon_fo):
    classes = explore_inside(tile,poly,polyname,canon_fo)
    transformations = explore_borders(tile, poly)
    borders = set(transformations.keys())

    def class_index(cfo):
        for i, clas in enumerate(classes):
            if cfo in clas:
                return i
    initial_class = class_index(start_cfo)

    print("Classes:")
    pprint(classes)


    class_transfo = [[False for clas in classes] for clas in classes]
    for cfo in transformations:
        class_start = class_index(cfo)
        for bordercase in transformations[cfo]:
            #coordinate = neighbour_coord[bordercase]
            cfo_arrival = transformations[cfo][bordercase]
            print(cfo,cfo_arrival,flush=True)
            class_end = class_index(cfo_arrival)
            # print(transformations[cfo][bordercase])
            # print(cfo,cfo_arrival)
            # if coordinate:
            #     print("C1,C2,coord", class_start, class_end, coordinate)
            #     class_transfo[class_start][class_end].append(coordinate)
            class_transfo[class_start][class_end]=True
    print("Class transformations:")

    prettierprint_adjacency(class_transfo)


if __name__ == "__main__":
    from tiling_dicts.archimedean_tilings import archimedean_tilings
    from tiling_dicts.platonic_tilings import platonic_tilings
    from poly_dicts.plato_archi_nets import plato_archi_nets
    from poly_dicts.johnson_nets import johnson_nets
    tiling = platonic_tilings['4^4']
    polyname = "j8"
    net = johnson_nets[polyname]

    from symmetry_classes.poly_symmetries import poly_symmetries
    import symmetry_classes.symmetry_functions
    def canon_fo(polyname, face, orientation):
        return symmetry_classes.symmetry_functions.canon_fo(polyname, face, orientation, poly_symmetries)
    CFO_class_adjacency((0,0,0),tiling,net,polyname,None)
