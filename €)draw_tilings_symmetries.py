import math
import os
import sys

import pygame

from GenPngScreenspaceRoller import convertToTuples, map_screenspace, draw_background
from GeometryFunctions import centerpoint, distance
from RollyPoint import RollyPoint

def create_cell_groups(symmetries):
    different_groups = set()
    different_groups_list = list()
    self_symmetries = dict()
    for group in symmetries:
        cells = set(t for (t,o) in group)
        if(tuple(sorted(cells)) not in different_groups):
            different_groups.add(tuple(sorted(cells)))
            different_groups_list.append(group)
        selfsym = dict()
        for (t,o) in group:
            for (tt,oo) in group:
                if (t,o)!=(tt,oo) and t==tt:
                    selfsym.setdefault(t, set())
                    selfsym[t].add(o)
                    selfsym[t].add(oo)
        for tile, orientations in selfsym.items():
            self_symmetries.setdefault(tile,list())
            self_symmetries[tile].append(tuple(orientations))
    return different_groups_list, self_symmetries

def draw_symmetries(surf,grid,smallgrid,symmetries):
    groups, self_symmetries = create_cell_groups(symmetries)
    letter = ord('A')
    symmetrical_cells = dict()
    for index, group in enumerate(groups):
        if(len(set(c for c,o in group))>1):
            for cell,orientation in group:
                symmetrical_cells[cell]=chr(letter),orientation
            letter+=1
            if letter==ord("d"):
                letter+=1
    light = 160
    internal_symcolors = ((255,light,light),(light,255,light),(light,light,255),(255,255,light),(255,light,255),(light,255,255))

    for data in grid.values():
        points = data[0]
        cell = data[1]
        center = centerpoint(points)
        width = distance(points[0],points[int(len(points)/2)])

        if cell in self_symmetries:
            for color_index,linkedsides in enumerate(self_symmetries[cell]):
                color = internal_symcolors[color_index]

                for point_index in linkedsides:
                    p1 = points[point_index]
                    p2 = points[(point_index+1)%len(points)]
                    pc = centerpoint((p1,p2))
                    pygame.draw.polygon(surf, color, convertToTuples((p1,p2,center)), 0)

            pygame.draw.circle(surf, (255,255,255), center, int(width/
                            (max(3,4-(len(points)-3)/4.5)
                                                                )))
            #max 2.5 is also neat

        #distance = data[2] #not always available, distance from center
        # print(points)
        # pygame.draw.polygon(surf, color, convertToTuples(points), width)

    for data in smallgrid.values():
        points = data[0]
        cell = data[1]
        center = centerpoint(points)
        width = distance(points[0],points[int(len(points)/2)])
        if cell in symmetrical_cells:
            marker,orientation = symmetrical_cells[cell]
            font = pygame.font.SysFont(None, int(round(width)))
            font.set_underline(True)
            text = font.render(marker, True, (0,0,0))
            p1 = points[orientation]
            p2 = points[(orientation+1)%len(points)]
            dx = (p2-p1).x
            dy = (p2-p1).y
            angle = math.atan2(-dy,dx) * 180 / math.pi
            if cell in self_symmetries and len(self_symmetries[cell])==1 and len(self_symmetries[cell][0])==len(points):
                # print(len(self_symmetries[cell][0]),len(points))
                angle=0
            text = pygame.transform.rotate(text, angle)
            text = pygame.transform.scale(text,(int(text.get_width()/2),int(text.get_height() / 2)))
            surf.blit(text, (center[0] - text.get_width() / 2, center[1] - text.get_height() / 2))


def draw_tiling_symmetries():
    pygame.init()
    from tiling_dicts.combine_uniform_tilings import uniform_tilings as all_tilings
    for tilingname, tiling in all_tilings.items():
        print(tilingname)
        # screen = pygame.display.set_mode((800, 800), pygame.DOUBLEBUF)
        screen = pygame.Surface((800, 800), pygame.SRCALPHA)
        screen.fill((255, 255, 255, 255))
        outlines = pygame.Surface((800, 800), pygame.SRCALPHA)
        area = (0, 0, 1000, 1000)

        area = (-200, -200, 1000, 1000)
        area2 = (0, 0, 800, 800)
        xx = (area[0] + area[2]) / 2
        yy = (area[1] + area[3]) / 2
        p1 = RollyPoint(xx, yy)
        EDGESIZE = 50
        p2 = RollyPoint(xx + EDGESIZE, yy)
        precision = 7

        mapping = map_screenspace(tiling, 0, area, p1, p2, 1)
        single = map_screenspace(tiling, 0, area, p1, p2, 1, limit=True)
        outlines = pygame.Surface((800, 800), pygame.SRCALPHA)
        outlines.fill((255, 0, 255, 0))
        from symmetry_classes.tiling_symmetries import tiling_symmetries
        draw_symmetries(screen, mapping, single, tiling_symmetries[tilingname])
        draw_background(screen, mapping, (0, 0, 0),3)
        draw_background(screen, single, (0, 0, 0), 8)
        # draw_background(screen, single, (0, 0, 0))
        text = pygame.font.SysFont(None, int(round(40))).render(tilingname.replace("u","-uniform ").replace("x","."),True,(0,0,0),(255,255,255))
        screen.blit(text,(0,0))
        # refresh()
        path = "tiling_dicts/tiling_pictures"
        try:os.mkdir(path)
        except:pass
        pygame.image.save(screen, path + os.sep + tilingname + ".png")

if __name__ == "__main__":
    draw_tiling_symmetries()