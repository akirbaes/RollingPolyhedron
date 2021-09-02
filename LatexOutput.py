import os
import pickle

import GenPngScreenspaceRoller
from RollyPoint import RollyPoint
from tiling_dicts._1uniform_tilings import uniform1
from tiling_dicts._2uniform_tilings import uniform2
from tiling_dicts._3uniform_tilings import uniform3
from tiling_dicts.platonic_tilings import platonic_tilings
from tiling_dicts.archimedean_tilings import archimedean_tilings
# from tiling_dicts.isogonal_tilings import biisogonal_tilings
# from tiling_dicts.triisogonal_vertex_homogeneous import triisogonal_vertex_homogeneous
# all_tilings = {**platonic_tilings, **archimedean_tilings, **biisogonal_tilings, **triisogonal_vertex_homogeneous}
from tiling_dicts.uniform_tilings import uniform_tilings

all_tilings  = {**uniform_tilings}
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.johnson_nets import johnson_nets
from poly_dicts.prism_nets import prism_nets
all_nets = {**plato_archi_nets, **johnson_nets, **prism_nets}
all_nets_dict = {**plato_archi_nets, **johnson_nets, **prism_nets}

from DrawingFunctions import turn_into_image
tileurl = """https://i.imgur.com/0NvVetj.png
https://i.imgur.com/eBjngcx.png
https://i.imgur.com/5a9KBJT.png
https://i.imgur.com/O35WIdn.png
https://i.imgur.com/cFMHQEg.png
https://i.imgur.com/QunlcxR.png
https://i.imgur.com/BR3iVNA.png
https://i.imgur.com/kRvEAYw.png
https://i.imgur.com/HiK00HY.png
https://i.imgur.com/wkMNhb4.png
https://i.imgur.com/DY3tRhP.png
https://i.imgur.com/kSvh4XE.png
https://i.imgur.com/pfMgmVE.png
https://i.imgur.com/FQxRbGO.png
https://i.imgur.com/6py4GES.png
https://i.imgur.com/bES75Zp.png
https://i.imgur.com/yrkd2Td.png
https://i.imgur.com/yYlmPFb.png
https://i.imgur.com/YYohMiu.png
https://i.imgur.com/spTeWTF.png
https://i.imgur.com/ah4STKx.png
https://i.imgur.com/dl7gFm3.png
https://i.imgur.com/E38mCuu.png
https://i.imgur.com/78iFOLz.png
https://i.imgur.com/wKxSBeF.png
https://i.imgur.com/0YIadhU.png
https://i.imgur.com/WdThPkO.png
https://i.imgur.com/W6DaIXo.png
https://i.imgur.com/Qjqeo0Z.png
https://i.imgur.com/onomQdI.png
https://i.imgur.com/8xbc2uw.png
https://i.imgur.com/Xf51OOa.png
https://i.imgur.com/EIshIi3.png
https://i.imgur.com/Xw0TiuP.png
https://i.imgur.com/04RFAi4.png
https://i.imgur.com/7BsKbSN.png
https://i.imgur.com/G2zlHYt.png
https://i.imgur.com/ICtYQ54.png
https://i.imgur.com/Ye5e7T3.png
https://i.imgur.com/y7K63i8.png
https://i.imgur.com/oyP65JS.png
https://i.imgur.com/E06cGnX.png
https://i.imgur.com/J7Trahc.png
https://i.imgur.com/aZGEdNv.png
https://i.imgur.com/fg8gUOV.png
https://i.imgur.com/EO2MDBD.png
https://i.imgur.com/4IQOe3I.png
https://i.imgur.com/6uYGA78.png
https://i.imgur.com/E1CfT4o.png
https://i.imgur.com/o2VM5qE.png
https://i.imgur.com/ragnfbp.png
https://i.imgur.com/9ZPDs3o.png
https://i.imgur.com/SMNF4s0.png
https://i.imgur.com/0qFXuWn.png
https://i.imgur.com/IQgKp70.png
https://i.imgur.com/CNpAjhe.png
https://i.imgur.com/44o1BpV.png
https://i.imgur.com/0fcht32.png
https://i.imgur.com/xHTgCGe.png
https://i.imgur.com/oXXut5a.png
https://i.imgur.com/rYN8pBq.png
https://i.imgur.com/cWrJj6w.png
https://i.imgur.com/5GZ8gzX.png
https://i.imgur.com/SzWlfz5.png
https://i.imgur.com/Wu6THrL.png
https://i.imgur.com/xIMJ5V9.png
https://i.imgur.com/SNJ9Ix5.png
https://i.imgur.com/Ubo4SVS.png
https://i.imgur.com/ead6MaS.png
https://i.imgur.com/QWeVUSi.png""".split()

