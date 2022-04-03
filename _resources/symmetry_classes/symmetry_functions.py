def canon_fo(polyname,face,orientation,poly_symmetries):
    try:
        symmetries = poly_symmetries[polyname]
        for sym in symmetries:
            if (face,orientation) in sym:
                #print("Found a symmetry!")
                return min(sym)
    except:
        print("No symmetry info for this poly")
    return face, orientation


def canon_FO(polyname,face,orientation):
    try:
        symmetries = poly_symmetries[polyname]
        for sym in symmetries:
            if (face,orientation) in sym:
                #print("Found a symmetry!")
                return min(sym)
    except:
        print("No symmetry info for this poly")
    return face, orientation