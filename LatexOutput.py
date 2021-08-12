import os
import pickle

from DrawingFunctions import turn_into_image


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
            if(i,j) in coords:
                print(i,j,"already in")
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

