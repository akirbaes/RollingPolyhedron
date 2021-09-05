from sage.all import *
import os
import pprint
from copy import deepcopy
# sage -python findTilingSymmetriesUsingSage.py
SAVEGRAPHES = False

from tiling_dicts.uniform_tilings import uniform_tilings as all_tilings

MAX_ANTENNAE_AMOUNT = 12
#None for all
#12 works too


#Contrary to polyhedron, tilings can have different plane representations
#This was an issue for "3uhv34 (3x4^2x6;3x4x6x4;4^4)"]

def modify_net(net,face,ori):
    n = len(net)
    currentface = n
    sides = len(net[face])
    size=1
    net[currentface]=[face]
    net[face].append(currentface)
    currentface+=1
    size+=1
    # print("Max antennae",maxantennae)
    antennasides = size if MAX_ANTENNAE_AMOUNT==None else (MAX_ANTENNAE_AMOUNT-1)
    # print("sides to mark:",antennasides,"/",sides)

    for i in range(min(sides,antennasides)):
        index = (i+ori)%sides
        f = net[face][index]
        for k in range(size):
            net[f].append(currentface)
            net[currentface]=[f]
            f=currentface
            currentface+=1
        size+=1


def generate_classes(net,netname,original_tiles):
    classes = list()
    # print(net)
    for face1 in sorted(net):
        if(face1 in original_tiles):
            classes.append([])
            for ori1 in range(len(net[face1])):
                classes[-1].append(set())
                classes[-1][-1].add((face1,ori1))
            # classes[(face1,ori1)]=set()
    # for idx, x in numpy.ndenumerate(FFOO):
    #     f1,f2,ori1,ori2 = idx
    #     if(x):
    #         classes[f1,ori1].add((f2,ori2))

    modified = list()
    for face1 in sorted(net):
        if(face1 in original_tiles):
            modified.append([])
            for ori1 in range(len(net[face1])):
                modified_net = deepcopy(net)
                modify_net(modified_net,face1,ori1)
                # modified[-1].append((modified_net))
                g = Graph(modified_net)
                modified[-1].append(g)
                if(SAVEGRAPHES):
                    p=g.plot()
                    # p.show()
                    p.save("symmetry_classes/"+netname+"/"+netname+"_"+str(face1)+"-"+str(ori1)+'.png')

    for face1 in sorted(net):
        if(face1 in original_tiles):
            for ori1 in range(len(net[face1])):
                for face2 in sorted(net):
                    if(face2 in original_tiles):
                        for ori2 in range(len(net[face2])):
                            if modified[face1][ori1].is_isomorphic(modified[face2][ori2]):
                                classes[face1][ori1].add((face2, ori2))
    droplevel = list()
    print(classes)
    for clas in classes:
        droplevel.extend(clas)
    classes_unique = set( tuple(sorted(clas)) for clas in droplevel )
    return sorted(classes_unique)


def oblongue(til):
    addindex = len(til)
    def matching(cell,nid):
        n, nid = nid
        for index,data in enumerate(til[n]):
            if type(data)==tuple:
                (m, mid)=data
                if m==cell and (nid==-mid or mid==nid):
                    return index

    for cell in list(til):
        for i in range(len(til[cell])):
            if type(til[cell][i])==tuple:
                n,id = til[cell][i]
                til[n][matching(cell,(n,id))]=addindex
                til[cell][i]=addindex
                til[addindex]= [cell,n]
                # if(n!=cell): #not sure how it would cause a problem
                #     til[addindex]= [cell,n]
                # else:
                #     til[addindex]= [cell,addindex+1]
                #     til[addindex+1]= [n,addindex]
                #     addindex+=1
                addindex+=1
    return til



def firstdraft():
    all_symmetries = dict()
    for tilingname in all_tilings:#["snub_cube"]:#['hexagonal_prism']:  # all_nets:
    # for tilingname in ["3uhv34 (3x4^2x6;3x4x6x4;4^4)"]:#["snub_cube"]:#['hexagonal_prism']:  # all_nets:
        print(tilingname)
        tiling: dict = all_tilings[tilingname]
        original_tiles = list(range(len(tiling)))
        tiling = oblongue(tiling)
        g = Graph(tiling)
        if(SAVEGRAPHES):
            p=g.plot()
            try:os.mkdir("symmetry_classes/"+tilingname)
            except:pass
            p.save("symmetry_classes/"+tilingname+"/"+tilingname+'.png')
        # input()
        classes = generate_classes(tiling,tilingname,original_tiles)
        clasp = pprint.pformat(classes)
        print(len(classes), "classes")
        print(clasp)
        # try:
            # os.mkdir("symmetry_classes/SAGE")
        # except:
            # pass
        # f = open("symmetry_classes/SAGE/" + netname + "_" + "SAGE" +"A%s"%MAX_ANTENNAE_AMOUNT+ ".txt", "w")
        # f.write(clasp)
        # f.close()
        all_symmetries[tilingname] = classes



    all = pprint.pformat(all_symmetries)
    f = open("symmetry_classes/" + "_TILINGS_" + "SAGE"  +"A%s"%MAX_ANTENNAE_AMOUNT+ " test.py", "w")
    f.write(all)
    f.close()

if __name__ == "__main__":
    # for antenna in (0,1,2,None):
    #     print("Antenna mode",antenna)
    #     global MAX_ANTENNAE_AMOUNT
    #     MAX_ANTENNAE_AMOUNT = antenna
        # input()

    firstdraft()
    # print("Done with ",antenna,"antennae modifier")
    print("All done")