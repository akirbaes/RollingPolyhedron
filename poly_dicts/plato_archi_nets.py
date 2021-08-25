#dict[face]=[neighbour_face ...]
plato_archi_nets= dict()

plato_archi_nets['tetrahedron'] = \
{0: [1, 2, 3], 1: [2, 0, 3], 2: [0, 1, 3], 3: [2, 1, 0]}

plato_archi_nets['cube'] = \
{   0: [2, 3, 4, 1],
    1: [5, 2, 0, 4],
    2: [5, 3, 0, 1],
    3: [5, 4, 0, 2],
    4: [0, 3, 5, 1],
    5: [3, 2, 1, 4]}
    
plato_archi_nets['octahedron'] = \
{   0: [3, 1, 7],
    1: [0, 2, 6],
    2: [1, 3, 5],
    3: [2, 0, 4],
    4: [7, 5, 3],
    5: [4, 6, 2],
    6: [5, 7, 1],
    7: [6, 4, 0]}
    
plato_archi_nets['dodecahedron'] = \
{   0: [1, 2, 3, 4, 5],
    1: [5, 6, 7, 2, 0],
    2: [1, 7, 8, 3, 0],
    3: [2, 8, 9, 4, 0],
    4: [3, 9, 10, 5, 0],
    5: [4, 10, 6, 1, 0],
    6: [7, 1, 5, 10, 11],
    7: [8, 2, 1, 6, 11],
    8: [9, 3, 2, 7, 11],
    9: [10, 4, 3, 8, 11],
    10: [6, 5, 4, 9, 11],
    11: [10, 9, 8, 7, 6]}

plato_archi_nets['icosahedron'] = \
{   0: [1, 4, 5],
    1: [2, 0, 7],
    2: [3, 1, 9],
    3: [4, 2, 11],
    4: [0, 3, 14],
    5: [0, 13, 6],
    6: [7, 5, 15],
    7: [1, 6, 8],
    8: [9, 7, 16],
    9: [2, 8, 10],
    10: [11, 9, 17],
    11: [3, 10, 12],
    12: [14, 11, 18],
    13: [5, 14, 19],
    14: [4, 12, 13],
    15: [19, 16, 6],
    16: [15, 17, 8],
    17: [16, 18, 10],
    18: [17, 19, 12],
    19: [18, 15, 13]}


plato_archi_nets['truncated_tetrahedron'] = \
{   0: [7, 5, 4],
    1: [7, 6, 5],
    2: [6, 4, 5],
    3: [7, 4, 6],
    4: [7, 0, 5, 2, 6, 3],
    5: [7, 1, 6, 2, 4, 0],
    6: [7, 3, 4, 2, 5, 1],
    7: [5, 0, 4, 3, 6, 1]}

plato_archi_nets['cuboctahedron'] = \
{   0: [1, 2, 3, 4],
    1: [0, 8, 5],
    2: [0, 5, 6],
    3: [0, 6, 7],
    4: [0, 7, 8],
    5: [1, 12, 9, 2],
    6: [2, 9, 10, 3],
    7: [3, 10, 11, 4],
    8: [4, 11, 12, 1],
    9: [5, 13, 6],
    10: [6, 13, 7],
    11: [7, 13, 8],
    12: [8, 13, 5],
    13: [12, 11, 10, 9]}

plato_archi_nets['truncated_cube'] = \
{   0: [1, 10, 2, 11, 5, 9, 3, 8],
    1: [0, 8, 3, 6, 4, 12, 2, 10],
    2: [0, 10, 1, 12, 4, 13, 5, 11],
    3: [0, 9, 5, 7, 4, 6, 1, 8],
    4: [3, 7, 5, 13, 2, 12, 1, 6],
    5: [0, 11, 2, 13, 4, 7, 3, 9],
    6: [4, 1, 3],
    7: [4, 3, 5],
    8: [3, 1, 0],
    9: [3, 0, 5],
    10: [0, 1, 2],
    11: [0, 2, 5],
    12: [2, 1, 4],
    13: [2, 4, 5]}

