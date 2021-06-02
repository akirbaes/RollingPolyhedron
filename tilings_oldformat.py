#each dict is a tiling of form:
#{startface: [neighbours in clockwise order]}
#faces from 0 to p-1
#p = number of polygonal faces in the tiling
#match neighbour in startface and startface in neighbour
#unless startface has more than one neighbour of the same face, then
#startface: [neighbour+kp]
#neighbour: [startface+kp] : match identical k
#if startface is linked to itelf:
#with a centrosymmetry:
#startface: [startface+kp] with unique k for each centrosymmetry
#linked in a chain of itself:
#startface: [startface+kp, startface-kp] with shared k between the two

#In addition, by convention, neighbours internal to a tile are k==0
#internal neighbour: 0<=neighbour<p (or neighbour%p==neighbour)
#neighbour going outside the starting tile are
#neighbour+kp (just to be sure even if there are no duplicates)

#p = len(tiling)
#extract faceid = n%p
#extract k = n//p
#invert k: -n + 2*n%p
#matching rule:
#k==0: match with other k==0 directly
#k!=0: try to match with -k, otherwise, try to match with k

#can be simplified to: try to match with -k, then with --k

platonics = dict()
platonics["3^6"] = {
    0: [1, 2, 3]
}

platonics["4^4"] = {
    0: [1, 2, -1, -2]
}

platonics["6^3"] = {
    0: [1, 2, 3, -1, -2, -3]
}

archimedeans = dict()

p = 3
archimedeans["3^3x4^2"] = {
    0: [1, 0 + p, 2, 0 - p],
    1: [0, 2 + p, 2 + 2 * p],
    2: [0, 1 + p, 1 + 2 * p]
}

p = 6
archimedeans["3^2x4x3x4"] = {
    0: [1, 4, 5, 3 + p],
    1: [5 + p, 2, 0],
    2: [3, 1, 4 + p, 5 + p],
    3: [4, 2, 0 + p],
    4: [0, 3, 2 + p],
    5: [0, 1 + p, 2 + p]
}

p = 6
archimedeans["3x4x6x4"] = {
    0: [1, 3, 5, 1 + p, 3 + p, 5 + p],
    1: [2, 0, 4 + p, 0 + p],
    2: [3, 1, 5 + p],
    3: [4, 0, 2, 0 + p],
    4: [5, 3, 1 + p],
    5: [0, 4, 0 + p, 2 + p]
}

p = 3
archimedeans["3x6x3x6"] = {
    0: [1, 2, 1 + p, 2 + 2 * p, 1 + 2 * p, 2 + p],
    1: [0, 0 + p, 0 + 2 * p],
    2: [0, 0 + 2 * p, 0 + p]
}

p = 3
archimedeans["3x12^2"] = {
    0: [1, 0 + p, 2, 0 + 2 * p, 1 + 3 * p, 0 + 3 * p, 2 + p, 0 - p, 1 + p, 0 - 2 * p, 2 + 2 * p, 0 - 3 * p],
    1: [0, 0 + 3 * p, 0 + p],
    2: [0, 0 + p, 0 + 2 * p]
}

p = 6
archimedeans["4x6x12"] = {
    0: [1, 2, 3, 4, 5, 2 + p, 1 + p, 4 + 2 * p, 3 + p, 2 + 2 * p, 5 + p, 4 + p],
    1: [2, 0, 4 + p, 0 + p],
    2: [3, 0, 1, 0 + p, 5 + p, 0 + 2 * p],
    3: [4, 0, 2, 0 + p],
    4: [5, 0, 3, 0 + 2 * p, 1 + p, 0 + p],
    5: [0, 4, 0 + p, 2 + p]

}

p = 2
archimedeans["4x8^2"] = {
    0: [1, 0 + p, 1 + p, 0 + 2 * p, 1 + 3 * p, 0 - p, 1 + 2 * p, 0 - 2 * p],
    1: [0, 0 + p, 0 + 3 * p, 0 + 2 * p]
}

p = 9
archimedeans["3^4x6"] = {
    0: [1, 2, 3, 4, 6 + p, 8 + p],
    1: [5, 0, 4 + p],
    2: [0, 6, 7],
    3: [0, 8, 5 + p],
    4: [0, 1 + p, 7 + p],
    5: [6, 1, 3 + p],
    6: [2, 5, 0 + p],
    7: [8, 2, 4 + p],
    8: [3, 7, 0 + p]
}

test = {
    0: [],
    1: [],
    2: [],
    3: [],
    4: [],
    5: []

}

all_tilings = {**platonics, **archimedeans}