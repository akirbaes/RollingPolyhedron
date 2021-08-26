# Rolling Regular-faced Polyhedron in N-Uniform Tilings

A polyhedron with a regular face can sit on a tiling using the same polygon.

This work explores such polyhedron rolling on various tilings with matching faces, and what area can be reached.

## ScreenspaceRoller.py

Generates a rolling space that fits in the screen/in a given area and explores it. Various options and output types. Color explored tiles by number of face/tile/orientation combinations.

## RollingProof.py

Generates a proof of rolling area by using the symmetries in the rolling structure. Outputs images and pickled dictionaries.

----
 
# Other tools

## Unlimited Net Drawer

**Useful for: checking the path of a polyhedron**

Left and Right to choose a poly out of Johnsons, Platonics, most Archimedeans and some Prisms

Up and Down to choose the starting face

Click to roll and cover the space

Enter to take a screenshot

## tiling_drawer.py

**Useful for: creating a tiling dict manually based on an image**

Mousewheel to change shape

Left click to add a cell

Right click on a cell to remove it and its children

Right click on an edge to link it to another edge

Once all edges are linked, it will prompt you to save the net under a name.

## tiling_visualisation.py

**Useful for: visualising a tiling**

Plots tilings and makes a screenshot

Might need to change the default values

----

# Resources

## tiling_dicts

A folder with tiling dictionaries for a lot of tilings!

## poly_dicts

A folder with net dictionaries for a lot of polyhedrons!

 ----

 ----

# Legacy files 

**to delete or archive**


## NetDrawer

I used this to find back the tessellation net based on the net. Basis for tiling_drawer and Unlimited Net Drawer

## main.py

Rolls whatever shape I chose in the space, with marks for orientation. Very unreadable. Work in Progress!

## IsohedralTileRollExplore

Turns a tiling into a coordinates system and explores it while coloring based on coordinates. Work in Progress!