plato_archi_nets['truncated_octahedron'] = \
{   0: [1, 2, 3, 4],
    1: [0, 4, 9, 5, 12, 2],
    2: [0, 1, 12, 6, 13, 3],
    3: [0, 2, 13, 7, 11, 4],
    4: [0, 3, 11, 8, 9, 1],
    5: [1, 9, 8, 10, 6, 12],
    6: [2, 12, 5, 10, 7, 13],
    7: [3, 13, 6, 10, 8, 11],
    8: [4, 11, 7, 10, 5, 9],
    9: [8, 5, 1, 4],
    10: [8, 7, 6, 5],
    11: [8, 4, 3, 7],
    12: [2, 1, 5, 6],
    13: [2, 6, 7, 3]}

plato_archi_nets['rhombicuboctahedron'] = \
{   0: [1, 2, 3, 4],
    1: [0, 22, 5, 18],
    2: [0, 18, 6, 21],
    3: [0, 21, 10, 23],
    4: [0, 23, 11, 22],
    5: [1, 14, 17, 7],
    6: [2, 7, 8, 9],
    7: [6, 18, 5, 19],
    8: [6, 19, 15, 20],
    9: [6, 20, 10, 21],
    10: [3, 9, 16, 12],
    11: [4, 12, 13, 14],
    12: [11, 23, 10, 25],
    13: [11, 25, 15, 24],
    14: [11, 24, 5, 22],
    15: [13, 16, 8, 17],
    16: [15, 25, 10, 20],
    17: [15, 19, 5, 24],
    18: [2, 1, 7],
    19: [8, 7, 17],
    20: [8, 16, 9],
    21: [2, 9, 3],
    22: [4, 14, 1],
    23: [4, 3, 12],
    24: [13, 17, 14],
    25: [13, 12, 16]}

plato_archi_nets['truncated_cuboctahedron'] = \
{   0: [1, 23, 2, 22, 3, 20, 4, 21],
    1: [0, 21, 7, 23],
    2: [0, 23, 5, 22],
    3: [0, 22, 6, 20],
    4: [0, 20, 8, 21],
    5: [2, 23, 13, 24, 10, 25, 14, 22],
    6: [3, 22, 14, 25, 17, 19, 12, 20],
    7: [1, 21, 11, 18, 16, 24, 13, 23],
    8: [4, 20, 12, 19, 9, 18, 11, 21],
    9: [8, 19, 15, 18],
    10: [5, 24, 15, 25],
    11: [8, 18, 7, 21],
    12: [8, 20, 6, 19],
    13: [5, 23, 7, 24],
    14: [5, 25, 6, 22],
    15: [10, 24, 16, 18, 9, 19, 17, 25],
    16: [15, 24, 7, 18],
    17: [15, 19, 6, 25],
    18: [8, 9, 15, 16, 7, 11],
    19: [8, 12, 6, 17, 15, 9],
    20: [0, 3, 6, 12, 8, 4],
    21: [0, 4, 8, 11, 7, 1],
    22: [0, 2, 5, 14, 6, 3],
    23: [0, 1, 7, 13, 5, 2],
    24: [5, 13, 7, 16, 15, 10],
    25: [5, 10, 15, 17, 6, 14]}

