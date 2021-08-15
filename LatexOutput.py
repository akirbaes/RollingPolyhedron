import os
import pickle
from tiling_dicts.platonic_tilings import platonic_tilings
from tiling_dicts.archimedean_tilings import archimedean_tilings
from tiling_dicts.isogonal_tilings import biisogonal_tilings

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
https://i.imgur.com/8xbc2uw.png""".split()


def find_roller_withname(tilename,polyname):
    path = "_proofimages/roller"
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if (name.endswith(".png")) and name.startswith(polyname+"@"+tilename):
                return name
    raise FileNotFoundError

def find_roller_face_withname(tilename,polyname):
    path = "_proofimages_backup/rollers_withfaces"
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if (name.endswith(polyname+" rolls the "+tilename+" tiling.png")):
                return name
    raise FileNotFoundError

def output_condensedtable(all_nets,all_tilings,rollersdata):
    values = ["SPR","PR","SQPR","QPR"]#,"HPR","br","ar","x"]
    values = ["SPR","PR"]#,"SQPR","QPR"]#,"HPR","br","ar","x"]

    line0= "  Tiling & \multicolumn{2}{|l|}{Plane roller}"
    # line1= "  & Stable & Unstable & Stable & Unstable"
    line1= "  & Stable & Unstable "

    lines = []

    for i in range(3):
        sectionname = ("Platonics","Archimedeans","2-isogonals")[i]
        hypertarget = ("platonic_tiling_rollers","platonic_tiling_rollers","2isogonal_tiling_rollers")[i]
        lines.append("  \multicolumn{3}{|l|}{\hypertarget{%s}{%s}} "%(hypertarget,sectionname))

        tilinglist = (platonic_tilings,archimedean_tilings,biisogonal_tilings)[i]

        waitinglist = list()

        for tile in tilinglist:
            rollers = [[],[]]
            for (tilename,polyname),value in rollersdata.items():
                if tile == tilename: #n², a better way would be sorting them by the first list first
                    url = tileurl[all_tilings.index(tilename)]
                    tileref = "\href{%s}{$%s$}"%(url,tilename)

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
                lines.append(tileref+" & "+" & ".join(", ".join(elem) for elem in rollers))

        if(waitinglist):
            lines.append(" No roller & \multicolumn{2}{|l|}{%s} "%", ".join(waitinglist))

    with open(".latex_output/condensed_rollerstable.txt", "w") as f:
        f.write("\makegapedcells\n\\begin{xltabular}{\columnwidth}{|X|X|X|}")
        f.write(" \n\hline\n")
        f.write(line0)
        f.write("\\\\ \n")
        f.write(line1)
        f.write("\\\\ \n\hline\n")
        for line in lines:
            f.write(line)
            f.write("\\\\ \n\hline\n")
        f.write("\end{xltabular}\n")
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
            hyperlink = (tilename in platonic_tilings and "platonic_tiling_quasirollers") or (tilename in archimedean_tilings and "archimedean_tiling_quasirollers") or (tilename in biisogonal_tilings and "2isogonal_tiling_quasirollers") or "unknown quasi tiling group"
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
        f.write("Pair & Roll & Stability \\\\\n\hline\n")
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
        f.write("Pair & Roll & Stability \\\\\n\hline\n")
        f.write("\n")
        for line in otherlines:
            f.write(" & ".join(line))
            f.write("\\\\\n\hline\n")
        f.write("""\hline
\end{xltabular}\n""")



def output_rollerstable(all_nets,all_tilings,rollingresults):
    stablelines = list()
    otherlines = list()
    all_rollers = list()
    for (tilename,polyname),results in rollingresults.items():
        linedata = []
        if results and results["type"]=="roller":
            hypertarget = "poly"+str(all_nets.index(polyname))+"tile"+str(all_tilings.index(tilename))
            hyperlink = (tilename in platonic_tilings and "platonic_tiling_rollers") or (tilename in archimedean_tilings and "archimedean_tiling_rollers") or (tilename in biisogonal_tilings and "2isogonal_tiling_rollers") or "unknown tiling group"
            linedata.append("\hypertarget{%s}{"%hypertarget+"\makecell{%s \\\\ $%s$ \\\\ \hyperlink{%s}{back}}}"%(polyname.replace("_"," \\\\ "),tilename,hyperlink))
            filename = find_roller_withname(tilename,polyname)
            all_rollers.append(tilename+" "+polyname)
            # print(tilename+" "+polyname)
            linedata.append("\\raisebox{-.5\height}{\includegraphics[width=100pt]{rolls/proofrolls/roller/%s}}"%filename)
            if (results["stability"]):
                linedata.append("All tiles")
            else:
                linedata.append(
                    "\\raisebox{-.5\height}{\includegraphics[width=100pt]{rolls/proofrolls/rollerstability/%s}}" %
                    (polyname+"@"+tilename+" stability.png"))
            filename = find_roller_face_withname(tilename,polyname)
            linedata.append(
                "\\raisebox{-.5\height}{\includegraphics[width=100pt]{rolls/proofrolls/rollerswithfaces/%s}}" %filename)
            if(results["stability"]):
                stablelines.append(linedata)
            else:
                otherlines.append(linedata)
    with open(".latex_output/stable_rollerstable.txt","w") as f:
        f.write("""\makegapedcells 
\\begin{xltabular}{\columnwidth}{|c|%s|}
\hline
"""%("|".join("X" for x in stablelines[0])))
        f.write("Pair & Roll & Stability & Faces \\\\\n\hline\n")
        f.write("\n")
        for line in stablelines:
            f.write(" & ".join(line))
            f.write("\\\\\n\hline\n")
        f.write("""\hline
\end{xltabular}\n""")

    with open(".latex_output/unstable_rollerstable.txt","w") as f:
        f.write("""\makegapedcells 
\\begin{xltabular}{\columnwidth}{|c|%s|}
\hline
"""%("|".join("X" for x in otherlines[0])))
        f.write("Pair & Roll & Stability & Faces \\\\\n\hline\n")
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

if __name__ == "__main__":

    with open('rollersdata.pickle', 'rb') as handle:
        rollersdata,all_tilings,all_nets = pickle.load(handle)
        # for tiling in all_tilings:
        #     print(tiling)
        # for net in all_nets:
        #     print(net)
        # print(rollersdata)
    output_table(all_nets,all_tilings,rollersdata)
    output_matrix(all_nets,all_tilings,rollersdata)
    output_condensedtable(all_nets, all_tilings, rollersdata)
    with open("rolling_results.pickle", "rb") as handle:
        rollingresults = pickle.load(handle)
    output_rollerstable(all_nets,all_tilings,rollingresults)
    output_quasirollerstable(all_nets, all_tilings, rollingresults)
