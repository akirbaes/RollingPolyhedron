#dict[face]=[(neighbour_face, differenciator)]
#neighbour faces in clockwise order
#match differenciator: -d with +d, else d with d
uniform2= dict()

uniform2['(3^6;3^4x6)1'] = \
{   0: [(10, 1), (1, 0), (12, 0), (5, 2), (8, 3), (3, 4)],
    1: [(0, 0), (6, 0), (2, 0)],
    2: [(1, 0), (3, 0), (7, 0)],
    3: [(2, 0), (4, 0), (0, 4)],
    4: [(3, 0), (5, 0), (11, 6)],
    5: [(4, 0), (6, 0), (0, 2)],
    6: [(1, 0), (9, 5), (5, 0)],
    7: [(2, 0), (8, 0), (12, 0)],
    8: [(7, 0), (0, 3), (9, 0)],
    9: [(8, 0), (6, 5), (10, 0)],
    10: [(9, 0), (0, 1), (11, 0)],
    11: [(10, 0), (4, 6), (12, 0)],
    12: [(0, 0), (7, 0), (11, 0)]}
    
uniform2['(3^6;3^4x6)2'] = \
{   0: [(12, 1), (3, 0), (1, 0), (9, 0), (6, 2), (15, 3)],
    1: [(0, 0), (2, 0), (13, 0)],
    2: [(1, 0), (4, 0), (8, 0)],
    3: [(0, 0), (16, 4), (4, 0)],
    4: [(2, 0), (3, 0), (5, 0)],
    5: [(4, 0), (19, 5), (6, 0)],
    6: [(5, 0), (0, 2), (7, 0)],
    7: [(6, 0), (10, 6), (8, 0)],
    8: [(2, 0), (7, 0), (20, 0)],
    9: [(0, 0), (18, 0), (10, 0)],
    10: [(9, 0), (11, 0), (7, 6)],
    11: [(10, 0), (16, 0), (12, 0)],
    12: [(11, 0), (0, 1), (20, 7)],
    13: [(1, 0), (14, 0), (18, 0)],
    14: [(13, 0), (20, 0), (15, 0)],
    15: [(14, 0), (0, 3), (19, 0)],
    16: [(11, 0), (17, 0), (3, 4)],
    17: [(18, 0), (19, 0), (16, 0)],
    18: [(9, 0), (13, 0), (17, 0)],
    19: [(15, 0), (5, 5), (17, 0)],
    20: [(8, 0), (12, 7), (14, 0)]}
    
uniform2['(3^6;3^3x4^2)1'] = \
{   0: [(4, 1), (0, 2), (1, 0), (0, -2)],
    1: [(0, 0), (2, 0), (2, 3)],
    2: [(1, 0), (1, 3), (3, 0)],
    3: [(2, 0), (4, 4), (4, 0)],
    4: [(3, 0), (0, 1), (3, 4)]}

uniform2['(3^6;3^3x4^2)2'] = \
{   0: [(6, 1), (0, 2), (1, 0), (0, -2)],
    1: [(0, 0), (2, 0), (2, 3)],
    2: [(1, 0), (1, 3), (3, 0)],
    3: [(2, 0), (4, 0), (4, 4)],
    4: [(3, 0), (3, 4), (5, 0)],
    5: [(4, 0), (6, 0), (6, 5)],
    6: [(5, 0), (5, 5), (0, 1)]}

uniform2['3^6;3^2x4x3x4'] = \
{   0: [(6, 0), (10, 1), (7, 0), (1, 0)],
    1: [(0, 0), (3, 0), (2, 0)],
    2: [(1, 0), (8, 0), (4, 0)],
    3: [(1, 0), (5, 0), (9, 0)],
    4: [(2, 0), (7, 3), (9, 5), (6, 0)],
    5: [(3, 0), (7, 0), (8, 4), (6, 2)],
    6: [(0, 0), (4, 0), (5, 2)],
    7: [(0, 0), (4, 3), (5, 0)],
    8: [(2, 0), (10, 0), (5, 4)],
    9: [(3, 0), (4, 5), (10, 0)],
    10: [(8, 0), (9, 0), (0, 1)]}

