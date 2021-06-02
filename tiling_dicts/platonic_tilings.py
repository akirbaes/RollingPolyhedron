#dict[face]=[(neighbour_face, differenciator)]
#neighbour faces in clockwise order
#match differenciator: -d with +d, else d with d
platonic_tilings= dict()
platonic_tilings['3^6'] = \
{0: [(0, 1), (0, 2), (0, 3)]}

platonic_tilings['4^4'] = \
{0: [(0, 1), (0, 2), (0, -1), (0, -2)]}

platonic_tilings['6^3'] = \
{0: [(0, 1), (0, 2), (0, 3), (0, -1), (0, -2), (0, -3)]}

