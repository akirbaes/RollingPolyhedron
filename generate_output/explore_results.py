import pickle
import pprint
with open('../_results/rollersdata.pickle', 'rb') as handle:
    rollersdata, all_tilings, all_nets = pickle.load(handle)
    # Only contains the result type string

with open("../_results/rolling_results.pickle", "rb") as handle:
    rollingresults = pickle.load(handle)

# pprint.pprint(rollersdata)
# # print(list(rollersdata.keys()))
# pprint.pprint(rollersdata[list(rollersdata)[0]])

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