uniform2['3^6;3^2x4x12'] = \
{   0: [(8, 1), (3, 0), (11, 0), (1, 0), (4, 0), (2, 0), (13, 2), (3, 3), (6, 4), (1, 5), (15, 6), (2, 7)],
    1: [(0, 0), (10, 0), (0, 5), (5, 0)],
    2: [(0, 0), (9, 0), (0, 7), (14, 9)],
    3: [(0, 0), (7, 8), (0, 3), (12, 0)],
    4: [(0, 0), (5, 0), (9, 0)],
    5: [(1, 0), (6, 0), (4, 0)],
    6: [(5, 0), (0, 4), (7, 0)],
    7: [(6, 0), (3, 8), (8, 0)],
    8: [(9, 0), (7, 0), (0, 1)],
    9: [(2, 0), (4, 0), (8, 0)],
    10: [(1, 0), (11, 0), (15, 0)],
    11: [(0, 0), (12, 0), (10, 0)],
    12: [(3, 0), (13, 0), (11, 0)],
    13: [(12, 0), (0, 2), (14, 0)],
    14: [(13, 0), (2, 9), (15, 0)],
    15: [(10, 0), (14, 0), (0, 6)]}

uniform2['3^6;3^2x6^2'] = \
{   0: [(6, 1), (1, 0), (2, 0), (1, 2), (4, 3), (1, 4)],
    1: [(0, 0), (5, 5), (0, 2), (7, 6), (0, 4), (3, 0)],
    2: [(0, 0), (3, 0), (7, 0)],
    3: [(1, 0), (4, 0), (2, 0)],
    4: [(3, 0), (0, 3), (5, 0)],
    5: [(4, 0), (1, 5), (6, 0)],
    6: [(5, 0), (0, 1), (7, 0)],
    7: [(2, 0), (6, 0), (1, 6)]}

uniform2['3^4x6;3^2x6^2'] = \
{   0: [(0, 1), (1, 0), (4, 0), (0, -1), (2, 2), (3, 3)],
    1: [(0, 0), (4, 4), (2, 0)],
    2: [(1, 0), (0, 2), (3, 0)],
    3: [(2, 0), (0, 3), (4, 0)],
    4: [(0, 0), (3, 0), (1, 4)]}

uniform2['(3^3x4^2;3^2x4x3x4)1'] = \
{   0: [(2, 0), (1, 0), (7, 0), (14, 1)],
    1: [(0, 0), (3, 0), (8, 0), (5, 0)],
    2: [(0, 0), (17, 2), (4, 0)],
    3: [(1, 0), (4, 0), (16, 0)],
    4: [(2, 0), (12, 4), (3, 0)],
    5: [(1, 0), (17, 0), (6, 0)],
    6: [(5, 0), (11, 7), (7, 0)],
    7: [(0, 0), (6, 0), (16, 3)],
    8: [(1, 0), (9, 0), (10, 0)],
    9: [(8, 0), (16, 0), (11, 0)],
    10: [(8, 0), (12, 0), (17, 0)],
    11: [(9, 0), (6, 7), (13, 0), (12, 0)],
    12: [(10, 0), (11, 0), (15, 0), (4, 4)],
    13: [(11, 0), (17, 6), (14, 0)],
    14: [(13, 0), (0, 1), (15, 0)],
    15: [(12, 0), (14, 0), (16, 5)],
    16: [(3, 0), (15, 5), (7, 3), (9, 0)],
    17: [(5, 0), (10, 0), (2, 2), (13, 6)]}

