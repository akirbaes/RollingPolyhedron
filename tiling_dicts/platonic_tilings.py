#dict[face]=[(neighbour_face, differenciator)]
#neighbour faces in clockwise order
#match differenciator: -d with +d, else d with d
platonic_tilings= dict()
platonic_tilings['1u01 (3^6)'] = \
{0: [(1, 0), (1, 1), (1, 2)],
 1: [(0, 0), (0, -1), (0, -2)]}

platonic_tilings['1u02 (4^4)'] = \
{0: [(0, 1), (0, 2), (0, -1), (0, -2)]}

platonic_tilings['1u03 (6^3)'] = \
{0: [(0, 1), (0, 2), (0, 3), (0, -1), (0, -2), (0, -3)]}