plato_archi_nets['snub_cube'] = \
{   0: [25, 31, 3, 6],
    1: [4, 23, 19, 9],
    2: [7, 8, 20, 26],
    3: [4, 0, 29],
    4: [1, 5, 3],
    5: [4, 8, 6],
    6: [5, 7, 0],
    7: [6, 2, 28],
    8: [9, 2, 5],
    9: [1, 22, 8],
    10: [14, 21, 18, 17],
    11: [24, 27, 13, 33],
    12: [30, 34, 16, 36],
    13: [11, 37, 14],
    14: [13, 10, 15],
    15: [33, 14, 16],
    16: [15, 17, 12],
    17: [16, 10, 32],
    18: [22, 19, 10],
    19: [18, 1, 32],
    20: [2, 22, 21],
    21: [37, 20, 10],
    22: [20, 9, 18],
    23: [1, 29, 36],
    24: [25, 11, 35],
    25: [24, 0, 28],
    26: [27, 2, 37],
    27: [28, 26, 11],
    28: [25, 7, 27],
    29: [3, 30, 23],
    30: [12, 29, 31],
    31: [30, 0, 35],
    32: [19, 36, 17],
    33: [34, 11, 15],
    34: [35, 33, 12],
    35: [24, 34, 31],
    36: [23, 12, 32],
    37: [13, 26, 21]}

plato_archi_nets["snub_cube_c"]=\
{   0: [6, 3, 31, 25],
    1: [9, 19, 23, 4],
    2: [26, 20, 8, 7],
    3: [29, 0, 4],
    4: [3, 5, 1],
    5: [6, 8, 4],
    6: [0, 7, 5],
    7: [28, 2, 6],
    8: [5, 2, 9],
    9: [8, 22, 1],
    10: [17, 18, 21, 14],
    11: [33, 13, 27, 24],
    12: [36, 16, 34, 30],
    13: [14, 37, 11],
    14: [15, 10, 13],
    15: [16, 14, 33],
    16: [12, 17, 15],
    17: [32, 10, 16],
    18: [10, 19, 22],
    19: [32, 1, 18],
    20: [21, 22, 2],
    21: [10, 20, 37],
    22: [18, 9, 20],
    23: [36, 29, 1],
    24: [35, 11, 25],
    25: [28, 0, 24],
    26: [37, 2, 27],
    27: [11, 26, 28],
    28: [27, 7, 25],
    29: [23, 30, 3],
    30: [31, 29, 12],
    31: [35, 0, 30],
    32: [17, 36, 19],
    33: [15, 11, 34],
    34: [12, 33, 35],
    35: [31, 34, 24],
    36: [32, 12, 23],
    37: [21, 26, 13]}
    
plato_archi_nets['icosidodecahedron'] = \
{   0: [1, 2, 3, 4, 5],
    1: [0, 10, 6],
    2: [0, 6, 7],
    3: [0, 7, 8],
    4: [0, 8, 9],
    5: [0, 9, 10],
    6: [2, 1, 11, 12, 13],
    7: [2, 13, 14, 15, 3],
    8: [4, 3, 15, 16, 17],
    9: [5, 4, 17, 18, 19],
    10: [1, 5, 19, 20, 11],
    11: [6, 10, 21],
    12: [6, 21, 22],
    13: [7, 6, 22],
    14: [7, 22, 23],
    15: [7, 23, 8],
    16: [8, 23, 24],
    17: [9, 8, 24],
    18: [9, 24, 25],
    19: [10, 9, 25],
    20: [10, 25, 21],
    21: [12, 11, 20, 27, 29],
    22: [13, 12, 29, 28, 14],
    23: [15, 14, 28, 31, 16],
    24: [18, 17, 16, 31, 26],
    25: [20, 19, 18, 26, 27],
    26: [25, 24, 30],
    27: [21, 25, 30],
    28: [22, 30, 23],
    29: [22, 21, 30],
    30: [28, 29, 27, 26, 31],
    31: [23, 30, 24]}

