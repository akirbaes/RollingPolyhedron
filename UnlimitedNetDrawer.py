"""Checking the path of a polyhedron
Left and Right to choose a poly out of Johnsons, Platonics, most Archimedeans and some Prisms
Up and Down to choose the starting face
Click to roll and cover the space
[Enter] to take a screenshot"""
#Roll a poly by clicking to expand
#Left and Right changes the poly
#Up and Down changes the starting face
import pprint, time, pygame
import traceback

from GeometryFunctions import *
from poly_dicts.johnson_nets import johnson_nets
from poly_dicts.plato_archi_nets import plato_archi_nets
from poly_dicts.prism_nets import prism_nets
from PolyFunctions import visualise
WIDTH = 1000
HEIGHT = 1000
EDGE_SIZE = 50
p1 = Point(WIDTH/2, HEIGHT/2)
p2 = Point(WIDTH/2+EDGE_SIZE, HEIGHT/2)

all_poly = dict(**plato_archi_nets, **johnson_nets, **prism_nets)
all_poly_names = list(all_poly.keys())

startface = 0
#startface=all_poly_names.index("cube")
working_poly_id = 0


visitedfaces= set()
visitededges=set()
poly=None
all_objects = []


depths = dict()

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

def loop():
    global all_objects
    global working_poly_id
    global startface
    clock = pygame.time.Clock()
    running = True
    drawn = False
    while running:
        clock.tick(30)
        wipe_surface(2)
        wipe_surface(0)
        wipe_surface(1)
        for edge in all_objects:
            edge.draw()
            edge.draw_cursor()
        if(len(visitedfaces)<=1):
            if(not drawn):
                visualise(poly, p1, p2, startface, poly[startface][0], surf=get_surface(2), screen=screen, shapes=get_surface(3))
                drawn=True
        else:
            wipe_surface(3)
            drawn=False
        draw_text(1, polyname.capitalize(), WIDTH / 2, 20, (0, 0, 0), 35)
        if ((set(poly.keys()) - visitedfaces)):
            draw_text(1, "Unvisited:" + str((set(poly.keys()) - visitedfaces)), WIDTH / 2, 50, (0, 0, 0), 35)
        refresh()
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                for edge in all_objects:
                    if(e.button==1):
                        edge.mouse_click()
                    elif(e.button==3):
                        edge.mouse_right_click()

                print("Visited:", visitedfaces or None)
                print("Not visited:", (set(poly.keys()) - visitedfaces) or None)
            if e.type== pygame.KEYDOWN and e.key == pygame.K_RETURN:
                filename = "%s[%s.png" % (polyname,int(time.time()))
                draw_text(1,polyname.capitalize(),WIDTH/2,20,(255,0,0),35)
                if((set(poly.keys()) - visitedfaces)):
                    draw_text(1,"Unvisited:"+str((set(poly.keys()) - visitedfaces)),WIDTH/2,50,(255,0,0),35)
                refresh()
                pygame.image.save(screen, filename)
                print("Saved",filename)

            if e.type== pygame.KEYDOWN and e.key == pygame.K_LEFT:
                startface=0
                working_poly_id=(working_poly_id-1)%len(all_poly_names)
                running = False
            if e.type== pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                startface=0
                working_poly_id=(working_poly_id+1)%len(all_poly_names)
                running = False

            if e.type== pygame.KEYDOWN and e.key == pygame.K_UP:
                startface=(startface+1)%len(poly)
                running = False
            if e.type== pygame.KEYDOWN and e.key == pygame.K_DOWN:
                startface=(startface-1)%len(poly)
                running = False

            if e.type == pygame.QUIT:
                running = False
                print("Quit!", flush=True)
                exit()

    #
    wipe_surface(2)
    #wipe_surface(0)
    #wipe_surface(1)
    wipe_surface(3)

class DummyParent():
    def __init__(self):
        self.favorite = None

