#dict[face]=[neighbour_face ...]
plato_archi_nets= dict()
plato_archi_nets['cube'] = \
{   0: [2, 3, 4, 1],
    1: [5, 2, 0, 4],
    2: [5, 3, 0, 1],
    3: [5, 4, 0, 2],
    4: [0, 3, 5, 1],
    5: [3, 2, 1, 4]}

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


plato_archi_nets['octahedron'] = \
{   0: [3, 1, 7],
    1: [0, 2, 6],
    2: [1, 3, 5],
    3: [2, 0, 4],
    4: [7, 5, 3],
    5: [4, 6, 2],
    6: [5, 7, 1],
    7: [6, 4, 0]}

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

plato_archi_nets['tetrahedron'] = \
{0: [1, 2, 3], 1: [2, 0, 3], 2: [0, 1, 3], 3: [2, 1, 0]}

plato_archi_nets['truncated_tetrahedron'] = \
{   0: [7, 5, 4],
    1: [7, 6, 5],
    2: [6, 4, 5],
    3: [7, 4, 6],
    4: [7, 0, 5, 2, 6, 3],
    5: [7, 1, 6, 2, 4, 0],
    6: [7, 3, 4, 2, 5, 1],
    7: [5, 0, 4, 3, 6, 1]}