plato_archi_nets['truncated_dodecahedron'] = \
{   0: [4, 13, 1, 17, 5, 28, 11, 27, 6, 26],
    1: [0, 13, 4, 14, 3, 15, 2, 16, 5, 17],
    2: [1, 15, 3, 30, 9, 23, 10, 29, 5, 16],
    3: [1, 14, 4, 31, 8, 24, 9, 30, 2, 15],
    4: [1, 13, 0, 26, 6, 25, 8, 31, 3, 14],
    5: [1, 16, 2, 29, 10, 22, 11, 28, 0, 17],
    6: [0, 27, 11, 12, 7, 18, 8, 25, 4, 26],
    7: [6, 12, 11, 21, 10, 20, 9, 19, 8, 18],
    8: [7, 19, 9, 24, 3, 31, 4, 25, 6, 18],
    9: [7, 20, 10, 23, 2, 30, 3, 24, 8, 19],
    10: [7, 21, 11, 22, 5, 29, 2, 23, 9, 20],
    11: [7, 12, 6, 27, 0, 28, 5, 22, 10, 21],
    12: [7, 6, 11],
    13: [1, 0, 4],
    14: [1, 4, 3],
    15: [1, 3, 2],
    16: [1, 2, 5],
    17: [1, 5, 0],
    18: [7, 8, 6],
    19: [7, 9, 8],
    20: [7, 10, 9],
    21: [7, 11, 10],
    22: [11, 5, 10],
    23: [10, 2, 9],
    24: [9, 3, 8],
    25: [8, 4, 6],
    26: [0, 6, 4],
    27: [0, 11, 6],
    28: [5, 11, 0],
    29: [2, 10, 5],
    30: [3, 9, 2],
    31: [4, 8, 3]}

plato_archi_nets['truncated_icosahedron'] = \
{   0: [24, 1, 31, 11, 29, 12],
    1: [0, 24, 2, 23, 3, 31],
    2: [1, 24, 13, 26, 6, 23],
    3: [1, 23, 5, 22, 4, 31],
    4: [3, 22, 8, 30, 11, 31],
    5: [3, 23, 6, 21, 7, 22],
    6: [5, 23, 2, 26, 10, 21],
    7: [5, 21, 9, 27, 8, 22],
    8: [7, 27, 19, 30, 4, 22],
    9: [7, 21, 10, 20, 18, 27],
    10: [9, 21, 6, 26, 17, 20],
    11: [0, 31, 4, 30, 15, 29],
    12: [0, 29, 14, 25, 13, 24],
    13: [12, 25, 17, 26, 2, 24],
    14: [12, 29, 15, 28, 16, 25],
    15: [14, 29, 11, 30, 19, 28],
    16: [14, 28, 18, 20, 17, 25],
    17: [16, 20, 10, 26, 13, 25],
    18: [16, 28, 19, 27, 9, 20],
    19: [18, 28, 15, 30, 8, 27],
    20: [9, 10, 17, 16, 18],
    21: [5, 6, 10, 9, 7],
    22: [7, 8, 4, 3, 5],
    23: [3, 1, 2, 6, 5],
    24: [0, 12, 13, 2, 1],
    25: [14, 16, 17, 13, 12],
    26: [13, 17, 10, 6, 2],
    27: [18, 19, 8, 7, 9],
    28: [14, 15, 19, 18, 16],
    29: [12, 0, 11, 15, 14],
    30: [11, 4, 8, 19, 15],
    31: [4, 11, 0, 1, 3]}

