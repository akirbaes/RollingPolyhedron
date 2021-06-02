#!/usr/bin/python
# -*- coding: utf-8 -*
from poly_dicts.johnson_nets import johnson_nets
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.prism_nets import prism_nets
from copy import deepcopy

all_nets = {**johnson_nets, **plato_archi_nets, **prism_nets}
bits = " ▘▝▀▖▌▞▛▗▚▐▜▄▙▟█"
#▖ 	▗ 	▘ 	▙ 	▚ 	▛ 	▜ 	▝ 	▞ 	▟ ▄ 	 	▀ ▐▌█
def make_adjacency_matrix(net):
    return [
        [face2 in net[face1] for face2 in net]for face1 in net
    ]

def make_adjacency_matrix_ordered(net,faceorder):
    return [
        [face2 in net[face1] for face2 in faceorder]for face1 in faceorder
    ]
def rotate_faces(net,centralface,amount):
    #rotates by 1
    facestorotate = net[centralface]
    size = len(facestorotate)
    faceorder = sorted(net)
    for j in range(amount):
        finalorder = faceorder.copy()
        for i in range(len(facestorotate)):
            f1 = facestorotate[i]
            f2 = facestorotate[(i+1)%size]
            finalorder[f2]=faceorder[f1]
        faceorder = finalorder
    return faceorder

def prettyprint_adjacency(matrix):
    print("\n".join(["".join([it and "X" or " " for it in line]) for line in matrix]))
def prettierprint_adjacency(matrix):
    w = len(matrix[0])
    h = len(matrix)
    chars = ""
    for j in range(0,h,2):
        for i in range(0,w,2):
            number = matrix[i][j]
            try:number+=matrix[i+1][j]*2
            except:pass
            try:number+=matrix[i][j+1]*4
            except:pass
            try:number+=matrix[i+1][j+1]*8
            except:pass
            chars+=bits[number]
        chars+="\n"
    print(chars)

def compare(mat1,mat2):
    for i in range(len(mat1)):
        for j in range(len(mat1[0])):
            if(mat1[i][j]!=mat2[i][j]):
                return False
    return True

if __name__ == "__main__":
    for netname in ['hexagonal_prism']: #all_nets:
        print(netname)
        net = all_nets[netname]
        #mat = make_adjacency_matrix(all_nets[netname])
        #print(mat)
        # prettyprint_adjacency(mat)
        # prettierprint_adjacency(mat)
        copynet = deepcopy(all_nets[netname])
        for face in sorted(net):
            neighbours = net[face]
            matrices = []
            for rot in range(len(neighbours)):
                reorder = rotate_faces(net,face,rot)
                newmat = make_adjacency_matrix_ordered(net,reorder)
                if any((compare(mat,newmat) for mat in matrices)):
                    pass
                else:
                    matrices.append(newmat)
            print("Face %i of %i sides has %i distinct orientations"%(face,len(neighbours),len(matrices)))

        for face in sorted(net):


