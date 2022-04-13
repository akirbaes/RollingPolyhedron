import sys
sys.path.append("../..")
import os
import pickle
from _resources.uniform_tiling_supertiles import uniform_tilings as all_tilings
from _resources.regular_faced_polyhedron_nets import all_nets



def draw_lines_svg(svg,lineslist):
    area = (RollyPoint(0,0),RollyPoint(800,0),RollyPoint(800,800),RollyPoint(0,800))
    #maybe optimize them
    for segment in lineslist:
        if is_inside(RollyPoint(segment[0]),area) or is_inside(RollyPoint(segment[1]),area):
            svg.add(svg.line(*segment, stroke="black", stroke_width=2))
    return svg


def draw_polygons_svg(svg,polylist):
    #maybe optimize them
    area = (RollyPoint(0,0),RollyPoint(800,0),RollyPoint(800,800),RollyPoint(0,800))
    for poly in polylist:
        if(any(is_inside(RollyPoint(point),area) for point in poly)):
            svg.add(svg.polygon(poly, fill="red"))
    return svg

def draw_filled_result_svg(filename, mapping, visited):
    def comparesegments(s1,s2):
        return sum((abs(s1[s][xy]-s2[s-1][xy])<=1 for s in range(2) for xy in range(2)))==4
    segments = set()
    # print(mapping.values())
    for visitedplace in mapping.values():
        # print(visitedplace)
        # for cface, cell, tiledistance, celldistance in visitedplace:
        cface = convertToTuples(visitedplace[0])
        for i in range(len(cface)):
            segment = cface[i-1],cface[i]
            if not any(comparesegments(segment,other_segment) for other_segment in segments):
                segments.add(segment)
    polys = list()
    for visitedplace in visited.values():
        if(visitedplace):
            c, f, o, poly = visitedplace[0] #there can be several, I didn't really do a good job with poly's duplication
            polys.append(convertToTuples(poly))

    svg = svgwrite.Drawing(filename+'.svg', profile='tiny',height=800, width=800)
    draw_polygons_svg(svg,polys)
    draw_lines_svg(svg,segments)
    svg.save()
    return
    
def stable_cells_multipleresults(all_results,poly):
    #[TODO]
    return []

def stable_cells_symmetries(result,poly):
    #[TODO]
    #unstable:
    #unused face matches the sides
    #not every compatible cfo (sym) appears in visits
    #
    """
    for cell, visits in result:
        total = 0
        
        
    """
    return []
    
def face_complete_cells(result,poly):
    face_completes = []
    facepergon = [(face if len(neigh)==gon for face,neigh in poly.items()) for gon in range(12)]
    for cell,res in result.items():
        cell_gon = len(cell[1]) #check how it is structured
        usedfaces = facepergon[cell_gon]
        cellfaces = set(face for face,_ori in res)
        if(all(face in cellfaces for face in usedfaces)):
            face_completes.append(cell)
    
def used_faces(result, poly):
    used_faces = set(face for face, _ori in res for res in result.values())

def incompatible_cells(tiling,poly):
    incompatible = []
    compatibility = (len(neigh) for neigh in poly.values())
    for startcell,neighbours in tiling.items():
        if len(neighbours) not in compatibility:
            incompatible.append(startcell)
    return incompatible

if __name__ == "__main__":
    pass