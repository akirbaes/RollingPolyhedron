# to work on to create a tiling creation software
# has some useless functions copied from NetDrawer
import pprint
import traceback

import pygame
from GeometryFunctions import *
from PolyAndTessNets import *

pp = pprint.PrettyPrinter(indent=4)
WIDTH = 800
HEIGHT = 800
EDGE_SIZE = 40
p1 = Point(300, 300)
p2 = Point(300 + EDGE_SIZE, 300)
depths = dict()

current_facetype = 3
facetypes = [3, 4, 6, 12]
visitedfaces = set()
visitededges = set()
# visited or not on the other structure
# then the missing visits
all_objects = []

selected_edge = None
copy_change = "update"

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
    s.fill((0, 0, 0, 0))
    pygame.draw.polygon(s, color_alpha, [(p.x, p.y) for p in points])
    surf.blit(s, (0, 0))
    if outline:
        pygame.draw.lines(surf, (0, 0, 0), True, [(p.x, p.y) for p in points])


def second_main():
    # delete all edges and reconstruct the net part of the tiling
    poly = all_objects[0].poly
    face1 = all_objects[0].face1
    partial_net = dict()
    faces = [face1]
    while (len(partial_net) < len(poly)):
        face = faces.pop()
        ref = poly[face]
        newpath = []
        partial_net[face] = newpath
        for f in ref:
            if ((face, f) in visitededges):
                newpath.append(f)
            else:
                newpath.append(None)
            if (f not in partial_net):
                faces.append(f)
    pp.pprint(partial_net)

    wipe_surface(2)
    wipe_surface(0)
    wipe_surface(1)
    for edge in all_objects:
        edge.draw()
    refresh()
    pygame.image.save(screen, "%s.png" % polyname)
    # pygame.scrap.init()
    # pygame.scrap.put(pygame.SCRAP_BMP,screen.)


def loop():
    global all_objects
    global copy_change
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(30)
        wipe_surface(2)
        wipe_surface(0)
        wipe_surface(1)
        Edge.closest = None
        if(copy_change=="update"):
            wipe_surface(-1)
            copy_change="change"
        for edge in all_objects:
            edge.draw()
        for edge in all_objects:
            edge.draw_cursor()
        refresh()
        copy_change = "no change"
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                if (e.button == 4):
                    global current_facetype
                    current_facetype = facetypes[(facetypes.index(current_facetype) + 1) % len(facetypes)]
                    # wheel_up
                elif (e.button == 5):
                    current_facetype = facetypes[facetypes.index(current_facetype) - 1]
                    # wheel down
                mouse_right_triggers = list()
                for edge in all_objects:
                    edge.polysize = current_facetype
                    if(edge.active):edge.update_shape()
                    if(edge.mouse_inside()):
                        if (e.button == 1):
                            if(edge.mouse_click()):
                                get_tiling()
                            break
                        elif (e.button == 3):
                            mouse_right_triggers.append(edge)
                if(mouse_right_triggers):
                    #the issue is that a lot overlap
                    distances = [distance(centerpoint((edge.p1,edge.p2)), pygame.mouse.get_pos()) for edge in mouse_right_triggers]
                    mouse_right_triggers[distances.index(min(distances))].mouse_right_click()
                    get_tiling()
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                all_objects = []
                running = False

                # jump to step 2

            if e.type == pygame.QUIT:
                running = False
                print("Quit!", flush=True)
                exit()



def get_tiling():
    global copy_change
    copy_change="update"
    firstedge = all_objects[0]
    print("{")
    for edge in all_objects:
        edge.pcounter = 0
    for edge in all_objects:
        if not edge.active:
            neighbours = []
            neighbour_objects = []
            if(edge.parent!=None):
                neighbours.append(edge.parent.faceid)
            for chi in edge.children:
                if not chi.active:
                    if(chi.faceid in neighbours):
                        #duplicate! but we can't process it right now
                        chi.pcounter=neighbours.count(chi.faceid)
                    neighbours.append(chi.faceid)
                else:
                    if(chi.is_neighbour()):
                        neighbours.append(chi.other.parent.faceid)
                    else:
                        neighbours.append(None)


            print(edge.faceid,":",neighbours,len(edge.children))
    print("}")

