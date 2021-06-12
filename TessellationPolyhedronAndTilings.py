tessellation_polyhedrons = {
    'cube': {   0: [1, 2, 4, 3],
                1: [0, 3, 5, 2],
                2: [0, 1, 5, 4],
                3: [0, 4, 5, 1],
                4: [0, 2, 5, 3],
                5: [1, 3, 4, 2]},
    'hexagonal_antiprism': {   0: [1, 8, 3],
                               1: [0, 2, 10],
                               2: [1, 3, 5, 7, 13, 11],
                               3: [2, 0, 4],
                               4: [5, 3, 8],
                               5: [2, 4, 6],
                               6: [5, 8, 7],
                               7: [6, 9, 2],
                               8: [10, 12, 9, 6, 4, 0],
                               9: [8, 13, 7],
                               10: [11, 8, 1],
                               11: [10, 2, 12],
                               12: [13, 8, 11],
                               13: [12, 2, 9]},
    'icosahedron': {   0: [1, 4, 5],
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
                       19: [18, 15, 13]},
    'j1': {   0: [1, 2, 3, 4],
              1: [2, 0, 4],
              2: [1, 3, 0],
              3: [4, 0, 2],
              4: [3, 1, 0]},
    'j10': {   0: [7, 1, 8],
               1: [0, 12, 2],
               2: [1, 3, 9],
               3: [2, 12, 4],
               4: [3, 5, 10],
               5: [4, 12, 6],
               6: [5, 7, 11],
               7: [6, 12, 0],
               8: [0, 9, 11],
               9: [2, 10, 8],
               10: [4, 11, 9],
               11: [6, 8, 10],
               12: [3, 1, 7, 5]},
    'j12': {   0: [2, 1, 3],
               1: [2, 4, 0],
               2: [0, 5, 1],
               3: [4, 5, 0],
               4: [1, 5, 3],
               5: [4, 2, 3]},
    'j13': {   0: [6, 1, 3],
               1: [2, 4, 0],
               2: [8, 5, 1],
               3: [4, 7, 0],
               4: [1, 5, 3],
               5: [4, 2, 9],
               6: [0, 7, 8],
               7: [3, 9, 6],
               8: [2, 6, 9],
               9: [5, 8, 7]},
    'j14': {   0: [3, 2, 1],
               1: [4, 0, 2],
               2: [5, 1, 0],
               3: [0, 4, 6, 5],
               4: [1, 5, 7, 3],
               5: [8, 4, 2, 3],
               6: [3, 7, 8],
               7: [4, 8, 6],
               8: [5, 6, 7]},
    'j15': {   0: [3, 9, 1],
               1: [4, 0, 2],
               2: [5, 1, 9],
               3: [0, 4, 6, 10],
               4: [1, 5, 7, 3],
               5: [8, 4, 2, 10],
               6: [3, 7, 11],
               7: [4, 8, 6],
               8: [5, 11, 7],
               9: [10, 2, 0],
               10: [9, 3, 11, 5],
               11: [10, 6, 8]},
    'j16': {   0: [3, 9, 1],
               1: [4, 0, 2],
               2: [5, 1, 12],
               3: [0, 4, 6, 10],
               4: [1, 5, 7, 3],
               5: [8, 4, 2, 13],
               6: [3, 7, 11],
               7: [4, 8, 6],
               8: [5, 14, 7],
               9: [10, 12, 0],
               10: [9, 3, 11, 13],
               11: [10, 6, 14],
               12: [13, 2, 9],
               13: [14, 5, 12, 10],
               14: [13, 11, 8]},
    'j17': {   0: [7, 1, 8],
               1: [0, 12, 2],
               2: [1, 3, 9],
               3: [2, 13, 4],
               4: [3, 5, 10],
               5: [4, 14, 6],
               6: [5, 7, 11],
               7: [6, 15, 0],
               8: [0, 9, 11],
               9: [2, 10, 8],
               10: [4, 11, 9],
               11: [6, 8, 10],
               12: [1, 15, 13],
               13: [3, 12, 14],
               14: [5, 13, 15],
               15: [7, 14, 12]},
    'j49': {   0: [3, 6, 1, 5],
               1: [0, 6, 7, 5],
               2: [7, 3, 5],
               3: [4, 0, 2],
               4: [3, 7, 6],
               5: [0, 1, 2],
               6: [0, 4, 1],
               7: [1, 4, 2]},
    'j50': {   0: [4, 7, 5, 2],
               1: [4, 2, 10],
               2: [1, 0, 3],
               3: [2, 5, 10],
               4: [0, 1, 6],
               5: [0, 8, 3],
               6: [4, 9, 7],
               7: [6, 8, 0],
               8: [7, 9, 5],
               9: [6, 10, 8],
               10: [3, 9, 1]},
    'j51': {   0: [13, 2, 11],
               1: [4, 2, 5],
               2: [3, 0, 1],
               3: [4, 10, 2],
               4: [7, 3, 1],
               5: [13, 6, 1],
               6: [5, 9, 7],
               7: [6, 8, 4],
               8: [7, 9, 10],
               9: [6, 12, 8],
               10: [8, 11, 3],
               11: [10, 12, 0],
               12: [9, 13, 11],
               13: [12, 5, 0]},
    'j8': {   0: [1, 8, 3],
              1: [0, 2, 7],
              2: [4, 1, 3],
              3: [5, 2, 0],
              4: [2, 5, 6, 7],
              5: [4, 3, 8, 6],
              6: [7, 4, 5, 8],
              7: [6, 8, 1, 4],
              8: [7, 6, 5, 0]},
    'j84': {   0: [3, 1, 11],
               1: [0, 4, 2],
               2: [1, 5, 8],
               3: [4, 0, 9],
               4: [3, 5, 1],
               5: [4, 6, 2],
               6: [9, 7, 5],
               7: [6, 10, 8],
               8: [7, 11, 2],
               9: [10, 6, 3],
               10: [9, 11, 7],
               11: [10, 0, 8]},
    'j86': {   0: [1, 4, 10],
               1: [2, 0, 12],
               2: [1, 3, 4],
               3: [2, 13, 5],
               4: [2, 5, 6, 0],
               5: [7, 4, 3, 9],
               6: [7, 10, 4],
               7: [5, 8, 6],
               8: [7, 9, 11],
               9: [8, 5, 13],
               10: [11, 0, 6],
               11: [10, 8, 12],
               12: [11, 13, 1],
               13: [12, 9, 3]},
    'j87': {   0: [14, 16, 1],
               1: [0, 9, 11, 7],
               2: [12, 4, 13],
               3: [5, 6, 13],
               4: [2, 8, 5],
               5: [4, 15, 3],
               6: [14, 7, 3],
               7: [6, 1, 10],
               8: [9, 16, 4],
               9: [8, 12, 1],
               10: [11, 13, 7],
               11: [1, 12, 10],
               12: [11, 9, 2],
               13: [10, 2, 3],
               14: [15, 0, 6],
               15: [5, 16, 14],
               16: [15, 8, 0]},
    'j88': {   0: [3, 8, 5, 1],
               1: [6, 0, 7],
               2: [3, 6, 12],
               3: [13, 0, 2],
               4: [5, 10, 7],
               5: [0, 11, 4],
               6: [2, 1, 16],
               7: [1, 4, 14],
               8: [11, 0, 13, 9],
               9: [15, 8, 17],
               10: [11, 15, 4],
               11: [5, 8, 10],
               12: [13, 2, 17],
               13: [8, 3, 12],
               14: [15, 16, 7],
               15: [10, 9, 14],
               16: [17, 6, 14],
               17: [9, 12, 16]},
    'j89': {   0: [3, 8, 5, 1],
               1: [6, 0, 7],
               2: [3, 6, 15],
               3: [10, 0, 2],
               4: [5, 13, 7],
               5: [0, 9, 4],
               6: [2, 1, 19],
               7: [1, 4, 17],
               8: [11, 9, 0, 10],
               9: [8, 14, 5],
               10: [8, 3, 16],
               11: [14, 8, 16, 12],
               12: [18, 11, 20],
               13: [14, 18, 4],
               14: [9, 11, 13],
               15: [16, 2, 20],
               16: [11, 10, 15],
               17: [18, 19, 7],
               18: [13, 12, 17],
               19: [20, 6, 17],
               20: [12, 15, 19]},
    'j90': {   0: [1, 11, 3],
               1: [21, 0, 4, 2],
               2: [1, 5, 20],
               3: [4, 0, 7],
               4: [1, 3, 6, 5],
               5: [4, 18, 2],
               6: [8, 17, 4],
               7: [3, 12, 8],
               8: [7, 9, 6],
               9: [8, 10, 16],
               10: [12, 14, 15, 9],
               11: [0, 13, 12],
               12: [7, 11, 10],
               13: [11, 21, 14],
               14: [13, 23, 10],
               15: [10, 23, 19, 16],
               16: [9, 15, 17],
               17: [16, 18, 6],
               18: [19, 5, 17],
               19: [15, 20, 18],
               20: [19, 22, 2],
               21: [22, 13, 1],
               22: [23, 21, 20],
               23: [14, 22, 15]},
    'octahedron': {   0: [1, 7, 3],
                      1: [0, 2, 6],
                      2: [1, 3, 5],
                      3: [4, 2, 0],
                      4: [5, 3, 7],
                      5: [4, 6, 2],
                      6: [5, 7, 1],
                      7: [6, 4, 0]},
    'tetrahedron': {0: [1, 2, 3], 1: [2, 0, 3], 2: [0, 1, 3], 3: [0, 2, 1]}
}

