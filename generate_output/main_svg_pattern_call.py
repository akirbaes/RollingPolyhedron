import pickle
import pprint
import sys

import svgwrite

from _libs import CFOClassGenerator
from _libs.FileManagementShortcuts import outputfolder
from _libs.GenPngScreenspaceRoller import draw_polynet, draw_answer, convertToTuples
from _libs.GeometryFunctions import xgon
from _libs.RollyPoint import RollyPoint
from _libs.SupertileCoordinatesGenerator import generate_supertile_coordinate_helpers
from _libs.RollingProofImageGen import generate_image

sys.path.append("../..")
from _resources.regular_faced_polyhedron_nets import all_nets
from _resources.uniform_tiling_supertiles import uniform_tilings as all_tilings


with open("../_results/rolling_results.pickle", "rb") as handle:
    rollingresults = pickle.load(handle)

pprint.pprint(list(rollingresults)[0])
pprint.pprint(rollingresults[list(rollingresults)[0]])

cfo = (int,int,int)
xy = x,y = int,int
roll_class = int
roll_group = int
Union = "Union"

rollingres = {
    ("tiling", "polyhedron"):
        {
            "CFO_class_groups (connected classes)" : [{int}],
            "CFO_classes (equivalent states)": [{cfo}],
            "all_data (per connected group)":
                [ #per connected group
                    {
                        'exploration':{
                            (x,y):{roll_class}
                        },
                        "symmetry_vectors (0 to 2)":[xy],
                        "type":str
                    }
                ],
            "class_to_supertile_coordinates":{
                roll_class:{(roll_group,xy)}
            },
            "polyhedron":str,
            "stability":bool,
            "tiling":str,
            "type":str
        }
}

pprint.pprint(rollingres)

def determine_stable_spots(all_data):
    min_size_area = \
        min((len(res["exploration"]), index) for index, res in enumerate(all_data) if
            "exploration" in res.keys())[
            1]
    fill_area = {pos: [0 for cell in tiling] for pos in all_data[min_size_area]["exploration"]}
    maxfo = [sum(len(n) for n in net.values() if len(n) == len(neigh)) for tile, neigh in
             sorted(tiling.items())]
    cell_stability = [0 for cell in tiling]
    for index, group in enumerate(groups):
        for clas in group:
            for c, f, o in classes[clas]:
                cell_stability[c] += all_data[index] in ("quasi_roller","roller")
    for index, result in enumerate(all_data):
        if "exploration" in result.keys():
            for pos, group in result["exploration"].items():
                for clas in group:
                    for c, f, o in classes[clas]:
                        try:
                            fill_area[pos][c] += all_data[index] in ("quasi_roller","roller")
                        except KeyError:
                            pass

    stable_spots = {pos: [counter == maxfo[cell] for cell, counter in enumerate(celldata)] for pos, celldata in
                    fill_area.items()}
    stable_spots = {
        pos: [cell_stability[cell] == maxfo[cell] and maxfo[cell] != 0 for cell in range(len(tiling))] for pos
        in fill_area}
#def generate_image(tiling,polyhedron,tilingname,polyname,classes,group,groups,hexborders,symmetries,explored,type,stable_spots = []):
#def draw_polynet(surf, surface2, polyhedron, startface, startorientation, p1, p2, tilingname, polyname, unusedfaces=None, svg=None):
#def draw_answer(filename, tilingname, polyname, visits, grid, polyhedron, p1, p2, startface, startorientation, w, h, unusedfaces, svg=False):
if __name__ == "__main__":
    for (tilingname,polyname),data in rollingresults.items():
        tiling = all_tilings[tilingname]
        net = all_nets[polyname]
        if not data: continue
        if data.get("CFO_class_groups",None)==None: continue
        borders = generate_supertile_coordinate_helpers(tiling, tilingname)
        classes, transformations, groups = CFOClassGenerator.generate_CFO_classes(tiling, net, polyname, tilingname, None)

        connected_classes = data["CFO_class_groups"]
        equivalent_states = data["CFO_classes"]

        adjacent_classes = data["class_to_supertile_coordinates"]

        stable_spots = determine_stable_spots(data["all_data"])
        # input(classes)
        for group_index,connected_data in enumerate(data["all_data"]):
            if not connected_data: continue
            type = connected_data["type"]
            if type not in ("quasi_roller","roller"): continue
            explored_tiles = connected_data["exploration"]
            symmetry_vectors = connected_data["symmetry_vectors"]


            generate_image(tiling, net, tilingname, polyname, classes, groups[group_index], groups, borders, symmetry_vectors,
                       explored_tiles, type,group_index, stable_spots)
            c,f,o = list(classes[groups[group_index][0]])[0]

            area = (-200, -200, 1000, 1000)
            area2 = (0, 0, 800, 800)
            xx = (area[0] + area[2]) / 2
            yy = (area[1] + area[3]) / 2
            p1 = RollyPoint(xx, yy)
            EDGESIZE = 50
            p2 = RollyPoint(xx + EDGESIZE, yy)
            precision = 7

            faces = set(net.keys())
            used_faces=set()
            for explored_classes in explored_tiles.values():
                for eclassid in explored_classes:
                    for c,f,o in classes[eclassid]:
                        used_faces.add(f)
            unused_faces = faces-used_faces

            tilingshortname = tilingname.split()[0]
            filename = outputfolder("..","_results","svgnet")+polyname+"@"+tilingshortname

            dwg = svgwrite.Drawing(filename + '.svg', profile='tiny', height=800, width=800)

            face = xgon(len(net[f]), p1, p2)
            dwg.add(dwg.polygon(convertToTuples(face), fill="blue"))

            draw_polynet(None, None, net,f,o,p1,p2,tilingname,polyname,unusedfaces=unused_faces,svg=dwg)
            # draw_answer(filename, tilingname, polyname, visits, grid, polyhedron, p1, p2, startface, startorientation,w, h, unusedfaces, svg=dwg)
            dwg.save()