plato_archi_nets['rhombicosidodecahedron'] = \
{   0: [3, 4, 5, 1, 2],
    1: [0, 56, 6, 57],
    2: [0, 57, 19, 58],
    3: [0, 58, 14, 59],
    4: [0, 59, 15, 55],
    5: [8, 56, 0, 55],
    6: [1, 7, 11, 12, 13],
    7: [6, 56, 8, 37],
    8: [7, 5, 9, 10, 38],
    9: [8, 55, 15, 52],
    10: [8, 52, 16, 39],
    11: [6, 37, 17, 40],
    12: [6, 40, 18, 43],
    13: [6, 43, 19, 57],
    14: [3, 22, 23, 24, 25],
    15: [9, 4, 25, 26, 53],
    16: [10, 53, 27, 28, 29],
    17: [11, 38, 29, 30, 31],
    18: [12, 31, 32, 33, 20],
    19: [13, 20, 21, 22, 2],
    20: [19, 43, 18, 44],
    21: [19, 44, 34, 45],
    22: [19, 45, 14, 58],
    23: [14, 45, 34, 60],
    24: [14, 60, 36, 61],
    25: [15, 59, 14, 61],
    26: [15, 61, 36, 54],
    27: [16, 54, 36, 51],
    28: [16, 51, 35, 50],
    29: [17, 39, 16, 50],
    30: [17, 50, 35, 41],
    31: [18, 40, 17, 41],
    32: [18, 41, 35, 42],
    33: [18, 42, 34, 44],
    34: [21, 33, 46, 47, 23],
    35: [32, 30, 28, 49, 46],
    36: [26, 24, 47, 49, 27],
    37: [7, 38, 11],
    38: [37, 8, 39, 17],
    39: [38, 10, 29],
    40: [12, 11, 31],
    41: [31, 30, 32],
    42: [33, 32, 46],
    43: [13, 12, 20],
    44: [21, 20, 33],
    45: [22, 21, 23],
    46: [34, 42, 35, 48],
    47: [34, 48, 36, 60],
    48: [46, 49, 47],
    49: [35, 51, 36, 48],
    50: [30, 29, 28],
    51: [28, 27, 49],
    52: [9, 53, 10],
    53: [52, 15, 54, 16],
    54: [53, 26, 27],
    55: [9, 5, 4],
    56: [7, 1, 5],
    57: [1, 13, 2],
    58: [3, 2, 22],
    59: [4, 3, 25],
    60: [24, 23, 47],
    61: [25, 24, 26]}

plato_archi_nets['truncated_icosidodecahedron'] = \
{   0: [15, 21, 14, 22, 13, 23, 12, 1, 11, 20],
    1: [0, 12, 2, 10, 16, 11],
    2: [1, 12, 23, 43, 31, 8, 3, 9, 17, 10],
    3: [2, 8, 4, 7, 28, 9],
    4: [3, 8, 31, 44, 33, 45, 5, 6, 30, 7],
    5: [4, 45, 56, 58, 61, 6],
    6: [4, 5, 61, 30],
    7: [3, 4, 30, 28],
    8: [2, 31, 4, 3],
    9: [2, 3, 28, 17],
    10: [1, 2, 17, 16],
    11: [0, 1, 16, 20],
    12: [1, 0, 23, 2],
    13: [0, 22, 24, 23],
    14: [0, 21, 25, 22],
    15: [0, 20, 26, 21],
    16: [1, 10, 17, 41, 18, 39, 19, 55, 20, 11],
    17: [16, 10, 2, 9, 28, 41],
    18: [16, 41, 28, 40, 27, 39],
    19: [16, 39, 27, 52, 26, 55],
    20: [0, 11, 16, 55, 26, 15],
    21: [0, 15, 26, 54, 25, 14],
    22: [0, 14, 25, 47, 24, 13],
    23: [0, 13, 24, 43, 2, 12],
    24: [13, 22, 47, 32, 46, 33, 44, 31, 43, 23],
    25: [14, 21, 54, 35, 49, 34, 48, 32, 47, 22],
    26: [15, 20, 55, 19, 52, 36, 51, 35, 54, 21],
    27: [19, 39, 18, 40, 29, 38, 37, 53, 36, 52],
    28: [17, 9, 3, 7, 30, 42, 29, 40, 18, 41],
    29: [28, 42, 61, 38, 27, 40],
    30: [28, 7, 4, 6, 61, 42],
    31: [2, 43, 24, 44, 4, 8],
    32: [24, 47, 25, 48, 56, 46],
    33: [24, 46, 56, 45, 4, 44],
    34: [25, 49, 59, 50, 56, 48],
    35: [25, 54, 26, 51, 59, 49],
    36: [26, 52, 27, 53, 59, 51],
    37: [27, 38, 61, 60, 59, 53],
    38: [27, 29, 61, 37],
    39: [16, 18, 27, 19],
    40: [18, 28, 29, 27],
    41: [16, 17, 28, 18],
    42: [28, 30, 61, 29],
    43: [23, 24, 31, 2],
    44: [24, 33, 4, 31],
    45: [33, 56, 5, 4],
    46: [24, 32, 56, 33],
    47: [22, 25, 32, 24],
    48: [25, 34, 56, 32],
    49: [25, 35, 59, 34],
    50: [34, 59, 57, 56],
    51: [26, 36, 59, 35],
    52: [26, 19, 27, 36],
    53: [36, 27, 37, 59],
    54: [21, 26, 35, 25],
    55: [20, 16, 19, 26],
    56: [45, 33, 46, 32, 48, 34, 50, 57, 58, 5],
    57: [56, 50, 59, 60, 61, 58],
    58: [56, 57, 61, 5],
    59: [49, 35, 51, 36, 53, 37, 60, 57, 50, 34],
    60: [59, 37, 61, 57],
    61: [42, 30, 6, 5, 58, 57, 60, 37, 38, 29]}