def draw_copy(points,edge):
    global copy_change
    if(copy_change=="no change"):
        return
    drawn = []
    orientation = edge.parent.get_orientation(edge)
    #caseOrientation = currentCaseNeighbours.index(previouscase)  # décalage actuel par rapport à la normale
    # print("Orientation de case:",caseOrientation)
    # points = points[caseOrientation:]+points[:caseOrientation]
    #currentCaseNeighbours = currentCaseNeighbours[caseOrientation:] + currentCaseNeighbours[:caseOrientation]
    p1,p2 = (points[-orientation:]+points[:-orientation])[:2]

    to_draw = [(p1,p2,edge.parent)]
    while to_draw:
        p1,p2,shape = to_draw.pop()
        if(shape in drawn):
            continue
        neigh = []
        if(shape.parent!=None):
            neigh=[shape.parent]
        neigh += shape.children
        #is a full shape
        points = Edge.shapes_functions[len(shape.points)](p1,p2)
        #is a parent
        for id, chi in enumerate(neigh):
            if chi!=None and chi.active==False and chi.faceid not in drawn:
                # print(len(points),id)
                pa = points[(id)%len(points)]
                pb = points[(id+1)%len(points)]
                to_draw.append((pb,pa,chi))
                #pc=centerpoint((pa,pb))
                #draw_text(2, str(id), pa.x, pa.y, (0, 0, 255), EDGE_SIZE / 2)
        if shape.parent!=None and shape.parent not in drawn:
            ppoints = Edge.shapes_functions[len(shape.parent.points)](p2,p1)
            orientation = shape.parent.get_orientation(shape)
            #ppoints = list(reversed(ppoints))
            pa, pb = (ppoints[-orientation:] + ppoints[:-orientation])[:2]
            #neigh = (shape.parent.parent==None and [None] or [] )+ shape.parent.children
            #pa,pb = points[-neigh.index(shape)], points[+1-neigh.index(shape)]
            to_draw.append((pa,pb,shape.parent))


        if (shape.active == False):
            drawn.append(shape)
            draw_polygon(-1,points,(128,128,128),0.1)
            center=centerpoint(points)
            draw_text(-1,str(shape.faceid),center[0],center[1],(128,128,128),EDGE_SIZE/2)
