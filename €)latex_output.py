# -*- coding: utf-8 -*-
import os
import pickle

import GenPngScreenspaceRoller
from RollyPoint import RollyPoint
from tiling_dicts._1uniform_tilings import uniform1
from tiling_dicts._2uniform_tilings import uniform2
from tiling_dicts._3uniform_tilings import uniform3
from tiling_dicts._4uniform_tilings import uniform4
from tiling_dicts.platonic_tilings import platonic_tilings
from tiling_dicts.archimedean_tilings import archimedean_tilings
# from tiling_dicts.isogonal_tilings import biisogonal_tilings
# from tiling_dicts.triisogonal_vertex_homogeneous import triisogonal_vertex_homogeneous
# all_tilings = {**platonic_tilings, **archimedean_tilings, **biisogonal_tilings, **triisogonal_vertex_homogeneous}
from tiling_dicts.combine_uniform_tilings import uniform_tilings

all_tilings  = {**uniform_tilings}
print(len(all_tilings))
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.johnson_nets import johnson_nets
from poly_dicts.prism_nets import prism_nets
all_nets = {**plato_archi_nets, **johnson_nets, **prism_nets}
all_nets_dict = {**plato_archi_nets, **johnson_nets, **prism_nets}

from DrawingFunctions import turn_into_image

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
    polyname:"https://en.wikipedia.org/wiki/%s"%(polyname[:-2] if polyname.endswith("_c") else polyname) for polyname in list(plato_archi_nets)+list(prism_nets)
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

def find_tiling_url(tilename):
    number = str(list(all_tilings).index(tilename)+1)+" "
    path = "saved_results\Imgur Album kuniform tessellations tile symmetries and periodic translation area"
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if name.startswith(number):

                url = "https://i.imgur.com/%s"%(name.split(" ")[-1])
                return url

def find_roller_url(planerollerid):
    path= "saved_results\Imgur Album Plane rollers starting position hint"
    number = str(planerollerid+1)+" "
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if name.startswith(number):

                url = "https://i.imgur.com/%s"%(name.split(" ")[-1])
                return url

def roller_id(til,poly,rollersdata):
    return list(rollersdata).index((til,poly))

def find_roller_face_withname(tilename,polyname):
    # path = "_proofimages_backup/rollers_withfaces"
    path="rolled_nets"
    for dirpath, dirnames, filenames in os.walk(path):

        for name in filenames:
            if (tilename+" @ "+polyname) in name:

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
                        url = find_tiling_url(tilename)
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
                        or (tilename.startswith("4") and "4isogonal_tiling_rollers") \
                        or "unknown tiling group"
            if mode=="main":
                linedata.append("\hypertarget{%s}{"%hypertarget+"\makecell{%s \\\\ $%s$ \\\\ \hyperlink{%s}{back}}}"%(polyname,tilename,hyperlink))
            elif mode=="complement":
                polyref = "\href{%s}{%s}"%(polyurls[polyname],polyname.replace("_"," "))
                tileref = "\href{%s}{$%s$}" % (find_tiling_url(tilename), tilename)
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
            fileurl = find_roller_url(roller_id(tilename,polyname,rollingresults))
            filename = find_roller_face_withname(tilename,polyname)
            linedata.append(
                "\\raisebox{-.5\height}{\includegraphics[width=100pt]{rolls/proofrolls/rollerswithfaces/%s}}" %(filename))
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