johnsonurls = [
("https://en.wikipedia.org/wiki/Johnson_solid#Pyramids",(1,2)),
("https://en.wikipedia.org/wiki/Johnson_solid#Cupolae_and_rotunda",(3,4,5,6)),
("https://en.wikipedia.org/wiki/Johnson_solid#Elongated_and_gyroelongated_pyramids",(7,8,9,10,11)),
("https://en.wikipedia.org/wiki/Johnson_solid#Bipyramids",(12,13,14,15,16,17)),
("https://en.wikipedia.org/wiki/Johnson_solid#Elongated_and_gyroelongated_cupolae_and_rotundas",(18,19,20,21,22,23,24,25)),
("https://en.wikipedia.org/wiki/Johnson_solid#Bicupolae",(26,27,28,29,30,31)),
("https://en.wikipedia.org/wiki/Johnson_solid#Cupola-rotundas_and_birotundas",(32,33,34)),
("https://en.wikipedia.org/wiki/Johnson_solid#Elongated_bicupolae",(35,36,37,38,39)),
("https://en.wikipedia.org/wiki/Johnson_solid#Elongated_cupola-rotundas_and_birotundas",(40,41,42,43)),
("https://en.wikipedia.org/wiki/Johnson_solid#Gyroelongated_bicupolae,_cupola-rotundas,_and_birotundas",(44,45,46,47,48)),
("https://en.wikipedia.org/wiki/Johnson_solid#Augmented_prisms",(49,50,51,52,53,54,55,56,57)),
("https://en.wikipedia.org/wiki/Johnson_solid#Augmented_dodecahedra",(58,59,60,61)),
("https://en.wikipedia.org/wiki/Johnson_solid#Diminished_and_augmented_diminished_icosahedra",(62,63,64)),
("https://en.wikipedia.org/wiki/Johnson_solid#Augmented_Archimedean_solids",(65,66,67,68,69,70,71)),
("https://en.wikipedia.org/wiki/Johnson_solid#Gyrate_and_diminished_rhombicosidodecahedra",(72,73,74,75,76,77,78,79,80,81,82,83)),
("https://en.wikipedia.org/wiki/Johnson_solid#Snub_antiprisms",(84,85)),
("https://en.wikipedia.org/wiki/Johnson_solid#Others",(86,87,88,89,90,91,92))
]





polyurls = {
    polyname:"https://en.wikipedia.org/wiki/%s"%(polyname.replace("_c","")) for polyname in list(plato_archi_nets)+list(prism_nets)
}

# "cube": "https://en.wikipedia.org/wiki/Cube",
# "octahedron": "https://en.wikipedia.org/wiki/Octahedron",
# "dodecahedron": "https://en.wikipedia.org/wiki/Regular_dodecahedron",
# "icosahedron": "https://en.wikipedia.org/wiki/Regular_icosahedron",
# "truncated_tetrahedron": "https://en.wikipedia.org/wiki/Truncated_tetrahedron",
# "cuboctahedron": "https://en.wikipedia.org/wiki/Cuboctahedron",
# "truncated_cube": "https://en.wikipedia.org/wiki/Truncated_cube",
# ""

for url,js in johnsonurls:
    for num in js:
        jsurl = url.replace("#","?solid=J%i\\#"%num)
        polyurls["j"+str(num)]=jsurl
        if(num in (44,45,46,47,48)):
            polyurls["j"+str(num)+"_c"]=jsurl
# print(polyurls)

def find_roller_withname(tilename,polyname):
    path = "_proofimages/roller"
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if (name.endswith(".png")) and name.startswith(polyname+"@"+tilename):
                return name
    raise FileNotFoundError(polyname+" @ "+tilename)

def find_roller_face_withname(tilename,polyname):
    # path = "_proofimages_backup/rollers_withfaces"
    path="rolled_nets"
    for dirpath, dirnames, filenames in os.walk(path):

        for name in filenames:
            if name.startswith(tilename+" @ "+polyname):

            # if (name.endswith(polyname+" rolls the "+tilename+" tiling.png")):
                return name
    raise FileNotFoundError(tilename,polyname)

