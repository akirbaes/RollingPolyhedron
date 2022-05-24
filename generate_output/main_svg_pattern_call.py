import pickle
import pprint
import sys
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

from _libs.RollingProofImageGen import generate_image
#def generate_image(tiling,polyhedron,tilingname,polyname,classes,group,groups,hexborders,symmetries,explored,type,stable_spots = []):
if __name__ == "__main__":
    print("Test")
    print(tiling)
    for (tilingname,polyname),data in rollingresults.items():
        borders = generate_supertile_coordinate_helpers(tiling, tilingname)
        classes, transformations, groups = CFOClassGenerator.generate_CFO_classes(tiling, net, polyname, tilingname, None)

        connected_classes = data["CFO_class_groups"]
        equivalent_states = data["CFO_classes"]
        for connected_data in data["all_data"]:
            explored_tiles = connected_data["exploration"]
            symmetry_vectors = connected_data["symmetry_vectors"]
        adjacent_classes = data["class_to_supertile_coordinates"]