def output_htmlmatrix(all_nets, all_tilings, rollersdata):
    print("Output htmlmatrix of",len(all_nets),"*",len(all_tilings))
    characters = "  ◙◘#↔×• "#"█■▒▩▩↔x*?" #━ "█■▒▩▩↔x*❌"◙○◘•
    """.SPR {background-color: red; color: red;}
.PR {background-color: brown; color: brown;}
.SQPR {background-color: DarkBlue; color: #0080FF;}
.QPR {background-color: DarkBlue; color: blue;}
.HPR {background-color: DarkBlue; color: BlueViolet;}
.br {background-color: Green; color: GhostWhite;}
.ar { color: Green;}
.x {color: Green;}"""
    output = """<!DOCTYPE html>
<html>
<head>
<style>
tr.tilingnames td {writing-mode: vertical-rl;vertical-align: baseline;transform: rotate(-180deg);}
body {
  font-family: 'Courier New', monospace;
  font-size: 8px;
  horizontal-align: right;
}
img { display: block; }
tr:hover { background: yellow; }
tr.tilingnames:hover {background: white;  }
td, tr, img  { padding: 0px; margin: 0px; border: none; }
table { border-collapse: collapse; }
</style>
</head>
"""
    #border-collapse:collapse;

    values = ["SPR","PR","SQPR","QPR","HPR","br","ar","x","_"]
    descriptions = ["Stable Plane Roller", "Other Plane Roller", "Stable Quasi-Plane Roller", "Other Quasi-Plane Roller", "Hollow-Plane Roller", "Band Roller", "Area Roller", "Area Roller (cannot escape starting tile)", "Incompatible"]

    output += '<table >\n'
    for i in range(len(values)):
        output+='  <tr><td><img src=%s.png></td><td>%s<td></tr>\n'%(values[i],descriptions[i])
    output += '</table >\n'


    output += '<table >\n  <tr class="tilingnames">\n    <td/>\n'
    for tiling in all_tilings:
        shortile = tiling.split(" ")[0]
        output+='    <td><a href="t/%s.png">%s</a></td>\n'%(shortile,shortile) #?page=
    output+= '</tr>'

    for net in all_nets:
        shortnet = net
        # shortnet = shortnet.replace("triangular_","▲-")
        # shortnet = shortnet.replace("square_","■-")
        # shortnet = shortnet.replace("pentagonal_","⬟-")
        # shortnet = shortnet.replace("hexagonal_","⬣-")
        # shortnet = shortnet.replace("octagonal_","⯃-")
        # shortnet = shortnet.replace("dodecagonal_","12-")
        # shortnet = shortnet.replace("decagonal_","10-")
        shortnet = shortnet.replace("triangular_","3-")
        shortnet = shortnet.replace("square_","4-")
        shortnet = shortnet.replace("pentagonal_","5-")
        shortnet = shortnet.replace("hexagonal_","6-")
        shortnet = shortnet.replace("octagonal_","8-")
        shortnet = shortnet.replace("dodecagonal_","12-")
        shortnet = shortnet.replace("decagonal_","10-")
        output+= '  <tr>\n    <td><a href="p/%s.png">%s</a></td>\n'%(net,shortnet)

        for tiling in all_tilings:
            data = rollersdata[(tiling,net)]
            # outchar = characters[values.index(data)]

            shortile = tiling.split(" ")[0]

            image = "<img src=%s.png>"%(data.replace(" ","_"))
            outchar = '<a href="r.php?p=%s&amp;t=%s&amp;r=%s">%s</a></td>\n' % (net,shortile, data.replace(" ","_"), image)  # ?page=
            # output+='    <td class="%s">%s</td>'%(data,outchar)
            output+='    <td>%s</td>'%(outchar)

        output+= '</tr>'
    output+="\n</table>\n</html>"

    with open(".html_output/index.html","w", encoding="utf-8") as f:
        f.write(output)



def output_rollingpairs(all_nets,all_tilings,rollersdata):
    all_plane_roller_pairs = []
    for (tile,net),value in rollersdata.items():
        if(value in ("SPR","SQPR")):
            all_plane_roller_pairs.append((net,tile))
    with open(".latex_output/stable_pairs.py","w") as f:
        f.write(str(all_plane_roller_pairs))


def output_counters_table(all_nets,all_tilings,rollersdata):
    print("Counts table output")
    #{'ar', 'HPR', 'br', 'QPR', 'PR', 'SQPR', 'x', ' ', 'SPR'}
    f = open(".latex_output/rollers_counters_table.tex","w")
    # f.write("Number of rollers of the given type found on all considered tessellations:\n\n")
    f.write("""\\begin{center}
\\begin{longtable}{ | c | c | c | c | c |}
\hline \n""")
#\caption{Number of rollers of the given type found on all considered tessellations.\label{counters}}\n""")

    titles = "Polyhedron","Plane roller","Hollow plane","Band","Area$>$1"

    f.write(" & ".join(titles) + " \\\\ \n\hline\hline\n")
    for net in all_nets:
        counts = [0,0,0,0,0]
        index = {"PR":0,"SPR":0,"SQPR":1,"QPR":1,"HPR":1,"br":2,"ar":3,"x":4," ":4}
        for tile in all_tilings:
            counts[index[rollersdata[(tile,net)]]]+=1
        counts.pop(-1)
        netter = net.replace("_"," ")
        neturl = "\href{%s}{%s}"%(polyurls[net],netter+"hiral" if netter.endswith(" c") else netter)
        #neturl = net.replace("_"," ")
        if(counts[0]):
            f.write(" & ".join([neturl]+[str(c) for c in counts])+" \\\\ \hline ")

    f.write("""\n\end{longtable}
\end{center}""")
    f.close()

    uniqueresults = [[],[],[],[],[]]
    duperesults = [[],[],[],[],[]]
    index = {"PR":0,"SPR":0,"SQPR":1,"QPR":1,"HPR":1,"br":2,"ar":3,"x":4," ":4}
    f = open(".latex_output/supercondensed_results.tex","w")

    for net in all_nets:
        for tile in all_tilings:

            # netter = net.replace("_", " ")
            # neturl = "\href{%s}{%s}" % (polyurls[net], netter + "hiral" if netter.endswith(" c") else netter)
            if(net not in uniqueresults[index[rollersdata[(tile,net)]]]):
                uniqueresults[index[rollersdata[(tile, net)]]].append(net)
            duperesults[index[rollersdata[(tile, net)]]].append(net)
    f.write("\\begin{table}\n")
    f.write("\\begin{tabular}{|p{\linewidth}|} \n")
    # f.write("\hline \n")

    titles = "Plane","Hollow plane","Band","Area$>$1"
    commands = "\planeroller", "\hollowplaneroller", "\\bandroller", "\\arearoller"
    for i in range(len(titles)-1):
        f.write(" \hline ")
        f.write(commands[i]+" Polyhedrons that Roll on a %s on a given tessellation: (%i results for %i pairings)\\\\ \hline "%(titles[i],len(uniqueresults[i]), len(duperesults[i])))
        f.write(" - ".join([
            "\href{%s}{%s}" % (polyurls[net], (net+"hiral" if net.endswith("_c") else net).replace("_","~"))
            + ("~(x%s)"%duperesults[i].count(net) if duperesults[i].count(net)>1 else "") for net in uniqueresults[i]
        ]))
        f.write("\\\\ \hline ")

    f.write("\n\\end{tabular} \n")
    f.write("\\caption{\label{tab:supercondensed_results}Condensed table showing Polyhedron to Roller classification with impacted tessellations count.}\n")
    f.write("\\end{table}")
    f.close()