net_tessellations = {
    'cube': {   0: [(1, 0), (2, 0), (4, 0), (3, 0)],
                1: [(0, 0), (2, 1), (5, 0), (5, 1)],
                2: [(0, 0), (5, 1), (1, -1), (3, 1)],
                3: [(0, 0), (4, 1), (4, 2), (2, -1)],
                4: [(0, 0), (3, -2), (3, -1), (4, 1)],
                5: [(5, 1), (2, -1), (1, -1), (1, 0)]},
    'hexagonal_antiprism': {   0: [(1, 0), (2, 1), (7, 1)],
                               1: [(0, 0), (2, 0), (2, 1)],
                               2: [   (1, 0),
                                      (3, 0),
                                      (5, 0),
                                      (0, -1),
                                      (2, 0),
                                      (1, -1)],
                               3: [(2, 0), (7, 1), (9, 1)],
                               4: [(5, 0), (9, 1), (13, 1)],
                               5: [(2, 0), (4, 0), (6, 0)],
                               6: [(5, 0), (8, 0), (7, 0)],
                               7: [(6, 0), (3, -1), (0, -1)],
                               8: [   (10, 0),
                                      (12, 0),
                                      (9, 0),
                                      (6, 0),
                                      (13, 1),
                                      (10, 1)],
                               9: [(8, 0), (4, -1), (3, -1)],
                               10: [(11, 0), (8, 0), (8, -1)],
                               11: [(10, 0), (12, 1), (11, 0)],
                               12: [(13, 0), (8, 0), (11, -1)],
                               13: [(12, 0), (8, -1), (4, -1)]},
    'icosahedron': {   0: [(9, 1), (8, 2), (1, 0)],
                       1: [(0, 0), (7, 3), (2, 0)],
                       2: [(1, 0), (9, 0), (3, 0)],
                       3: [(2, 0), (11, 0), (4, 0)],
                       4: [(3, 0), (10, 5), (9, 4)],
                       5: [(6, 0), (8, 11), (16, 10)],
                       6: [(15, 0), (7, 0), (5, 0)],
                       7: [(6, 0), (8, 0), (1, 3)],
                       8: [(7, 0), (5, 11), (0, 2)],
                       9: [(2, 0), (0, 1), (4, 4)],
                       10: [(11, 0), (4, 5), (14, 6)],
                       11: [(3, 0), (10, 0), (12, 0)],
                       12: [(11, 0), (18, 0), (14, 0)],
                       13: [(19, 0), (16, 9), (17, 8)],
                       14: [(12, 0), (17, 7), (10, 6)],
                       15: [(19, 0), (16, 0), (6, 0)],
                       16: [(15, 0), (13, 9), (5, 10)],
                       17: [(18, 0), (14, 7), (13, 8)],
                       18: [(12, 0), (17, 0), (19, 0)],
                       19: [(18, 0), (15, 0), (13, 0)]},
    'j1': {   0: [(1, 0), (0, -1), (3, 0), (0, 1)],
              1: [(2, 0), (0, 0), (2, 1)],
              2: [(1, 0), (4, 1), (1, -1)],
              3: [(4, 0), (0, 0), (4, 1)],
              4: [(3, 0), (2, -1), (3, -1)]},
    'j10': {   0: [(8, 0), (10, -2), (4, -1)],
               1: [(2, 0), (4, 1), (12, -1)],
               2: [(1, 0), (3, 0), (9, 0)],
               3: [(2, 0), (12, 0), (4, 0)],
               4: [(3, 0), (1, -1), (0, 1)],
               5: [(6, 0), (11, -1), (7, 1)],
               6: [(5, 0), (7, 0), (11, 0)],
               7: [(6, 0), (5, -1), (10, 1)],
               8: [(0, 0), (9, 0), (11, 0)],
               9: [(2, 0), (10, 0), (8, 0)],
               10: [(9, 0), (0, 2), (7, -1)],
               11: [(6, 0), (8, 0), (5, 1)],
               12: [(3, 0), (12, 0), (1, 1), (12, 1)]},
    'j12': {   0: [(3, 1), (1, 0), (5, 1)],
               1: [(2, 0), (4, 0), (0, 0)],
               2: [(5, 1), (3, 1), (1, 0)],
               3: [(4, 0), (0, 1), (2, 1)],
               4: [(1, 0), (5, 0), (3, 0)],
               5: [(4, 0), (0, 1), (2, 1)]},
    'j13': {   0: [(6, 0), (1, 0), (3, 0)],
               1: [(2, 0), (8, 1), (0, 0)],
               2: [(9, 1), (5, 1), (1, 0)],
               3: [(4, 0), (7, 0), (0, 0)],
               4: [(6, 1), (5, 0), (3, 0)],
               5: [(4, 0), (7, 1), (2, 1)],
               6: [(0, 0), (4, 1), (8, 0)],
               7: [(3, 0), (9, 0), (5, 1)],
               8: [(9, 1), (6, 0), (1, 1)],
               9: [(2, 1), (8, 1), (7, 0)]},
    'j14': {   0: [(3, 0), (6, 1), (7, 1)],
               1: [(4, 0), (7, 1), (8, 1)],
               2: [(5, 0), (8, 1), (6, 1)],
               3: [(0, 0), (4, 0), (6, 0), (5, 1)],
               4: [(1, 0), (5, 0), (7, 0), (3, 0)],
               5: [(8, 0), (4, 0), (2, 0), (3, -1)],
               6: [(3, 0), (0, -1), (2, -1)],
               7: [(4, 0), (1, -1), (0, -1)],
               8: [(5, 0), (2, -1), (1, -1)]},
    'j15': {   0: [(3, 0), (6, 1), (7, 1)],
               1: [(4, 0), (7, 1), (8, 1)],
               2: [(5, 0), (8, 1), (11, 1)],
               3: [(0, 0), (4, 0), (6, 0), (10, 0)],
               4: [(1, 0), (5, 0), (7, 0), (3, 0)],
               5: [(8, 0), (4, 0), (2, 0), (10, 1)],
               6: [(3, 0), (0, -1), (9, 1)],
               7: [(4, 0), (1, -1), (0, -1)],
               8: [(5, 0), (2, -1), (1, -1)],
               9: [(10, 0), (11, 1), (6, -1)],
               10: [(9, 0), (3, 0), (11, 0), (5, -1)],
               11: [(10, 0), (9, -1), (2, -1)]},
    'j16': {   0: [(3, 0), (6, 1), (7, 1)],
               1: [(4, 0), (7, 1), (8, 1)],
               2: [(5, 0), (8, 1), (14, 1)],
               3: [(0, 0), (4, 0), (6, 0), (10, 0)],
               4: [(1, 0), (5, 0), (7, 0), (3, 0)],
               5: [(8, 0), (4, 0), (2, 0), (13, 0)],
               6: [(3, 0), (0, -1), (9, 1)],
               7: [(4, 0), (1, -1), (0, -1)],
               8: [(5, 0), (2, -1), (1, -1)],
               9: [(10, 0), (11, 1), (6, -1)],
               10: [(9, 0), (3, 0), (11, 0), (13, 1)],
               11: [(10, 0), (9, -1), (12, 1)],
               12: [(13, 0), (14, 1), (11, -1)],
               13: [(14, 0), (5, 0), (12, 0), (10, -1)],
               14: [(13, 0), (12, -1), (2, -1)]},
    'j17': {   0: [(7, 0), (1, 0), (8, 0)],
               1: [(0, 0), (12, 0), (2, 0)],
               2: [(1, 0), (3, 0), (9, 0)],
               3: [(2, 0), (13, 0), (4, 0)],
               4: [(3, 0), (11, 1), (10, 0)],
               5: [(13, 1), (14, 0), (6, 0)],
               6: [(5, 0), (7, 0), (11, 0)],
               7: [(6, 0), (15, 0), (0, 0)],
               8: [(0, 0), (15, 1), (14, 1)],
               9: [(2, 0), (12, 1), (15, 1)],
               10: [(4, 0), (13, 1), (12, 1)],
               11: [(6, 0), (14, 1), (4, 1)],
               12: [(1, 0), (9, 1), (10, 1)],
               13: [(3, 0), (10, 1), (5, 1)],
               14: [(5, 0), (11, 1), (8, 1)],
               15: [(7, 0), (8, 1), (9, 1)]},
    'j49': {   0: [(1, 1), (6, 1), (1, 2), (1, 0)],
               1: [(0, 0), (0, 2), (7, 0), (0, 1)],
               2: [(2, 1), (3, 0), (5, 0)],
               3: [(4, 0), (3, 1), (2, 0)],
               4: [(3, 0), (7, 0), (6, 0)],
               5: [(6, 1), (7, 1), (2, 0)],
               6: [(5, 1), (4, 0), (0, 1)],
               7: [(1, 0), (4, 0), (5, 1)]},
    'j50': {   0: [(0, -1), (7, 0), (0, 1), (2, 0)],
               1: [(4, 0), (10, 1), (10, 0)],
               2: [(3, 1), (0, 0), (3, 0)],
               3: [(2, 0), (2, 1), (10, 0)],
               4: [(5, 2), (1, 0), (5, 1)],
               5: [(4, 2), (8, 0), (4, 1)],
               6: [(7, 1), (9, 0), (7, 0)],
               7: [(6, 0), (6, 1), (0, 0)],
               8: [(9, 1), (9, 0), (5, 0)],
               9: [(6, 0), (8, 1), (8, 0)],
               10: [(3, 0), (1, 1), (1, 0)]},
    'j51': {   0: [(1, 1), (2, 0), (10, 1)],
               1: [(4, 0), (0, 1), (5, 0)],
               2: [(3, 0), (0, 0), (2, 1)],
               3: [(4, 0), (7, 1), (2, 0)],
               4: [(7, 0), (3, 0), (1, 0)],
               5: [(13, 0), (6, 0), (1, 0)],
               6: [(5, 0), (9, 1), (8, 1)],
               7: [(8, 1), (3, 1), (4, 0)],
               8: [(7, 1), (6, 1), (10, 0)],
               9: [(9, 1), (12, 0), (6, 1)],
               10: [(8, 0), (11, 0), (0, 1)],
               11: [(10, 0), (12, 0), (13, 1)],
               12: [(9, 0), (13, 0), (11, 0)],
               13: [(12, 0), (5, 0), (11, 1)]},
    'j8': {   0: [(1, 0), (3, 1), (2, 1)],
              1: [(0, 0), (2, 0), (3, 1)],
              2: [(4, 0), (1, 0), (0, -1)],
              3: [(5, 0), (0, -1), (1, -1)],
              4: [(2, 0), (5, 0), (6, 0), (5, 1)],
              5: [(4, 0), (3, 0), (4, -1), (7, 1)],
              6: [(7, 0), (4, 0), (7, 1), (8, 1)],
              7: [(6, 0), (8, 0), (6, -1), (5, -1)],
              8: [(7, 0), (8, 0), (6, -1), (8, 2)]},
    'j84': {   0: [(3, 0), (1, 0), (11, 0)],
               1: [(0, 0), (4, 0), (2, 0)],
               2: [(1, 0), (5, 0), (8, 0)],
               3: [(10, 1), (0, 0), (9, 0)],
               4: [(11, 1), (8, 1), (1, 0)],
               5: [(7, 1), (9, 1), (2, 0)],
               6: [(10, 1), (7, 0), (9, 1)],
               7: [(6, 0), (5, 1), (8, 0)],
               8: [(7, 0), (4, 1), (2, 0)],
               9: [(6, 1), (5, 1), (3, 0)],
               10: [(6, 1), (11, 0), (3, 1)],
               11: [(10, 0), (0, 0), (4, 1)]},
    'j86': {   0: [(1, 0), (5, 1), (3, 1)],
               1: [(2, 0), (0, 0), (12, 1)],
               2: [(1, 0), (3, 0), (4, 0)],
               3: [(2, 0), (10, 1), (0, -1)],
               4: [(2, 0), (5, 0), (9, 1), (5, 1)],
               5: [(7, 0), (4, 0), (0, -1), (4, -1)],
               6: [(7, 0), (13, 1), (9, 1)],
               7: [(5, 0), (8, 0), (6, 0)],
               8: [(7, 0), (9, 0), (11, 0)],
               9: [(8, 0), (4, -1), (6, -1)],
               10: [(11, 0), (3, -1), (13, 1)],
               11: [(10, 0), (8, 0), (12, 0)],
               12: [(11, 0), (13, 0), (1, -1)],
               13: [(12, 0), (6, -1), (10, -1)]},
    'j87': {   0: [(14, 0), (16, 0), (15, 1)],
               1: [(7, 1), (1, 2), (11, 0), (1, 1)],
               2: [(12, 0), (4, 0), (13, 0)],
               3: [(5, 0), (8, 1), (9, 1)],
               4: [(2, 0), (8, 0), (5, 0)],
               5: [(4, 0), (15, 0), (3, 0)],
               6: [(11, 1), (7, 0), (12, 1)],
               7: [(6, 0), (1, 1), (10, 0)],
               8: [(3, 1), (16, 0), (4, 0)],
               9: [(3, 1), (12, 0), (13, 1)],
               10: [(11, 0), (13, 0), (7, 0)],
               11: [(1, 0), (6, 1), (10, 0)],
               12: [(6, 1), (9, 0), (2, 0)],
               13: [(10, 0), (2, 0), (9, 1)],
               14: [(16, 1), (0, 0), (15, 1)],
               15: [(5, 0), (14, 1), (0, 1)],
               16: [(14, 1), (8, 0), (0, 0)]},
    'j88': {   0: [(3, 0), (8, 0), (5, 0), (8, 1)],
               1: [(6, 0), (1, 1), (7, 1)],
               2: [(14, 1), (6, 0), (12, 0)],
               3: [(17, 1), (0, 0), (12, 1)],
               4: [(5, 0), (10, 0), (11, 1)],
               5: [(0, 0), (9, 1), (4, 0)],
               6: [(2, 0), (1, 0), (16, 0)],
               7: [(7, 1), (1, 1), (14, 0)],
               8: [(11, 0), (0, 0), (13, 0), (0, 1)],
               9: [(15, 0), (5, 1), (11, 1)],
               10: [(10, 1), (15, 0), (4, 0)],
               11: [(9, 1), (8, 0), (4, 1)],
               12: [(13, 0), (2, 0), (3, 1)],
               13: [(8, 0), (17, 1), (12, 0)],
               14: [(2, 1), (16, 0), (7, 0)],
               15: [(10, 0), (9, 0), (15, 1)],
               16: [(17, 0), (6, 0), (14, 0)],
               17: [(13, 1), (3, 1), (16, 0)]},
    'j89': {   0: [(3, 0), (8, 0), (5, 0), (11, 1)],
               1: [(6, 0), (5, 1), (9, 1)],
               2: [(13, 1), (6, 0), (15, 0)],
               3: [(20, 1), (0, 0), (15, 1)],
               4: [(5, 0), (13, 0), (14, 1)],
               5: [(0, 0), (1, 1), (4, 0)],
               6: [(2, 0), (1, 0), (19, 0)],
               7: [(9, 1), (14, 1), (17, 0)],
               8: [(11, 0), (9, 0), (0, 0), (10, 0)],
               9: [(8, 0), (7, 1), (1, 1)],
               10: [(8, 0), (20, 1), (12, 1)],
               11: [(14, 0), (8, 0), (16, 0), (0, 1)],
               12: [(18, 0), (16, 1), (10, 1)],
               13: [(2, 1), (18, 0), (4, 0)],
               14: [(7, 1), (11, 0), (4, 1)],
               15: [(16, 1), (2, 0), (3, 1)],
               16: [(11, 0), (12, 1), (15, 1)],
               17: [(18, 0), (19, 0), (7, 0)],
               18: [(13, 0), (12, 0), (17, 0)],
               19: [(20, 0), (6, 0), (17, 0)],
               20: [(10, 1), (3, 1), (19, 0)]},
    'j90': {   0: [(1, 0), (11, 0), (3, 0)],
               1: [(4, 1), (0, 0), (4, 0), (2, 0)],
               2: [(1, 0), (21, 1), (20, 0)],
               3: [(13, 1), (0, 0), (7, 0)],
               4: [(1, 0), (13, 1), (1, 1), (5, 0)],
               5: [(4, 0), (20, 1), (21, 1)],
               6: [(12, 1), (17, 0), (7, 1)],
               7: [(3, 0), (6, 1), (8, 0)],
               8: [(7, 0), (9, 0), (12, 1)],
               9: [(8, 0), (18, 1), (16, 0)],
               10: [(15, 1), (14, 0), (15, 0), (18, 1)],
               11: [(0, 0), (13, 0), (12, 0)],
               12: [(6, 1), (11, 0), (8, 1)],
               13: [(11, 0), (4, 1), (3, 1)],
               14: [(22, 1), (19, 1), (10, 0)],
               15: [(10, 0), (23, 0), (10, 1), (16, 0)],
               16: [(9, 0), (15, 0), (17, 0)],
               17: [(16, 0), (18, 0), (6, 0)],
               18: [(10, 1), (9, 1), (17, 0)],
               19: [(14, 1), (20, 0), (23, 1)],
               20: [(19, 0), (5, 1), (2, 0)],
               21: [(22, 0), (2, 1), (5, 1)],
               22: [(23, 0), (21, 0), (14, 1)],
               23: [(19, 1), (22, 0), (15, 0)]},
    'octahedron': {   0: [(1, 0), (7, 1), (1, 1)],
                      1: [(0, 0), (2, 0), (0, -1)],
                      2: [(1, 0), (3, 0), (3, 1)],
                      3: [(4, 0), (2, 0), (2, -1)],
                      4: [(5, 0), (3, 0), (5, 1)],
                      5: [(4, 0), (6, 0), (4, -1)],
                      6: [(5, 0), (7, 0), (7, 1)],
                      7: [(6, 0), (6, -1), (0, -1)]},
    'tetrahedron': {   0: [(1, 0), (2, 0), (3, 0)],
                       1: [(3, -1), (2, -2), (0, 0)],
                       2: [(0, 0), (1, 2), (3, -3)],
                       3: [(0, 0), (2, 3), (1, 1)]}
}