uniform2['(3^3x4^2;3^2x4x3x4)2'] = \
{   0: [(3, 0), (1, 0), (4, 1), (2, 0)],
    1: [(0, 0), (5, 0), (9, 2), (6, 3)],
    2: [(0, 0), (10, 4), (7, 0)],
    3: [(0, 0), (10, 0), (4, 0)],
    4: [(3, 0), (0, 1), (5, 0)],
    5: [(1, 0), (4, 0), (6, 0)],
    6: [(5, 0), (1, 3), (11, 5)],
    7: [(2, 0), (8, 0), (10, 0)],
    8: [(7, 0), (11, 6), (9, 0)],
    9: [(8, 0), (1, 2), (11, 0)],
    10: [(3, 0), (7, 0), (11, 0), (2, 4)],
    11: [(9, 0), (6, 5), (8, 6), (10, 0)]}

uniform2['3^3x4^2;3x4x6x4'] = \
{   0: [(5, 0), (1, 0), (4, 0), (6, 0), (2, 0), (3, 0)],
    1: [(0, 0), (8, 0), (2, 2), (9, 0)],
    2: [(0, 0), (11, 0), (1, 2), (12, 0)],
    3: [(0, 0), (12, 0), (4, 3), (7, 0)],
    4: [(0, 0), (9, 0), (3, 3), (10, 0)],
    5: [(0, 0), (7, 0), (6, 1), (8, 0)],
    6: [(0, 0), (10, 0), (5, 1), (11, 0)],
    7: [(3, 0), (14, 6), (5, 0)],
    8: [(1, 0), (5, 0), (13, 0)],
    9: [(1, 0), (14, 0), (4, 0)],
    10: [(4, 0), (13, 7), (6, 0)],
    11: [(2, 0), (6, 0), (14, 4)],
    12: [(2, 0), (13, 5), (3, 0)],
    13: [(8, 0), (10, 7), (12, 5)],
    14: [(9, 0), (11, 4), (7, 6)]}

uniform2['(3^3x4^2;4^4)1'] = \
{   0: [(2, 0), (0, 1), (1, 0), (0, -1)],
    1: [(0, 0), (1, 4), (3, 0), (1, -4)],
    2: [(0, 0), (3, 2), (3, 3)],
    3: [(1, 0), (2, 2), (2, 3)]}

uniform2['(3^3x4^2;4^4)2'] = \
{   0: [(2, 0), (0, 1), (1, 0), (0, -1)],
    1: [(0, 0), (1, 4), (3, 0), (1, -4)],
    2: [(0, 0), (4, 2), (4, 3)],
    3: [(1, 0), (3, 5), (4, 0), (3, -5)],
    4: [(3, 0), (2, 2), (2, 3)]}

uniform2['3^2x4x3x4;3x4x6x4'] = \
{   0: [(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0)],
    1: [(0, 0), (9, 0), (13, 0), (8, 0)],
    2: [(0, 0), (8, 0), (14, 0), (7, 0)],
    3: [(0, 0), (7, 0), (13, 1), (12, 0)],
    4: [(0, 0), (12, 0), (14, 2), (11, 0)],
    5: [(0, 0), (11, 0), (13, 3), (10, 0)],
    6: [(0, 0), (10, 0), (14, 4), (9, 0)],
    7: [(2, 0), (10, 7), (3, 0)],
    8: [(1, 0), (11, 6), (2, 0)],
    9: [(1, 0), (6, 0), (12, 5)],
    10: [(5, 0), (7, 7), (6, 0)],
    11: [(4, 0), (8, 6), (5, 0)],
    12: [(3, 0), (9, 5), (4, 0)],
    13: [(1, 0), (3, 1), (5, 3)],
    14: [(2, 0), (4, 2), (6, 4)]}

uniform2['3^2x6^2;3x6x3x6'] = \
{   0: [(0, 1), (1, 0), (2, 0), (0, -1), (2, 2), (1, 3)],
    1: [(0, 0), (2, 4), (0, 3)],
    2: [(0, 0), (0, 2), (1, 4)]}

uniform2['3x4x3x12;3x12^2'] = \
{   0: [(0, 1), (1, 0), (2, 0), (0, 2), (4, 3), (1, 4), (0, -1), (5, 5), (4, 6), (0, -2), (2, 7), (5, 8)],
    1: [(0, 0), (0, 4), (3, 0)],
    2: [(0, 0), (3, 0), (0, 7)],
    3: [(1, 0), (4, 0), (5, 0), (2, 0)],
    4: [(3, 0), (0, 3), (0, 6)],
    5: [(3, 0), (0, 5), (0, 8)]}

