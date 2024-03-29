from _resources.tiling_dicts import uniform1
from _resources.tiling_dicts import uniform2
from _resources.tiling_dicts import uniform3
from _resources.tiling_dicts import uniform4


uniform_tilings = {**uniform1, **uniform2, **uniform3, **uniform4}

import pprint

if __name__ == "__main__":
    print(uniform_tilings)
    with open("../uniform_tiling_supertiles.py", "w") as f:
        f.write("uniform_tilings = \\\n")
        f.write(pprint.pformat(uniform_tilings, indent=1, sort_dicts=False))

"""from _1uniform_tilings import uniform1
    import archimedean_tilings
from isogonal_tilings import biisogonal_tilings
from platonic_tilings import platonic_tilings
from triisogonal_vertex_homogeneous import triisogonal_vertex_homogeneous
uniform_tilings = {**1, **archimedean_tilings, **biisogonal_tilings, **triisogonal_vertex_homogeneous}
names = list(all_tilings)
print(names)

sizes = set()

for tiling in all_tilings.values():
    for neigh in tiling.values():
        sizes.add(len(neigh))

print(sorted(sizes))

print(len(all_tilings))"""