def output_whitematrix(all_nets,all_tilings,rollersdata):
    print("Output whitematrix",len(all_nets),"X",len(all_tilings))
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

def write_rollable_polyhedron_list(all_nets,all_tilings,rollersdata):

    all_poly = set(all_nets)
    all_rollables = set()
    rollable_pairs = dict()
    unrolled  =list()
    for i,net in enumerate(all_nets):
        all_poly.add(net)
        for j,tile in enumerate(all_tilings):
            if rollersdata[(tile,net)] in ("SPR","PR"):
                all_rollables.add((net))
                rollable_pairs[net]=rollable_pairs.get(net,[])+[tile]
        if net not in rollable_pairs:
            unrolled.append(net)
    # unrolled = all_poly-all_rollables
    with open(".latex_output/polyhedron_rollerslist.txt","w") as f:
        f.write("# Polyhedron found in plane roller: %i\n"%len(all_rollables))
        for poly,tilings in rollable_pairs.items():
            # for i,tile in enumerate(tilings):
                # if(" " in tile):
                #     tilings[i]=tile[:tile.index(" ")]
            f.write("%s: %s\n"%(poly,", ".join(tilings)))
        f.write("# Polyhedron without plane roller found: %i\n"%len(unrolled))
        for poly in unrolled:
            f.write(poly+"\n")
        f.write("Total poly: %i\n"%len(all_poly))

import pprint
import json

if __name__ == "__main__":
    write_tilings_list()
    write_polyherons_list()

    with open('rollersdata.pickle', 'rb') as handle:
        rollersdata,all_tilings,all_nets = pickle.load(handle)
        #Only contains the result type string

    with open("rolling_results.pickle", "rb") as handle:
        rollingresults = pickle.load(handle)

    print(len(all_nets),"polyhedron nets")
    print(len(all_tilings), "tessellation tilings")

    # new_object = dict()
    # print(rollingresults)
    # json_object=pprint.pformat(rollingresults,indent=2)
    # print(json_object)
    # json_object = json.dumps(rollingresults, indent=4)
    # with open("rolling_results.json", "w") as f:
    #     f.write(json_object)
    # exit()

    with open(".html_output/polyurls.txt", "w", encoding="utf-8") as f:
        f.write("$polyurls = [\n")
        for poly, url in polyurls.items():
            f.write('    "%s" => "%s",\n' % (poly, url))
        f.write("];")

    output_counters_table(all_nets,all_tilings,rollersdata)
    output_whitematrix(all_nets,all_tilings,rollersdata)
    output_htmlmatrix(all_nets,all_tilings,rollersdata)
    output_rollingpairs(all_nets,all_tilings,rollersdata)
    write_rollable_polyhedron_list(all_nets,all_tilings,rollersdata)


    # print(len(all_tilings))
    # for tiling in all_tilings:
    #     print(tiling)
    output_table(all_nets,all_tilings,rollersdata)
    output_matrix(all_nets,all_tilings,rollersdata)
    output_condensedtable(all_nets, all_tilings, rollersdata)



    output_rollerstable(all_nets,all_tilings,rollingresults)
    output_quasirollerstable(all_nets, all_tilings, rollingresults)

    import json
    # print(rollingresults)
    # print(json.dumps(rollersdata,indent=4))
    with open(".latex_output/rollersdata.py","w") as f:
        f.write("rollersdata = \\\n")
        f.write(pprint.pformat(rollersdata,indent=1,sort_dicts=False))
        # f.write(json.dumps(rollersdata,indent=4))
    with open(".latex_output/rollingresults.py","w") as f:
        f.write("rollingresults = \\\n")
        f.write(pprint.pformat(rollingresults,indent=1,sort_dicts=False))
        # f.write(json.dumps(rollingresults,indent=4))

