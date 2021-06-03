#!/usr/bin/python
# -*- coding: utf-8 -*
import os

from poly_dicts.johnson_nets import johnson_nets
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.prism_nets import prism_nets
from copy import deepcopy
import numpy
import pprint

all_nets = {**johnson_nets, **plato_archi_nets, **prism_nets}
bits = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"


# ▖ 	▗ 	▘ 	▙ 	▚ 	▛ 	▜ 	▝ 	▞ 	▟ ▄ 	 	▀ ▐▌█
def make_adjacency_matrix(net):
    return [
        [face2 in net[face1] for face2 in net] for face1 in net
    ]


def make_adjacency_matrix_ordered(net, faceorder):
    return [
        [face2 in net[face1] for face2 in faceorder] for face1 in faceorder
    ]


def rotate_faces(net, centralface, amount):
    # rotates by 1
    facestorotate = net[centralface]
    size = len(facestorotate)
    faceorder = sorted(net)
    for j in range(amount):
        finalorder = faceorder.copy()
        for i in range(len(facestorotate)):
            f1 = facestorotate[i]
            f2 = facestorotate[(i + 1) % size]
            finalorder[f2] = faceorder[f1]
        faceorder = finalorder
    return faceorder


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
def compare(mat1, mat2):
    for i in range(len(mat1)):
        for j in range(len(mat1[0])):
            if (mat1[i][j] != mat2[i][j]):
                return False
    return True
def generate_face_sym(net):
    Face = [{face} for face in sorted(net)]
    # Generate face sym
    order = sorted(net)
    mat = make_adjacency_matrix_ordered(net, order)
    for face1 in sorted(net):
        for face2 in sorted(net):
            if len(net[face2]) == len(net[face1]) and face2 not in Face[face1]:
                order = sorted(net)
                order[order.index(face1)], order[order.index(face2)] = order[order.index(face2)], order[
                    order.index(face1)]
                newmat = make_adjacency_matrix_ordered(net, order)
                if compare(mat, newmat):
                    Face[face1].add(face2)
                    Face[face2].add(face1)
    return Face

"""
def generate_rotation_sym(net):
    Ori = [[[n] for n in net[face]] for face in sorted(net)]
    # Generate rot sym
    for face in sorted(net):
        neighbours = net[face]
        matrices = []
        for rot in range(len(neighbours)):
            reorder = rotate_faces(net, face, rot)
            newmat = make_adjacency_matrix_ordered(net, reorder)
            if any((compare(mat, newmat) for mat in matrices)):
                pass
            else:
                matrices.append(newmat)
        print("Face %i of %i sides has %i distinct orientations" % (face, len(neighbours), len(matrices)))
"""
def canon_face(face,Face):
    return min(Face[face])
def canon_fo(face,orientation,FaceSym,FFOO):
    cface = canon_face(face,FaceSym)
    cori = orientation
    for i,val in enumerate(FFOO[face][cface][orientation]):
        if val:
            cori = i
            break
    return cface, cori

def generate_classes(net,FFOO):
    classes = dict()


    for face1 in sorted(net):
        for ori1 in range(len(net[face1])):
            classes[(face1,ori1)]=set()
    for idx, x in numpy.ndenumerate(FFOO):
        f1,f2,ori1,ori2 = idx
        if(x):
            classes[f1,ori1].add((f2,ori2))
    classes_unique = set( tuple(sorted(clas)) for clas in classes.values() )
    return sorted(classes_unique)
    # for face1 in sorted(net):
    #     for ori1 in range(len(net[face1])):
    #         for face2 in net:
    #             for ori2 in range(len(net[face2])):
    #                 FFOO[face1][face2][ori1][ori2]


def generate_FFOO_sym(net):
    maxsides = max(len(neigh) for neigh in net.values())
    FFOO = [[[[0 for o2 in range(maxsides)] for o1 in range(maxsides)] for face2 in sorted(net)] for face1 in sorted(net)]
    FFOO=numpy.array(FFOO)
    FaceSym = generate_face_sym(net)

    order = sorted(net)
    mat = make_adjacency_matrix_ordered(net, order)
    #print(Face)
    for face in sorted(net):
        for rot in range(len(net[face])):
            FFOO[face][face][rot][rot]=1
            for face2 in sorted(net):
                if(face2 in FaceSym[face]):
                    FFOO[face][face2][rot][rot]=1
                    FFOO[face2][face][rot][rot]=1

    # Generate face sym
    for face1 in sorted(net):
        for face2 in sorted(net):
            if len(net[face2]) == len(net[face1]) and face2 in FaceSym[face1]:
                order = sorted(net)
                order[order.index(face1)], order[order.index(face2)] = order[order.index(face2)], order[
                    order.index(face1)]
                newmat = make_adjacency_matrix_ordered(net, order)
                if compare(mat, newmat):
                    # Generate rot sym
                    n1 = net[face1]
                    for rot1 in range(len(n1)):
                        reorder = rotate_faces(net, face1, rot1)
                        newmat1 = make_adjacency_matrix_ordered(net, reorder)
                        n2 = net[face2]
                        for rot2 in range(len(n2)):
                            reorder = rotate_faces(net, face2, rot2)
                            newmat2 = make_adjacency_matrix_ordered(net, reorder)
                            if compare(newmat1, newmat2):
                                # print(face1,face2,rot1,rot2)
                                # print(len(FFOO),end=" ")
                                # print(len(FFOO[face1]),end=" ")
                                # print(len(FFOO[face1][face2]),end=" ")
                                # print(len(FFOO[face1][face2][rot1]),end=" ")
                                # print()
                                FFOO[face1][face2][rot1][rot2]=1
                                FFOO[face2][face1][rot2][rot1]=1

        #fill diagonals identities
    #ffoon = numpy.array(FFOO)
    return FFOO



def first_FOO_draft():
    all_symmetries = dict()
    for netname in all_nets:#["snub_cube"]:#['hexagonal_prism']:  # all_nets:
        print(netname)
        net: dict = all_nets[netname]
        # order = sorted(net)
        # prettyprint_adjacency(make_adjacency_matrix_ordered(net,order))
        # order[2],order[0]=order[0],order[2]
        # print()
        # prettyprint_adjacency(make_adjacency_matrix_ordered(net,order))




        FFOO = generate_FFOO_sym(net)
        classes = generate_classes(net,FFOO)
        clasp = pprint.pformat(classes)
        print(len(classes),"classes")
        print(clasp)
        try:os.mkdir("symmetry_classes/FFOO")
        except:pass
        f=open("symmetry_classes/FFOO/"+netname+"_"+"FFOO"+".txt","w")
        f.write(clasp)
        f.close()
        all_symmetries[netname]=classes
        # prettierprint_FFOOmatrix(FFOO, borders = True)
        #FFOO = [[[[0 for o2 in range(len(net[face2]))] for o1 in range(len(net[face1]))] for face2 in sorted(net)] for face1 in sorted(net)]
        # mat = make_adjacency_matrix(all_nets[netname])
        # print(mat)
        # prettyprint_adjacency(mat)
        # prettierprint_adjacency(mat)

    all = pprint.pformat(all_symmetries)
    f = open("symmetry_classes/" + "_" + "FFOO" + ".txt", "w")
    f.write(all)
    f.close()

if __name__ == "__main__":
    first_FOO_draft()