class Edge():

    depth = 0
    numbering = set()
    shapes_functions = (None, None, None, triangle, square, None, hexagon, None, octagon, None, None, None, dodecagon)
    select_neighbour = None
    cursors = list()
    closest = None

    def update_shape(self):
        if(self.is_neighbour()):
            self.polysize=len(self.other.parent.points)
        shape = Edge.shapes_functions[self.polysize]
        self.points = shape(self.p1, self.p2)

    def __init__(self, coords, polysize, parent):
        self.pcount = 0  # as face
        self.p = -1  # as pairing edge
        self.parent = parent
        if(parent!=None):
            self.parent.children.append(self) #first edge doesn't have a parent
        self.other = None #Other edge it is equal to (its parent is the face)
        self.children = []
        self.active = True
        self.coords = coords  # pair
        self.p1, self.p2 = coords
        self.faceid = None #Once an edge becomes a face, it gains a faceid
        self.polysize = polysize
        self.update_shape()
        for edge in all_objects:
            #at creation, if equal to another edge, link them already
            #must be internal neighbour
            if (edge != self and self.same_position(edge) and edge.active):
                # print("Set same-position link between",self.parent.faceid,edge.parent.faceid)
                self.set_link(edge)
        self.draw()

    def get_orientation(self,edge):
        if(edge==self.parent):
            return 0
        else:
            return self.children.index(edge)+(self.parent!=None)
    def is_closest_cursor(self):
        if(Edge.closest == None):
            distances = [distance(centerpoint((edge.p1,edge.p2)), pygame.mouse.get_pos()) for edge in Edge.cursors ]
            Edge.closest = Edge.cursors[distances.index(min(distances))]
            Edge.cursors = []
        return Edge.closest == self

    def get_a_faceid(self):
        #Unique ID contiguous from 0. Tracks the ones dealt and removed
        number = 0
        while number in Edge.numbering:
            number += 1
            if (number not in Edge.numbering):
                break
        Edge.numbering.add(number)
        return number

    def forget_faceid(self):
        Edge.numbering.remove(self.faceid)

    def are_related(self,other):
        return self.other==other and \
                (self.parent == other or other.parent == self or self.same_position(other))

    def is_neighbour(self):
        #Meaning this edge is equal to another and parents are neighbours
        return self.other != None

    def get_unique_p(self, other_p=0):
        self.pcount = max(self.pcount + 1, other_p)
        return self.pcount

    def same_position(self, other):
        return distance(floatcenterpoint((self.coords)), floatcenterpoint(other.coords)) < 2

    def set_link(self, other):
        self.other = other
        other.other = self
        self.update_shape()
        other.update_shape()

        # print("Self:", self.parent.faceid)

        # print("Other:", other.parent.faceid)
        if (self.parent == other.parent and self.parent != None):
            # self link
            # functions also when linking to same edge
            p = self.parent.get_unique_p()
            # other.set_parent_neighbour(self.parent.faceid - p * self.parent.polysize)
            # self.set_parent_neighbour(self.parent.faceid + p * self.parent.polysize)
        elif (self.same_position(other)):
            # internal link
            pass
            # print("internal_link")
            # self.set_parent_neighbour(other.parent.faceid)
            # other.set_parent_neighbour(self.parent.faceid)
        else:
            # external link
            p = self.parent.get_unique_p(other.parent.get_unique_p())
            #other.pcount = p
            # self.set_parent_neighbour(other.parent.faceid + p * other.parent.polysize)
            # other.set_parent_neighbour(self.parent.faceid + p * self.parent.polysize)

        #self.set_parent_neighbour(self.parent.faceid)
        #other.set_parent_neighbour(other.parent.faceid)

    def refresh_shape(self, polysize):
        self.polysize = polysize
        shape = Edge.shapes_functions[self.polysize]
        self.points = shape(self.p1, self.p2)

    def draw(self):
        if self.active:
            surf = get_surface(Edge.depth)
            pygame.draw.circle(surf, (0, 0, 0), self.p1.as_tuple(), 2)
            pygame.draw.circle(surf, (0, 0, 0), self.p2.as_tuple(), 2)
            pygame.draw.line(surf, (0, 0, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)
            if self.is_neighbour():
                center = centerpoint(self.points)
                draw_text(1, str(self.other.parent.faceid), *center, (0, 0, 0), EDGE_SIZE / 2)
                draw_polygon(1, self.points, (0, 0, 0), 0, 1)
                if(not self.same_position(self.other)):
                    draw_copy(self.points,self.other)

            if (self.mouse_inside()):
                Edge.cursors.append(self)
        else:
            # surf = get_surface(Edge.depth)
            draw_polygon(1, self.points, (255, 0, 0), 0.5, 0)
            draw_polygon(1, self.points, (0, 0, 0), 0, 1)
            # border = centerpoint((self.p1.as_tuple(), self.p2.as_tuple()))
            center = centerpoint(self.points)

            # surf = get_surface(1)
            # pygame.draw.line(surf, (250, 250, 250,255), border, center, 3)

            if (self.faceid != None):
                draw_text(1, str(self.faceid), *center, (0, 0, 0), EDGE_SIZE / 2)

    def draw_cursor(self):
        surf = get_surface(2)
        if (self.active):
            if not self.is_neighbour():  # self.face1 not in visitedfaces:
                pygame.draw.line(surf, (0, 255, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)
                if(selected_edge==self):
                    pygame.draw.polygon(surf, (0, 180, 0, 128), [(p.x, p.y) for p in self.points])
                elif (self.mouse_inside() and self.is_closest_cursor()):
                    pygame.draw.polygon(surf, (0, 128, 255, 128), [(p.x, p.y) for p in self.points])
                    center = centerpoint(self.points)
                    border = centerpoint((self.p1.as_tuple(), self.p2.as_tuple()))
                    # pygame.draw.line(surf, (250, 250, 250), border, center, 3)
                    # draw_text(2,str(self.faceid),*center,(0,0,0),EDGE_SIZE/2)
                else:
                    center = centerpoint(self.points)
                    border = centerpoint((self.p1.as_tuple(), self.p2.as_tuple()))
                    # pygame.draw.line(surf, (250, 250, 250), border, center, 3)
                    # if(self.faceid!=None):
                    #    draw_text(2,str(self.faceid),*center,(192,192,192),EDGE_SIZE/2)
                    draw_polygon(1, self.points, (0, 0, 0), 0.1, 0)
                    # pygame.draw.polygon(surf, (0, 0, 0, 16), [(p.x, p.y) for p in self.points])
            elif(self.mouse_inside() and self.is_closest_cursor()):
                    pygame.draw.polygon(surf, (255, 0, 0, 32), [(p.x, p.y) for p in self.points])
            # else:
            #    pygame.draw.line(surf, (0, 0, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)

    def mouse_inside(self):
        mx, my = pygame.mouse.get_pos()
        return is_inside(Point(mx, my), self.points)

    def mouse_click(self):
        global selected_edge
        selected_edge = None

        if (self.mouse_inside() and self.active and not self.is_neighbour()):  # and self.face1 not in visitedfaces):
            self.active = False
            self.faceid = self.get_a_faceid()
            # self.set_parent_neighbour(self.faceid)
            start = 1
            if(len(all_objects)==1):
                start = 0
            for i in range(start, len(self.points)):
                pa = self.points[i]
                pb = self.points[(i + 1) % len(self.points)]
                # must reverse order since we want the shape to continue outside
                ed = Edge((pb, pa), self.polysize, self)
                all_objects.append(ed)
        else:
            return False
        return True

    def mouse_right_click(self):
        global selected_edge
        if (self.mouse_inside()) and not self.active:
            selected_edge=None
            self.remove_traces()
        elif (self.mouse_inside()) and self.active and len(all_objects)>1:
            # self.remove_traces()
            if(self.is_neighbour()):
                if(self.same_position(self.other)):
                    try:self.other.parent.remove_traces()
                    except:pass
                else:
                    self.remove_traces()
            else:
                if selected_edge==None:
                    selected_edge=self
                else:
                    self.set_link(selected_edge)
                    selected_edge=None

            # print(self.is_neighbour(), selected_edge)
            # link stuff by pairs
        else:
            return False
        return True

    def remove_traces(self):
        if (self.other != None):
            self.other.other = None
            # self.other.set_parent_neighbour(None)
            self.other = None
            # self.set_parent_neighbour(None)
        if (not self.active):
            for ed in self.children:
                ed.remove_traces()
                all_objects.remove(ed)
            self.forget_faceid()
        self.children = []
        self.active = True
        # delete the edges that were created by this, and its descendance


if __name__ == "__main__":
    global polyname
    initialise_drawing()
    # pygame.scrap.init()
    # pygame.scrap.put(pygame.SCRAP_BMP,pygame.surfarray.array3d(screen))
    firstEdge = Edge((p1, p2), current_facetype, None)
    #firstEdge.parent=secondEdge
    #secondEdge.children.append(firstEdge)
    #firstEdge.update_shape()
    all_objects.append(firstEdge)
    #all_objects.append(secondEdge)
    refresh()
    loop()