plato_archi_nets['snub_dodecahedron'] = \
{   0: [35, 34, 33, 32, 36],
    1: [50, 45, 40, 60, 55],
    2: [42, 37, 57, 52, 47],
    3: [43, 38, 58, 53, 48],
    4: [49, 44, 39, 59, 54],
    5: [46, 41, 61, 56, 51],
    6: [64, 63, 62, 66, 65],
    7: [80, 75, 70, 90, 85],
    8: [87, 82, 77, 72, 67],
    9: [83, 78, 73, 68, 88],
    10: [69, 89, 84, 79, 74],
    11: [76, 71, 91, 86, 81],
    12: [32, 42, 41],
    13: [33, 43, 37],
    14: [34, 44, 38],
    15: [35, 45, 39],
    16: [36, 46, 40],
    17: [47, 85, 61],
    18: [48, 84, 57],
    19: [49, 83, 58],
    20: [50, 82, 59],
    21: [51, 86, 60],
    22: [52, 89, 80],
    23: [53, 88, 79],
    24: [54, 87, 78],
    25: [55, 91, 77],
    26: [56, 90, 81],
    27: [62, 72, 71],
    28: [63, 73, 67],
    29: [64, 74, 68],
    30: [65, 75, 69],
    31: [66, 76, 70],
    32: [0, 37, 12],
    33: [0, 38, 13],
    34: [0, 39, 14],
    35: [0, 40, 15],
    36: [0, 41, 16],
    37: [2, 32, 13],
    38: [3, 33, 14],
    39: [4, 34, 15],
    40: [1, 35, 16],
    41: [5, 36, 12],
    42: [2, 61, 12],
    43: [3, 57, 13],
    44: [4, 58, 14],
    45: [1, 59, 15],
    46: [5, 60, 16],
    47: [2, 80, 17],
    48: [3, 79, 18],
    49: [4, 78, 19],
    50: [1, 77, 20],
    51: [5, 81, 21],
    52: [2, 84, 22],
    53: [3, 83, 23],
    54: [4, 82, 24],
    55: [1, 86, 25],
    56: [5, 85, 26],
    57: [2, 43, 18],
    58: [3, 44, 19],
    59: [4, 45, 20],
    60: [1, 46, 21],
    61: [5, 42, 17],
    62: [6, 67, 27],
    63: [6, 68, 28],
    64: [6, 69, 29],
    65: [6, 70, 30],
    66: [6, 71, 31],
    67: [8, 62, 28],
    68: [9, 63, 29],
    69: [10, 64, 30],
    70: [7, 65, 31],
    71: [11, 66, 27],
    72: [8, 91, 27],
    73: [9, 87, 28],
    74: [10, 88, 29],
    75: [7, 89, 30],
    76: [11, 90, 31],
    77: [8, 50, 25],
    78: [9, 49, 24],
    79: [10, 48, 23],
    80: [7, 47, 22],
    81: [11, 51, 26],
    82: [8, 54, 20],
    83: [9, 53, 19],
    84: [10, 52, 18],
    85: [7, 56, 17],
    86: [11, 55, 21],
    87: [8, 73, 24],
    88: [9, 74, 23],
    89: [10, 75, 22],
    90: [7, 76, 26],
    91: [11, 72, 25]}

