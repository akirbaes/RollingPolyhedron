from tiling_dicts._1uniform_tilings import uniform1
from tiling_dicts._2uniform_tilings import uniform2
from tiling_dicts._3uniform_tilings import uniform3


uniform_tilings = {**uniform1, **uniform2, **uniform3}

if __name__ == "__main__":
    print(uniform_tilings)

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