def output_condensedtable(all_nets,all_tilings,rollersdata):
    values = ["SPR","PR","SQPR","QPR"]#,"HPR","br","ar","x"]
    values = ["SPR","PR"]#,"SQPR","QPR"]#,"HPR","br","ar","x"]


    sectionnames = ("Platonic Tilings (3)","Archimedean Tilings (8)","2-isogonals Tilings (20)","3-isogonal vertex homogeneous (39)")

    f=open(".latex_output/condensed_rollerstable.txt", "w")

    for i in range(len(sectionnames)):
        sectionname = sectionnames[i]
        hypertarget = ("platonic_tiling_rollers","archimedean_tiling_rollers","2isogonal_tiling_rollers","3isogonal_tiling_rollers")[i]

        tilinglist = (platonic_tilings,archimedean_tilings,uniform2,uniform3)[i]

        lines = []
        waitinglist = list()
        rollerslist = list()
        for tile in tilinglist:
            rollers = [[],[]]
            for (tilename,polyname),value in rollersdata.items():
                if tile == tilename: #n², a better way would be sorting them by the first list first
                    try:
                        url = tileurl[all_tilings.index(tilename)]
                        tileref = "\href{%s}{$%s$}"%(url,tilename)
                    except:
                        print(tilename,"has no url")
                        tileref = "$%s$"%tilename
                    hyperlink = "poly"+str(all_nets.index(polyname))+"tile"+str(all_tilings.index(tilename))
                    if(value in values):
                        sublist = rollers[values.index(value)]
                        if value == "SPR" or value == "PR":
                            sublist.append("\hyperlink{%s}{%s}"%(hyperlink,polyname.replace("_"," ")))
                        # elif(value=="SQPR" or value=="QPR"):
                        #     sublist.append(polyname.replace("_"," "))
            if(sum(len(sublist) for sublist in rollers) == 0):
                waitinglist.append(tileref)
            else:
                rollerslist.append((tileref,rollers))
        titles = ["Stable Plane Roller","Unstable Plane Roller"]
        kepttitles = list()
        keptelements = list()
        for index in range(len(values)):
            counter = any(sublist[index] for tiling,sublist in rollerslist)
            if(counter):
                kepttitles.append(titles[index])
                keptelements.append(index)

        lines.append( ("\hypertarget{%s}{%s} "%(hypertarget,sectionname), *kepttitles ))

        for tilename, data in rollerslist:
            keptrollers = [item for index,item in enumerate(data) if index in keptelements]
            lines.append((tilename, *[", ".join(category)  for category in keptrollers] ))

        f.write("\makegapedcells\n\\begin{xltabular}{\columnwidth}{|%s}"%("X|"*(len(kepttitles)+1)))
        f.write(" \n\hline\n")
        for line in lines:
            f.write(" & ".join(line)+ "\\\\\n\\hline\n")
        # rollers = [item for item in rollers if item]
        f.write("\end{xltabular}\n")
        if(waitinglist):
            f.write("No roller: "+", ".join(waitinglist)+"\n")
    print("Condensed table output")


def find_quasiroller_withname(tilename,polyname):
    path = "_proofimages/quasi_roller"
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if (name.endswith(".png")) and name.startswith(polyname+"@"+tilename):
                return name
    raise FileNotFoundError(polyname+"@"+tilename)

