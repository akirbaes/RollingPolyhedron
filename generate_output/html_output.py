# -*- coding: utf-8 -*-
import sys
sys.path.append("..")
sys.path.append("..\\..")
import os
import pickle

from _resources.uniform_tiling_supertiles import uniform_tilings as all_tilings
from _resources.regular_faced_polyhedron_nets import all_nets

from _libs.DrawingFunctions import turn_into_image

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

def outputfolder(*parts):
    # print(parts)
    name = os.sep.join(parts) + os.sep
    os.makedirs(name, exist_ok=True)
    return name



polyurls = {
    polyname:"https://en.wikipedia.org/wiki/%s"%(polyname[:-2] if polyname.endswith("_c") else polyname) for polyname in all_nets
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
    path = "../_proofimages/roller"
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if (name.endswith(".png")) and name.startswith(polyname+"@"+tilename):
                return name
    raise FileNotFoundError(polyname+" @ "+tilename)

def find_tiling_url(tilename):
    number = str(list(all_tilings).index(tilename)+1)+" "
    path = "../saved_results/Imgur Album kuniform tessellations tile symmetries and periodic translation area"
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if name.startswith(number):

                url = "https://i.imgur.com/%s"%(name.split(" ")[-1])
                return url

def find_roller_url(planerollerid):
    path= "../saved_results/Imgur Album Plane rollers starting position hint"
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
    path= "../rolled_nets"
    for dirpath, dirnames, filenames in os.walk(path):

        for name in filenames:
            if (tilename+" @ "+polyname) in name:

            # if (name.endswith(polyname+" rolls the "+tilename+" tiling.png")):
                return name
    raise FileNotFoundError(tilename,polyname)

def find_quasiroller_withname(tilename,polyname):
    path = "../_proofimages/quasi_roller"
    for dirpath, dirnames, filenames in os.walk(path):
        for name in filenames:
            if (name.endswith(".png")) and name.startswith(polyname+"@"+tilename):
                return name
    raise FileNotFoundError(polyname+"@"+tilename)

def output_polywikilink():
    links = [polyurls[poly].replace("https://en.wikipedia.org/wiki/","") for poly in all_nets]
    for i,poly in enumerate(all_nets):
        if(links[i]==poly):
            links[i]=0
    with open("wikishort.txt","w") as out:
        out.write(str(links))
        

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

    #Legend
    output += '<table >\n'
    for i in range(len(values)):
        output+='  <tr><td><img src=%s.png></td><td>%s<td></tr>\n'%(values[i],descriptions[i])
    output += '</table >\n'

    #Tilings head
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

            image = "<img src=./%s.png>"%(data.replace(" ","_"))
            outchar = '<a class="tooltip" href="r.php?p=%s&amp;t=%s&amp;r=%s">%s</a></td>\n' % (net,shortile, data.replace(" ","_"), image)  # ?page=
            # output+='    <td class="%s">%s</td>'%(data,outchar)
            output+='    <td>%s</td>'%(outchar)

        output+= '</tr>'
    output+="\n</table>\n</html>"

    htmloutput = outputfolder("html_output")+"index.html"
    with open(htmloutput, "w", encoding="utf-8") as f:
        f.write(output)



def output_rollingpairs(all_nets,all_tilings,rollersdata):
    all_plane_roller_pairs = []
    for (tile,net),value in rollersdata.items():
        if(value in ("SPR","SQPR")):
            all_plane_roller_pairs.append((net,tile))
    with open("../.latex_output/stable_pairs.py", "w") as f:
        f.write(str(all_plane_roller_pairs))


def write_tilings_list():
    s="[%s]"%(",".join('"%s"'%name for name in all_tilings))
    with open(outputfolder("html_output")+"tilingnames.txt","w") as f:
        f.write(s)
    return s

def write_polyherons_list():
    s="[%s]"%(",".join('"%s"'%name for name in all_nets))
    with open(outputfolder("html_output")+"polynames.txt","w") as f:
        f.write(s)
    return s

def write_result_type_list(rollingresults):
    imagenames = ["SPR","PR","SQPR","QPR","HPR","br","ar","x"," "]
    s="".join(str(imagenames.index(rollingresults[tiling,net])) for net in all_nets for tiling in all_tilings)
    with open(outputfolder("html_output")+"combi_ids.txt","w") as f:
        f.write(s)
    return s


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
    [TODO]
    with open("../.latex_output/polyhedron_rollerslist.txt", "w") as f:
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

if __name__ == "__main__":
    write_tilings_list()
    write_polyherons_list()

    with open('../_results/rollersdata.pickle', 'rb') as handle:
        rollersdata,all_tilings,all_nets = pickle.load(handle)
        #Only contains the result type string

    with open("../_results/rolling_results.pickle", "rb") as handle:
        rollingresults = pickle.load(handle)

    write_result_type_list(rollersdata)
    # print(len(all_nets),"polyhedron nets")
    # print(len(all_tilings), "tessellation tilings")

    # # # # # new_object = dict()
    print(rollersdata)
    # # # # # json_object=pprint.pformat(rollingresults,indent=2)
    # # # # # print(json_object)
    # # # # # json_object = json.dumps(rollingresults, indent=4)
    # # # # # with open("rolling_results.json", "w") as f:
    # # # # #     f.write(json_object)
    # # # # # exit()
    # # # # # folder = outputfolder("htmlpage")+"polymatrix.html"
    # with open("polyurls.txt", "w", encoding="utf-8") as f:
        # f.write("$polyurls = [\n")
        # for poly, url in polyurls.items():
            # f.write('    "%s" => "%s",\n' % (poly, url))
        # f.write("];")

    output_htmlmatrix(all_nets,all_tilings,rollersdata)
    output_polywikilink()
    
    
    
    # output_rollingpairs(all_nets,all_tilings,rollersdata)
    # write_rollable_polyhedron_list(all_nets,all_tilings,rollersdata)

