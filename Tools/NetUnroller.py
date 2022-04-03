#Shows a partial net of the poly to click on to expand
#Once fully expanded, prints the partial tiling (dictionary)
#And takes a screenshot
#This helps rebuilding the tessellation net from an image
#Because otherwise it's hard to match the orientation of the faces

#main creates edges→loop
#fully expanded: second_main prints the net and takes a picture→return to main
#[Enter]→go to next polyhedron
import pygame
from _libs.GeometryFunctions import *
from _resources.TessellationPolyhedron.PolyAndTessNets import *

pp = pprint.PrettyPrinter(indent=4)
WIDTH = 600
HEIGHT = 600
EDGE_SIZE = 30
p1 = RollyPoint(300, 300)
p2 = RollyPoint(300 + EDGE_SIZE, 300)
depths = dict()

visitedfaces= set()
visitededges=set()
#visited or not on the other structure
#then the missing visits
all_objects = []


def get_all_depths():
    return [depths[d] for d in sorted(depths.keys())]


def get_surface(depth):
    if (depth not in depths):
        depths[depth] = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    return depths[depth]


def wipe_surface(depth):
    get_surface(depth).fill((0, 0, 0, 0))


def initialise_drawing():
    global screen, s
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
    screen.fill((255, 255, 255))
    s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # working surface
    s.fill((0, 0, 0, 0))


def refresh():
    screen.fill((255, 255, 255))
    for surf in get_all_depths():
        screen.blit(surf, (0, 0))
    pygame.display.update()


def draw_text(depth, text, x, y, color, size):
    text = pygame.font.SysFont(None, int(round(size))).render(text, True, color)
    get_surface(depth).blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))


def draw_polygon(depth, points, color, alpha=1, outline=False):
    surf = get_surface(depth)
    color_alpha = color + (int(alpha * 255),)
    s.fill((0,0,0,0))
    pygame.draw.polygon(s, color_alpha, [(p.x, p.y) for p in points])
    surf.blit(s,(0,0))
    if outline:
        pygame.draw.lines(surf, (0, 0, 0), True, [(p.x, p.y) for p in points])


def second_main():
    #delete all edges and reconstruct the net part of the tiling
    poly = all_objects[0].poly
    face1 = all_objects[0].face1
    partial_net = dict()
    faces = [face1]
    while(len(partial_net)<len(poly)):
        face=faces.pop()
        ref = poly[face]
        newpath = []
        partial_net[face]=newpath
        for f in ref:
            if((face,f) in visitededges):
                newpath.append(f)
            else:
                newpath.append(None)
            if(f not in partial_net):
                faces.append(f)
    pp.pprint(partial_net)

    wipe_surface(2)
    wipe_surface(0)
    wipe_surface(1)
    for edge in all_objects:
        edge.draw()
    refresh()
    pygame.image.save(screen, "%s.png"%polyname)
    #pygame.scrap.init()
    #pygame.scrap.put(pygame.SCRAP_BMP,screen.)


def loop():
    global all_objects
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        wipe_surface(2)
        wipe_surface(0)
        wipe_surface(1)
        for edge in all_objects:
            edge.draw()
            edge.draw_cursor()
        refresh()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                for edge in all_objects:
                    if(e.button==1):
                        edge.mouse_click()
                    elif(e.button==3):
                        edge.mouse_right_click()
            if e.type== pygame.KEYDOWN and e.key == pygame.K_RETURN:
                all_objects = []
                running=False
                #jump to step 2

            if e.type == pygame.QUIT:
                running = False
                print("Quit!", flush=True)
                exit()