def output_quasirollerstable(all_nets,all_tilings,rollingresults):
    stablelines = list()
    otherlines = list()
    all_rollers = list()
    for (tilename,polyname),results in rollingresults.items():
        linedata = []
        if results and results["type"]=="quasi_roller":
            hypertarget = "poly"+str(all_nets.index(polyname))+"tile"+str(all_tilings.index(tilename))
            hyperlink = (tilename in platonic_tilings and "platonic_tiling_quasirollers") \
                        or (tilename in archimedean_tilings and "archimedean_tiling_quasirollers") \
                        or (tilename.startswith("2") and "2isogonal_tiling_quasirollers") \
                        or (tilename.startswith("3") and "3isogonal_tiling_quasirollers")\
                        or "unknown quasi tiling group"
            linedata.append("\hypertarget{%s}{"%hypertarget+"\makecell{%s \\\\ $%s$ \\\\ \hyperlink{%s}{back}}}"%(polyname.replace("_"," \\\\ "),tilename,hyperlink))
            filename = find_quasiroller_withname(tilename,polyname)
            all_rollers.append(tilename+" "+polyname)
            # print(tilename+" "+polyname)
            linedata.append("\\raisebox{-.5\height}{\includegraphics[width=100pt]{rolls/proofrolls/quasiroller/%s}}"%filename)
            if (results["stability"] and False):
                linedata.append("All tiles")
            else:
                linedata.append(
                    "\\raisebox{-.5\height}{\includegraphics[width=100pt]{rolls/proofrolls/quasirollerstability/%s}}" %
                    (polyname+"@"+tilename+" stability.png"))
            if(results["stability"]):
                stablelines.append(linedata)
            else:
                otherlines.append(linedata)
    with open(".latex_output/stable_quasirollerstable.txt","w") as f:
        f.write("""\makegapedcells 
\\begin{xltabular}{\columnwidth}{|c|%s|}
\hline
"""%("|".join("X" for x in stablelines[0])))
        f.write("Roller Pair & Structure & Stability \\\\\n\hline\n")
        f.write("\n")
        for line in stablelines:
            f.write(" & ".join(line))
            f.write("\\\\\n\hline\n")
        f.write("""\hline
\end{xltabular}\n""")

    with open(".latex_output/unstable_quasirollerstable.txt","w") as f:
        f.write("""\makegapedcells 
\\begin{xltabular}{\columnwidth}{|c|%s|}
\hline
"""%("|".join("X" for x in otherlines[0])))
        f.write("Roller Pair & Reachability & Stability \\\\\n\hline\n")
        f.write("\n")
        for line in otherlines:
            f.write(" & ".join(line))
            f.write("\\\\\n\hline\n")
        f.write("""\hline
\end{xltabular}\n""")



def output_rollerstable(all_nets,all_tilings,rollingresults, mode="complement"):
    # mode = mode=="main" + mode=="complement"*
    stablelines = list()
    otherlines = list()
    all_rollers = list()


    for (tilename,polyname),results in rollingresults.items():
        linedata = []
        if results and results["type"]=="roller":
            hypertarget = "poly"+str(all_nets.index(polyname))+"tile"+str(all_tilings.index(tilename))
            hyperlink = (tilename in platonic_tilings and "platonic_tiling_rollers") \
                        or (tilename in archimedean_tilings and "archimedean_tiling_rollers") \
                        or (tilename.startswith("2") and "2isogonal_tiling_rollers") \
                        or (tilename.startswith("3") and "3isogonal_tiling_rollers") \
                        or "unknown tiling group"
            if mode=="main":
                linedata.append("\hypertarget{%s}{"%hypertarget+"\makecell{%s \\\\ $%s$ \\\\ \hyperlink{%s}{back}}}"%(polyname,tilename,hyperlink))
            elif mode=="complement":
                polyref = "\href{%s}{%s}"%(polyurls[polyname],polyname.replace("_"," "))
                tileref = "\href{%s}{$%s$}" % (tileurl[all_tilings.index(tilename)], tilename)
                linedata.append("\hypertarget{%s}{"%hypertarget+"\makecell{%s \\\\ %s \\\\ }}"%(polyref,tileref))

            filename = find_roller_withname(tilename,polyname)
            all_rollers.append(tilename+" "+polyname)
            # print(tilename+" "+polyname)
            linedata.append("\\raisebox{-.5\height}{\includegraphics[width=100pt]{rolls/proofrolls/roller/%s}}"%filename)
            if (results["stability"]):
                if(mode=="main"):
                    linedata.append("All tiles")
            else:
                linedata.append(
                    "\\raisebox{-.5\height}{\includegraphics[width=100pt]{rolls/proofrolls/rollerstability/%s}}" %
                    (polyname+"@"+tilename+" stability.png"))
            # print(tilename,polyname)
            filename = find_roller_face_withname(tilename,polyname)
            linedata.append(
                "\\raisebox{-.5\height}{\includegraphics[width=100pt]{rolls/proofrolls/rollerswithfaces/%s}}" %filename)
            if(results["stability"]):
                stablelines.append(linedata)
            else:
                otherlines.append(linedata)
    with open(".latex_output/stable_rollerstable_%s.txt"%mode,"w") as f:
        f.write("""\makegapedcells 
\\begin{xltabular}{\columnwidth}{|c|%s|}
\hline
"""%("|".join("X" for x in stablelines[0])))
        f.write("Roller Pair & Reachability ")
        if(mode=="main"):
            f.write("& Stability")
        f.write("& Faces \\\\\n\hline\n")
        f.write("\n")
        for line in stablelines:
            f.write(" & ".join(line))
            f.write("\\\\\n\hline\n")
        f.write("""\hline
\end{xltabular}\n""")

    with open(".latex_output/unstable_rollerstable_%s.txt"%mode,"w") as f:
        f.write("""\makegapedcells 
\\begin{xltabular}{\columnwidth}{|c|%s|}
\hline
"""%("|".join("X" for x in otherlines[0])))
        f.write("Roller Pair & Reachability & Stability & Faces \\\\\n\hline\n")
        f.write("\n")
        for line in otherlines:
            f.write(" & ".join(line))
            f.write("\\\\\n\hline\n")
        f.write("""\hline
\end{xltabular}\n""")