class Edge():
    depth = 0

    shapes_functions = (None, None, None, triangle, square, pentagon, hexagon, None, octagon, None, decagon, None, dodecagon)

    def __init__(self, coords, poly, face0, face1, parent):
        self.favorite = None
        self.parent = parent
        self.children=[]
        self.active = True
        self.coords = coords
        self.p1, self.p2 = coords
        self.poly = poly
        self.face0 = face0  # previous face : do not draw
        self.face1 = face1  # next face: draw
        self.nextshape = len(poly[face1])
        try:
            shape = Edge.shapes_functions[self.nextshape]
            self.points = shape(self.p1, self.p2)
        except:
            print("Tried to draw shape with %i sides"%self.nextshape)
            traceback.print_exc()
        self.draw()

    def draw(self):
        if(self.active):
            surf = get_surface(Edge.depth)
            pygame.draw.circle(surf, (0, 0, 0), tuple(int(x) for x in self.p1.as_tuple()), 2)
            pygame.draw.circle(surf, (0, 0, 0), tuple(int(x) for x in self.p2.as_tuple()), 2)
            pygame.draw.line(surf, (0, 0, 0), tuple(int(x) for x in self.p1.as_tuple()), tuple(int(x) for x in self.p2.as_tuple()), 1)
        else:
            surf = get_surface(Edge.depth)
            draw_polygon(1,self.points,(255,0,0),0.5,0)
            draw_polygon(1,self.points,(0,0,0),0,1)
            border = centerpoint((self.p1.as_tuple(), self.p2.as_tuple()))
            center = centerpoint(self.points)

            surf = get_surface(1)
            pygame.draw.line(surf, (250, 250, 250,255), border, center, 3)

            if not(self.favorite is None):
                border = centerpoint((self.p1.as_tuple(), self.p2.as_tuple()))
                border = centerpoint(self.favorite.points)

            draw_text(1,str(self.face1),*center,(0,0,0),EDGE_SIZE/2)


    def draw_cursor(self):
        surf = get_surface(2)
        if(self.active):
            if self.is_parent_favorite(): #self.face1 not in visitedfaces:
                pygame.draw.line(surf, (0, 255, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)
                if (self.mouse_inside()):
                    pygame.draw.polygon(surf, (0, 128, 255, 128), [(p.x, p.y) for p in self.points])
                    center = centerpoint(self.points)
                    border = centerpoint((self.p1.as_tuple(), self.p2.as_tuple()))
                    #pygame.draw.line(surf, (250, 250, 250), border, center, 3)
                    draw_text(2,str(self.face1),*center,(0,0,0),EDGE_SIZE/2)
                else:
                    center = centerpoint(self.points)
                    border = centerpoint((self.p1.as_tuple(), self.p2.as_tuple()))
                    #pygame.draw.line(surf, (250, 250, 250), border, center, 3)
                    draw_text(2,str(self.face1),*center,(192,192,192),EDGE_SIZE/2)
                    draw_polygon(1,self.points,(0,0,0),0.1,0)
                    #pygame.draw.polygon(surf, (0, 0, 0, 16), [(p.x, p.y) for p in self.points])
            #else:
            #    pygame.draw.line(surf, (0, 0, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)

    def is_parent_favorite(self):
        return self.parent.favorite==None or self is self.parent.favorite

    def mouse_inside(self):
        mx, my = pygame.mouse.get_pos()
        return is_inside(Point(mx, my), self.points)

    def mouse_click(self,force=False):
        if ((self.mouse_inside() or force) and self.active and self.is_parent_favorite()):# and self.face1 not in visitedfaces):
            # print(visitededges)
            self.active=False
            visitedfaces.add(self.face1)
            if(self.face0 in visitedfaces):
                visitededges.add((self.face0,self.face1))
                visitededges.add((self.face1,self.face0))
            # print(visitededges)
            #net_structure.get(self.face0,[]).append(self.face1) #or rather: empty structure, set edge to None or face1
            start = 0 #start = 1
            for i in range(start,len(self.points)):
                pa = self.points[i]
                pb = self.points[(i+1)%len(self.points)]
                next_edges = self.poly[self.face1]
                old_edge_id = next_edges.index(self.face0)
                next_edge = next_edges[(old_edge_id+i)%len(next_edges)]
                #must reverse order since we want the shape to continue outside
                ed=Edge((pb, pa), poly, self.face1, next_edge, self)
                all_objects.append(ed)
                self.children.append(ed)
                self.parent.favorite=self
            #if(len(visitedfaces)==len(self.poly)):
            #    second_main()
    def mouse_right_click(self):
        if (self.mouse_inside()) and not self.active:
            self.remove_traces()
    def remove_traces(self):
        if(not self.active):
            try:
                visitedfaces.remove(self.face1)
            except:
                pass
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
        self.favorite=None
        self.parent.favorite=None
        self.active=True
            #delete the edges that were created by this, and its descendance


initialise_drawing()

if __name__ == "__main__":
    while(True):
        working_poly = all_poly_names[working_poly_id]
        polyname = working_poly
        poly = all_poly[working_poly]
        visitedfaces=set()
        visitededges=set()
        dummy=DummyParent()
        secondface = poly[startface][0]
        all_objects = []
        startedge = Edge((p1, p2), poly, secondface, startface ,dummy)
        all_objects.append(startedge)
        startedge.mouse_click(force=True)
        #all_objects.append(Edge((p2, p1), poly, secondface, startface,dummy))
        refresh()
        print(working_poly.capitalize(),"face #%i (%i/%i)"%(startface,startface+1,len(poly)))
        loop()