uniform2['3x4^2x6;3x4x6x4'] = \
{   0: [(2, 0), (1, 0), (6, 0), (9, 1), (8, 2), (5, 3)],
    1: [(0, 0), (10, 0), (7, 0), (12, 0)],
    2: [(0, 0), (14, 4), (4, 0), (10, 0)],
    3: [(6, 0), (17, 0), (5, 0), (13, 7)],
    4: [(2, 0), (17, 6), (9, 0), (13, 0)],
    5: [(3, 0), (14, 0), (0, 3), (16, 9)],
    6: [(0, 0), (12, 0), (3, 0), (11, 5)],
    7: [(1, 0), (13, 0), (8, 0), (17, 0)],
    8: [(7, 0), (16, 0), (0, 2), (15, 0)],
    9: [(4, 0), (15, 8), (0, 1), (11, 0)],
    10: [(2, 0), (13, 0), (1, 0)],
    11: [(9, 0), (6, 5), (13, 0)],
    12: [(6, 0), (1, 0), (17, 0)],
    13: [(4, 0), (11, 0), (3, 7), (16, 0), (7, 0), (10, 0)],
    14: [(5, 0), (17, 0), (2, 4)],
    15: [(8, 0), (9, 8), (17, 0)],
    16: [(13, 0), (5, 9), (8, 0)],
    17: [(3, 0), (12, 0), (7, 0), (15, 0), (4, 6), (14, 0)]}

uniform2['(3x4^2x6;3x6x3x6)1'] = \
{   0: [(3, 0), (1, 0), (2, 0), (3, 1), (2, 2), (1, 3)],
    1: [(0, 0), (4, 0), (0, 3)],
    2: [(0, 0), (0, 2), (4, 5)],
    3: [(0, 0), (4, 4), (0, 1), (4, 0)],
    4: [(1, 0), (3, 0), (2, 5), (3, 4)]}

uniform2['3x4^2x6;3x6x3x6)_2'] = \
{   0: [(2, 0), (3, 1), (1, 0), (3, 2)],
    1: [(0, 0), (4, 5), (2, 3), (3, 0), (2, 4), (4, 6)],
    2: [(0, 0), (1, 3), (1, 4)],
    3: [(1, 0), (0, 2), (4, 0), (0, 1)],
    4: [(3, 0), (1, 6), (1, 5)]}

uniform2['3x4x6x4;4x6x12'] = \
{   0: [(5, 0), (2, 0), (8, 0), (3, 0), (9, 0), (4, 0), (5, 1), (7, 2), (8, 3), (6, 4), (9, 5), (1, 0)],
    1: [(0, 0), (9, 8), (10, 11), (5, 0)],
    2: [(0, 0), (5, 0), (11, 0), (8, 0)],
    3: [(0, 0), (8, 0), (10, 0), (9, 0)],
    4: [(0, 0), (9, 0), (11, 10), (5, 7)],
    5: [(0, 0), (1, 0), (7, 6), (0, 1), (4, 7), (2, 0)],
    6: [(8, 0), (11, 0), (9, 9), (0, 4)],
    7: [(8, 0), (0, 2), (5, 6), (10, 0)],
    8: [(0, 0), (2, 0), (6, 0), (0, 3), (7, 0), (3, 0)],
    9: [(0, 0), (3, 0), (1, 8), (0, 5), (6, 9), (4, 0)],
    10: [(3, 0), (7, 0), (1, 11)],
    11: [(2, 0), (4, 10), (6, 0)]}


old=uniform2
uniform2=dict()

for index,(key,value) in enumerate(old.items()):
    index+=1
    if "(" not in key:
        newkey = "2u%02d (%s)"%(index,key)
    else:
        newkey = "2u%02d %s"%(index,key)
    uniform2[newkey]=value

if __name__ == "__main__":
    print(len(uniform2))
    print(list(uniform2.keys()))

del old