def output_table(all_nets,all_tilings,rollersdata):
    try:os.mkdir(".latex_output")
    except:pass
    with open(".latex_output/squaretable","w")as f:
        f.write("""\\begin{center}
\\begin{tabular}""")
        f.write("\n")
        f.write("{ %s}"%("c "*(len(all_tilings)+1)))
        f.write("\n")
        f.write("\hline")
        f.write("\n")
        f.write(" X & "+" & ".join(
            "\\rotatebox{90}{$%s$}"%t for t in all_tilings
            )+"\\\\")
        f.write("\n")
        f.write("\hline\hline")
        f.write("\n")
        for net in all_nets:
            netname=net.replace("_"," ")
            f.write(netname+" & "+ " & ".join(
                rollersdata.get((tiling,net)," ") for tiling in all_tilings
                )+"\\\\")
            f.write("\n")
        f.write("""\hline
\end{tabular}
\end{center}""")
        f.write("\n")



def output_whitematrix(all_nets,all_tilings,rollersdata):
    import pygame
    tiles = list()
    for i in range(8):
        tiles.append(pygame.image.load(".latex_output/matrixcolors9000%i.png"%i))
    values = ["SPR","PR","SQPR","QPR","HPR","br","ar","x"," "]
    tilewidth = 10
    width = len(all_tilings)
    height = len(all_nets)

    image = pygame.Surface((width*tilewidth, height*tilewidth))
    image.fill((255,255,255))

    for i,net in enumerate(all_nets):
        for j,tile in enumerate(all_tilings):
            type = values.index(rollersdata[(tile,net)])
            if(type!=len(tiles)):
                image.blit(tiles[type],(j*tilewidth,i*tilewidth))
    pygame.image.save(image,".latex_output/whitematrix.png")


def output_matrix(all_nets,all_tilings,rollersdata):
    all_rollers = list()
    values = [" ","SPR","PR","SQPR","QPR","HPR","br","ar","x"]
    counters = {name:0 for name in values}
    names = ["Incompatible pairs","Stable Plane Rollers","Other Plane Rollers","Stable Quasi-Plane Rollers","Other Quasi-Plane Rollers","Hollow Plane Rollers","Band Rollers","Area rollers","x"]

    matrix2 = [[0]+[index+1 for index in range(len(values))]]
    matrix = [[0 for j in all_tilings]for i in all_nets]
    coords = list()
    for i,net in enumerate(all_nets):
        for j,tile in enumerate(all_tilings):
            data = rollersdata[tile,net]
            value = 0
            counters[data]+=1
            try:
                value = values.index(data)
            except:pass
            matrix[i][j]=value
            # if(i,j) in coords:
                # print(i,j,"already in")
            coords.append((i,j))

            #if(data=="SR" or data=="PR" or data=="SQPR" or data=="QPR"):
            if(data in values):
                all_rollers.append((tile,net))
    colors_table = [(0,0,0),(255,0,0),(128,0,0),(0,128,255),(0,64,128),(128,128,0),(0,96,0),(48,0,48),(0,0,64)]
    turn_into_image(matrix, ".latex_output/rollersdata.png",colors_table)
    turn_into_image(matrix2, ".latex_output/rollersdata_legend.png",colors_table)
    print(len(all_rollers))
    for value,counter  in counters.items():
        print(names[values.index(value)],":",counter)


def write_tilings_list():
    tilings = uniform1, uniform2, uniform3
    tiling_markers = list()
    for tiling in tilings:
        tiling_markers.append(list(tiling)[0])
        tiling_markers.append(list(tiling)[-1])
    with open(".latex_output/tilingnames.txt","w") as f:
        for tilingname in all_tilings:
            if(tilingname in tiling_markers):
                f.write(".")
            else:
                f.write("|")
            f.write(tilingname+"\n")