plato_archi_nets["snub_dodecahedron_c"]=\
{   0: [36, 32, 33, 34, 35],
    1: [55, 60, 40, 45, 50],
    2: [47, 52, 57, 37, 42],
    3: [48, 53, 58, 38, 43],
    4: [54, 59, 39, 44, 49],
    5: [51, 56, 61, 41, 46],
    6: [65, 66, 62, 63, 64],
    7: [85, 90, 70, 75, 80],
    8: [67, 72, 77, 82, 87],
    9: [88, 68, 73, 78, 83],
    10: [74, 79, 84, 89, 69],
    11: [81, 86, 91, 71, 76],
    12: [41, 42, 32],
    13: [37, 43, 33],
    14: [38, 44, 34],
    15: [39, 45, 35],
    16: [40, 46, 36],
    17: [61, 85, 47],
    18: [57, 84, 48],
    19: [58, 83, 49],
    20: [59, 82, 50],
    21: [60, 86, 51],
    22: [80, 89, 52],
    23: [79, 88, 53],
    24: [78, 87, 54],
    25: [77, 91, 55],
    26: [81, 90, 56],
    27: [71, 72, 62],
    28: [67, 73, 63],
    29: [68, 74, 64],
    30: [69, 75, 65],
    31: [70, 76, 66],
    32: [12, 37, 0],
    33: [13, 38, 0],
    34: [14, 39, 0],
    35: [15, 40, 0],
    36: [16, 41, 0],
    37: [13, 32, 2],
    38: [14, 33, 3],
    39: [15, 34, 4],
    40: [16, 35, 1],
    41: [12, 36, 5],
    42: [12, 61, 2],
    43: [13, 57, 3],
    44: [14, 58, 4],
    45: [15, 59, 1],
    46: [16, 60, 5],
    47: [17, 80, 2],
    48: [18, 79, 3],
    49: [19, 78, 4],
    50: [20, 77, 1],
    51: [21, 81, 5],
    52: [22, 84, 2],
    53: [23, 83, 3],
    54: [24, 82, 4],
    55: [25, 86, 1],
    56: [26, 85, 5],
    57: [18, 43, 2],
    58: [19, 44, 3],
    59: [20, 45, 4],
    60: [21, 46, 1],
    61: [17, 42, 5],
    62: [27, 67, 6],
    63: [28, 68, 6],
    64: [29, 69, 6],
    65: [30, 70, 6],
    66: [31, 71, 6],
    67: [28, 62, 8],
    68: [29, 63, 9],
    69: [30, 64, 10],
    70: [31, 65, 7],
    71: [27, 66, 11],
    72: [27, 91, 8],
    73: [28, 87, 9],
    74: [29, 88, 10],
    75: [30, 89, 7],
    76: [31, 90, 11],
    77: [25, 50, 8],
    78: [24, 49, 9],
    79: [23, 48, 10],
    80: [22, 47, 7],
    81: [26, 51, 11],
    82: [20, 54, 8],
    83: [19, 53, 9],
    84: [18, 52, 10],
    85: [17, 56, 7],
    86: [21, 55, 11],
    87: [24, 73, 8],
    88: [23, 74, 9],
    89: [22, 75, 10],
    90: [26, 76, 7],
    91: [25, 72, 11]}
    
if __name__ == "__main__":
    print(", ".join(plato_archi_nets.keys()))