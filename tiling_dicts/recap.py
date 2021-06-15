from archimedean_tilings import archimedean_tilings
from isogonal_tilings import biisogonal_tilings
from platonic_tilings import platonic_tilings

names = list(platonic_tilings.keys())+list(archimedean_tilings.keys())+list(biisogonal_tilings.keys())
print(names)