def write_polyherons_list():
    nets = plato_archi_nets, johnson_nets, prism_nets
    net_markers=list()
    for net in nets:
        net_markers.append(list(net)[0])
        net_markers.append(list(net)[-1])

    net_markers.append("truncated_tetrahedron")
    net_markers.append("icosahedron")

    with open(".latex_output/polynames.txt","w") as f:
        for polyname in all_nets:
            f.write(polyname)
            if(polyname in net_markers):
                f.write("."+"\n")
            else:
                f.write("|"+"\n")


# def output_usedfaces(rollersdata,all_nets,all_tilings):
#
#     GenPngScreenspaceRoller.draw_answer(filename, tilingname, polyname, visits, grid, polyhedron, p1, p2, startface, startorientation, w, h,
#                 unusedfaces)

def draw_answers_nets(rollersdata):
    print("Generating rollers nets images")
    types = "roller","hollow", "band"," area"
    for (tilingname,polyname),value in rollersdata.items():
        if(value!=None and value["type"]=="roller"):
            # print((tilingname,polyname), value.keys())
            group_max = sum(1 for group_data in value["all_data"] if group_data and group_data["type"]=="roller")
            group_counter = 0
            for group_index,group_data in enumerate(value["all_data"]):
                if group_data and group_data["type"]=="roller":
                    # print(group_data.keys())
                    # print(group_data["symmetry_vectors"])
                    # print(group_data["exploration"])
                    # print("Current group:",value["CFO_class_groups"][group_index], value["CFO_class_groups"][group_index][0])
                    # print("Classes",len(value["CFO_classes"]),value["CFO_classes"])

                    gc = ""
                    if(group_max>1):
                        group_counter+=1
                        gc = " (%s)"%str(group_counter)
                    #instead of an arbitrary, choose the least frequent face
                    try:os.mkdir("rolled_nets/")
                    except:pass
                    filename = "rolled_nets/"+tilingname + " @ " + polyname + gc + ".png"
                    tiling = uniform_tilings[tilingname]
                    net = all_nets_dict[polyname]

                    existing_faces = set(net)
                    used_faces = set(f for cfo_group in value["CFO_class_groups"][group_index] for c,f,o in value["CFO_classes"][cfo_group])
                    unused_faces = existing_faces-used_faces

                    face_counter = {facesize: sum(1 for face in net if len(net[face])==facesize) for facesize in set(len(net[face]) for face in used_faces)}
                    rarest_face = sorted((face_counter[len(net[face])], face) for face in used_faces)[0][1]

                    # c,f,o = list(value["CFO_classes"][value["CFO_class_groups"][group_index][0]])[0]
                    c,f,o =  [(c,f,o) for cfo_group in value["CFO_class_groups"][group_index] for c,f,o in value["CFO_classes"][cfo_group] if f==rarest_face][0]
                    if(tilingname.startswith("2u03") and polyname=="j87"):
                        print(face_counter)
                        print("face",rarest_face,"of size",len(net[rarest_face]))

                    area = (-200, -200, 1000, 1000)
                    area2 = (0, 0, 800, 800)
                    xx = (area[0] + area[2]) / 2
                    yy = (area[1] + area[3]) / 2
                    p1 = RollyPoint(xx, yy)
                    EDGESIZE = 50
                    p2 = RollyPoint(xx + EDGESIZE, yy)
                    precision = 7

                    mapping =  GenPngScreenspaceRoller.map_screenspace(tiling, c, area, p1, p2, precision)
                    GenPngScreenspaceRoller.draw_answer(filename, tilingname, polyname, None, mapping, net, p1, p2, f, o,area2[2], area2[3],unused_faces)
    print("Generated roller nets images")
if __name__ == "__main__":
    write_tilings_list()
    write_polyherons_list()

    with open('rollersdata.pickle', 'rb') as handle:
        rollersdata,all_tilings,all_nets = pickle.load(handle)
        #Only contains the result type string

    with open("rolling_results.pickle", "rb") as handle:
        rollingresults = pickle.load(handle)

    output_whitematrix(all_nets,all_tilings,rollersdata)

    # draw_answers_nets(rollingresults)




    # print(len(all_tilings))
    # for tiling in all_tilings:
    #     print(tiling)
    output_table(all_nets,all_tilings,rollersdata)
    output_matrix(all_nets,all_tilings,rollersdata)
    output_condensedtable(all_nets, all_tilings, rollersdata)



    output_rollerstable(all_nets,all_tilings,rollingresults)
    output_quasirollerstable(all_nets, all_tilings, rollingresults)


