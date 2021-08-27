from archimedean_tilings import archimedean_tilings
from isogonal_tilings import biisogonal_tilings
from platonic_tilings import platonic_tilings
from triisogonal_vertex_homogeneous import triisogonal_vertex_homogeneous
all_tilings = {**platonic_tilings, **archimedean_tilings, **biisogonal_tilings, **triisogonal_vertex_homogeneous}
names = list(all_tilings)
print(names)