class Edge():
    depth = 0

    def __init__(self, coords, poly, face0, face1):
        self.children=[]
        self.active = True
        self.coords = coords
        self.p1, self.p2 = coords
        self.poly = poly
        self.face0 = face0  # previous face : do not draw
        self.face1 = face1  # next face: draw
        self.nextshape = len(poly[face1])
        shape = (None, None, None, triangle, square, None, hexagon)[self.nextshape]
        self.points = shape(self.p1, self.p2)
        self.draw()

    def draw(self):
        if(self.active):
            surf = get_surface(Edge.depth)
            pygame.draw.circle(surf, (0, 0, 0), tuple(int(x) for x in self.p1), 2)
            pygame.draw.circle(surf, (0, 0, 0), tuple(int(x) for x in self.p2), 2)
            pygame.draw.line(surf, (0, 0, 0), tuple(int(x) for x in self.p1), tuple(int(x) for x in self.p2), 1)
        else:
            surf = get_surface(Edge.depth)
            draw_polygon(1,self.points,(255,0,0),0.5,0)
            draw_polygon(1,self.points,(0,0,0),0,1)
            center = centerpoint(self.points)
            draw_text(1,str(self.face1),*center,(0,0,0),EDGE_SIZE/2)


    def draw_cursor(self):
        surf = get_surface(2)
        if(self.active):
            if self.face1 not in visitedfaces:
                pygame.draw.line(surf, (0, 255, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)
                if (self.mouse_inside()):
                    pygame.draw.polygon(surf, (0, 128, 255, 128), [(p.x, p.y) for p in self.points])
                    center = centerpoint(self.points)
                    draw_text(2,str(self.face1),*center,(0,0,0),EDGE_SIZE/2)
                else:
                    center = centerpoint(self.points)
                    draw_text(2,str(self.face1),*center,(192,192,192),EDGE_SIZE/2)
                    draw_polygon(1,self.points,(0,0,0),0.1,0)
                    #pygame.draw.polygon(surf, (0, 0, 0, 16), [(p.x, p.y) for p in self.points])
            else:
                pygame.draw.line(surf, (0, 0, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)

    def mouse_inside(self):
        mx, my = pygame.mouse.get_pos()
        return is_inside(RollyPoint(mx, my), self.points)

    def mouse_click(self):
        if (self.mouse_inside() and self.active and self.face1 not in visitedfaces):
            print(visitededges)
            self.active=False
            visitedfaces.add(self.face1)
            if(self.face0 in visitedfaces):
                visitededges.add((self.face0,self.face1))
                visitededges.add((self.face1,self.face0))
            print(visitededges)
            #net_structure.get(self.face0,[]).append(self.face1) #or rather: empty structure, set edge to None or face1
            for i in range(1,len(self.points)):
                pa = self.points[i]
                pb = self.points[(i+1)%len(self.points)]
                next_edges = self.poly[self.face1]
                old_edge_id = next_edges.index(self.face0)
                next_edge = next_edges[(old_edge_id+i)%len(next_edges)]
                #must reverse order since we want the shape to continue outside
                ed=Edge((pb, pa), poly, self.face1, next_edge)
                all_objects.append(ed)
                self.children.append(ed)
            if(len(visitedfaces)==len(self.poly)):
                second_main()
    def mouse_right_click(self):
        if (self.mouse_inside()) and not self.active:
            self.remove_traces()
    def remove_traces(self):
        if(not self.active):
            visitedfaces.remove(self.face1)
            try:
                visitededges.remove((self.face0,self.face1))
            except KeyError:
                pass
            try:
                visitededges.remove((self.face1,self.face0))
            except KeyError:
                pass
            for ed in self.children:
                ed.remove_traces()
                all_objects.remove(ed)
        self.children=[]
        self.active=True
            #delete the edges that were created by this, and its descendance


if __name__ == "__main__":
    for working_poly in ["icosahedron","j89","j90","j12","j13","j17","j51","j84"]:
        global polyname
        polyname = working_poly
        poly = polys[working_poly]
        initialise_drawing()
        #pygame.scrap.init()
        #pygame.scrap.put(pygame.SCRAP_BMP,pygame.surfarray.array3d(screen))
        visitedfaces=set()
        visitededges=set()
        all_objects.append(Edge((p1, p2), poly, 0, poly[0][0]))
        all_objects.append(Edge((p2, p1), poly, poly[0][0], 0))
        refresh()
        print(working_poly)
        loop()
