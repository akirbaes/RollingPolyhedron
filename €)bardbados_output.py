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
from tiling_dicts.uniform_tilings import uniform_tilings

all_tilings  = {**uniform_tilings}
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.johnson_nets import johnson_nets
from poly_dicts.prism_nets import prism_nets
all_nets = {**plato_archi_nets, **johnson_nets, **prism_nets}

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
    polyname:"https://en.wikipedia.org/wiki/%s"%(polyname.replace("_c","")) for polyname in list(plato_archi_nets)+list(prism_nets)
}

for url,js in johnsonurls:
    for num in js:
        jsurl = url.replace("#","?solid=J%i\\#"%num)
        polyurls["j"+str(num)]=jsurl
        if(num in (44,45,46,47,48)):
            polyurls["j"+str(num)+"_c"]=jsurl
# print(polyurls)

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

def output_barbadostable(rollersdata, condensed = False):
    try:os.mkdir(".bardbados_output")
    except:pass
    unitilings = uniform1,uniform2,uniform3,uniform4
    sectionsizes = list()
    for type in "1234":
        sectionsizes.append(len([1 for tiling,polyhedron in rollersdata if tiling.startswith(type)]))

    f=open(".bardbados_output/"+("condensed_"*condensed)+"rollerstable.txt", "w")

    if(condensed):
            f.write("<details><summary>%s</summary>\n\n"%"Condensed rollers table")
            f.write("Tiling|Plane Rollers\n")
            f.write("|-|-|\n")

    current_section = 0
    for tiling in all_tilings:
        if(tiling[0]!=str(current_section)):
            if(condensed):
                sectionname = tiling[0]+"-uniform (%i tilings, %i rolling pairs)"%(len(unitilings[current_section]),sectionsizes[current_section])
                current_section+=1
                f.write("%s\n"%sectionname)
            else:
                if(current_section!=0):
                    #end section
                    f.write("\n</details>\n\n")
                #start section
                sectionname = tiling[0]+"-uniform (%i tilings, %i rolling pairs)"%(len(unitilings[current_section]),sectionsizes[current_section])
                current_section+=1
                f.write("<details><summary>%s</summary>\n\n"%sectionname)
                f.write("Tiling|Plane Rollers\n")
                f.write("|-|-|\n")
        if(condensed):
            f.write("[%s](%s)"%(tiling,find_tiling_url(tiling)))
        else:
            f.write("%s\n![image](%s)"%(tiling,find_tiling_url(tiling)))
        f.write("|")
        if(condensed):
            rollers_for_this_tiling = ["[%s](%s)"%(poly,find_roller_url(roller_id(t,poly,rollersdata))) for t,poly in rollersdata if t==tiling]
        else:
            rollers_for_this_tiling = ["%s![image](%s)"%(poly,find_roller_url(roller_id(t,poly,rollersdata))) for t,poly in rollersdata if t==tiling]
        f.write(", ".join(rollers_for_this_tiling) or "No regular-faced convex polyhedron")
        f.write("\n")
    # if(condensed):
    f.write("\n</details>\n\n")
    f.close()

    print("Condensed"*condensed,"Table output")



def write_tilings_list():
    tilings = uniform1, uniform2, uniform3, uniform4
    tiling_markers = list()
    for tiling in tilings:
        tiling_markers.append(list(tiling)[0])
        tiling_markers.append(list(tiling)[-1])
    with open(".bardbados_output/tilingnames.txt","w") as f:
        for index,uni in enumerate(tilings):
            f.write("* %i-uniform (%i) \n\n"%(index+1,len(uni)))


def write_polyherons_list():
    try:os.mkdir(".bardbados_output")
    except:pass
    with open(".bardbados_output/polynames.txt","w") as f:
        chirals = len([1 for poly in plato_archi_nets if poly.endswith("_c")])
        f.write("All %i regular-faced convex polyhedron of interest"%(len(all_nets)))
        f.write("\n\n")
        f.write("### Platonics + Archimedeans: %i + %i chirals variations = %i"%(len(plato_archi_nets)-chirals,chirals,len(plato_archi_nets)))
        f.write("\n\n")
        f.write(", ".join(polyname for polyname in plato_archi_nets))
        f.write("\n\n")
        f.write("### Prisms and Antiprisms: %i"%len(prism_nets))
        f.write("\n\n")
        f.write(", ".join(polyname for polyname in prism_nets))
        f.write("\n\n")
        chirals = len([1 for poly in johnson_nets if poly.endswith("_c")])
        f.write("### Johnson solids: 92/92 + %i chiral variations = %i"%(chirals,len(johnson_nets)))
        f.write("\n\n")
        f.write(", ".join(polyname for polyname in johnson_nets))


# def output_usedfaces(rollersdata,all_nets,all_tilings):
#
#     GenPngScreenspaceRoller.draw_answer(filename, tilingname, polyname, visits, grid, polyhedron, p1, p2, startface, startorientation, w, h,
#                 unusedfaces)

if __name__ == "__main__":
    write_tilings_list()
    write_polyherons_list()

    with open('rollersdata.pickle', 'rb') as handle:
        rollersdata,all_tilings,all_nets = pickle.load(handle)
        #Only contains the result type string

    with open("rolling_results.pickle", "rb") as handle:
        rollingresults = pickle.load(handle)

    all_rollers = [(til,poly) for til,poly in rollersdata if rollersdata[(til,poly)]=="PR" or rollersdata[(til,poly)]=="SPR"]
    output_barbadostable(all_rollers,condensed=True)
    output_barbadostable(all_rollers,condensed=False)


