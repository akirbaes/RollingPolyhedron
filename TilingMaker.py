"""Create a tiling manually based on an image and export it as a dict
Mousewheel to change shape
Left click to add a face
Right click on a face to remove it and its children
Right click on an edge to link it to another edge
Once all edges are linked, it will prompt you to save the net under a name."""

# to work on to create a tiling creation software
# might have some useless functions copied from NetDrawer

#Issues: when saving, numbering is not checked, sometimes leaving big gaps
import os
import pprint
import tkinter
import tkinter.filedialog
import traceback

import pygame
from GeometryFunctions import *


pp = pprint.PrettyPrinter(indent=4)
WIDTH = 800
HEIGHT = 800
EDGE_SIZE = 40
p1 = RollyPoint(300, 300)
p2 = RollyPoint(300 + EDGE_SIZE, 300)
depths = dict()

current_facetype = 3
facetypes = [3, 4, 6, 12]

all_objects = [] #all edges

selected_edge = None
copy_change = "update"

###Drawing layers functions
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

###Drawing functions
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

###Main loop
def loop():
    global all_objects
    global copy_change
    clock = pygame.time.Clock()
    running = True
    tiling_result = {None: (None,)}

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


        if tiling_result and None not in (a for key in tiling_result for a in tiling_result[key]):
            top = tkinter.Tk()
            top.withdraw()  # hide window
            #filetypes=("Text txt",)
            file_name = tkinter.filedialog.asksaveasfilename(parent=top)
            basename = os.path.basename(file_name)
            top.destroy()
            try:
                f=open(file_name+'.py',"w")
                f.write(("all_tilings['%s'] = \\\n"%basename)+pprint.pformat(tiling_result,indent=4,sort_dicts=True))
                #f.write(pprint.pformat(tiling_result,indent=4,sort_dicts=True))
                f.close()
            except:
                traceback.print_exc()

            tiling_result_p = dict()
            for key in tiling_result:
                tiling_result_p[key] = [((isinstance(x,tuple) and x[0]+x[1]*len(tiling_result))) or (isinstance(x,int) and x) for x in tiling_result[key]]
            pprint.pprint(tiling_result_p,indent=4,sort_dicts=True)
            try:
                f=open(file_name+".oldformat","w")
                f.write(("all_tilings['%s'] = \\\n"%basename)+pprint.pformat(tiling_result_p,indent=4,sort_dicts=True))
                f.close()
            except:
                traceback.print_exc()

        tiling_result  = {None:(None,)}
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
                                tiling_result=get_tiling()
                            break
                        elif (e.button == 3):
                            mouse_right_triggers.append(edge)
                if(mouse_right_triggers):
                    #the issue is that a lot overlap
                    distances = [distance(centerpoint((edge.p1,edge.p2)), pygame.mouse.get_pos()) for edge in mouse_right_triggers]
                    mouse_right_triggers[distances.index(min(distances))].mouse_right_click()
                    tiling_result=get_tiling()
            global firstEdge
            global p2
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RIGHT:
                print("Rotate+")
                p2 = (p2-p1).rotate(15/180*pi)+p1
                all_objects[0].remove_traces()
                all_objects[0].__init__((p1,p2), current_facetype, None)
                # p2 = (p2-p1).rotate(15/180*pi)+p1
                # firstEdge = Edge((p1, p2), current_facetype, None)
                # all_objects.append(firstEdge)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_LEFT:
                print("Rotate-")
                p2 = (p2-p1).rotate(-15/180*pi)+p1
                all_objects[0].remove_traces()
                all_objects[0].__init__((p1,p2), current_facetype, None)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
                for edge in all_objects:
                    if edge.active:
                        for coord,edge2 in Edge.activelist.items():
                            if edge2!=edge:
                                if(distance(floatcenterpoint(edge.coords),coord))<2:
                                    edge.set_link(edge2)
                tiling_result=get_tiling()
            if e.type == pygame.KEYDOWN and e.key == ord("c"):
                #this is more for polyhedrons...
                for edge in all_objects:
                    if edge.active:
                        for edge2 in all_objects:
                            if edge2.active and edge2!=edge:
                                if distance(floatcenterpoint(edge.coords), floatcenterpoint(edge2.coords))<EDGE_SIZE/2:
                                    edge.set_link(edge2)
            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                running = False
            if e.type == pygame.QUIT:
                running = False
                print("Quit!", flush=True)
                exit()

            # refresh()

            """
            tiling_result_t = dict()
            for key in tiling_result:
                tiling_result_t[key] = [(isinstance(x,tuple) and x) or (isinstance(x,int) and (x,0)) for x in tiling_result[key]]
            pprint.pprint(tiling_result_t,indent=4,sort_dicts=True)
            try:
                f=open(file_name,"w")
                f.write(("all_tilings['%s'] = \\\n"%basename)+pprint.pformat(tiling_result_t,indent=4,sort_dicts=True))
                f.close()
            except:
                traceback.print_exc()"""

def get_tiling():
    """Generates the tiling dict and prints it"""
    global copy_change
    copy_change="update" #this shouldn't be there, tells when to redraw the background

    pcounter = 1
    all_neighbours = dict()
    for edge in all_objects:
        edge.pcounter = None
    for edge in all_objects:
        if not edge.active: #face
            neighbours = []
            if(edge.parent!=None):
                neighbours.append((edge.parent.faceid,0))
            for chi in edge.children:
                if not chi.active: #is another face: internal neighbour
                    neighbours.append((chi.faceid,0))
                else:
                    if(chi.is_neighbour()):
                        if(chi.same_position(chi.other)):#internal link
                            neighbours.append((chi.other.parent.faceid,0))
                        else:
                            if(chi.pcounter==None):#external link, risk of duplicate so numbering it
                                chi.pcounter = pcounter
                                chi.other.pcounter = pcounter
                                if(chi.parent == chi.other.parent):
                                    chi.other.pcounter = -pcounter
                                pcounter+=1
                            neighbours.append((chi.other.parent.faceid,chi.pcounter))
                    else:
                        neighbours.append(None)#edge not yet matched

            all_neighbours[edge.faceid]=neighbours
            #print(edge.faceid,":",neighbours,len(edge.children))
    pprint.pprint(all_neighbours,indent=4,sort_dicts=True)
    return all_neighbours


def draw_copy(points,edge, activelist = None):
    #Draws a copy of the whole thing outside
    #Inefficient but helpful
    if(activelist==None):
        activelist=dict()
    global copy_change
    if(copy_change=="no change"):
        return activelist
    drawn = []
    orientation = edge.parent.get_orientation(edge)
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
            if chi!=None and chi.active==True:
                pa = points[(id)%len(points)]
                pb = points[(id+1)%len(points)]
                pc = floatcenterpoint((pa,pb))
                if (pc not in activelist):
                    activelist[pc] = chi

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
        else:
            pc = floatcenterpoint((pa,pb))
            if (pc not in activelist):
                activelist[pc] = chi
    return activelist
class Edge():
    """Each edge of each polygon is an Edge object that turns into a face with children when deactivated"""
    depth = 0
    numbering = set()
    shapes_functions = (None, None, None, triangle, square, None, hexagon, None, octagon, None, None, None, dodecagon)
    select_neighbour = None
    cursors = list()
    closest = None
    activelist = dict()
    def reset(ignore):
        depth = 0
        numbering = set()
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
            pass
            # self link
            # functions also when linking to same edge
            #p = self.parent.get_unique_p()
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
            #p = self.parent.get_unique_p(other.parent.get_unique_p())
            pass
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
        #Draw one edge/face
        if self.active:
            surf = get_surface(Edge.depth)
            pygame.draw.circle(surf, (0, 0, 0), tuple(int(x) for x in self.p1.as_tuple()), 2)
            pygame.draw.circle(surf, (0, 0, 0), tuple(int(x) for x in self.p2.as_tuple()), 2)
            pygame.draw.line(surf, (0, 0, 0),
                             tuple(int(x) for x in self.p1.as_tuple()),
                                   tuple(int(x) for x in self.p2.as_tuple()), 1)
            if self.is_neighbour():
                center = centerpoint(self.points)
                draw_text(1, str(self.other.parent.faceid), *center, (0, 0, 0), EDGE_SIZE / 2)
                draw_polygon(1, self.points, (0, 0, 0), 0, 1)
                if(not self.same_position(self.other)):
                    Edge.activelist = {**draw_copy(self.points,self.other), **Edge.activelist}

            if (self.mouse_inside()):
                Edge.cursors.append(self)
        else:
            # surf = get_surface(Edge.depth)
            draw_polygon(1, self.points, (255, 0, 0), 0.5+self.mouse_inside()/2, 0)
            draw_polygon(1, self.points, (0, 0, 0), 0, 1)
            # border = centerpoint((self.p1.as_tuple(), self.p2.as_tuple()))
            center = centerpoint(self.points)

            # surf = get_surface(1)
            # pygame.draw.line(surf, (250, 250, 250,255), border, center, 3)

            if (self.faceid != None):
                draw_text(1, str(self.faceid), *center, (0, 0, 0), EDGE_SIZE / 2)

    def draw_cursor(self):
        #Draw the cursor (mouse reaction) to one edge/face
        surf = get_surface(2)
        if (self.active):
            if not self.is_neighbour():  # self.face1 not in visitedfaces:
                pygame.draw.line(surf, (0, 255, 0), tuple(int(x) for x in self.p1.as_tuple()),
                                 tuple(int(x) for x in self.p2.as_tuple()), 1)
                if(selected_edge==self):
                    pygame.draw.polygon(surf, (0, 180, 0, 128), [(int(p.x), int(p.y)) for p in self.points])
                elif (self.mouse_inside() and self.is_closest_cursor()):
                    pygame.draw.polygon(surf, (0, 128, 255, 128), [(int(p.x), int(p.y)) for p in self.points])
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
                    pygame.draw.polygon(surf, (255, 0, 0, 32), [(int(p.x), int(p.y)) for p in self.points])
            # else:
            #    pygame.draw.line(surf, (0, 0, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)

    def mouse_inside(self):
        mx, my = pygame.mouse.get_pos()
        return is_inside(RollyPoint(mx, my), self.points)

    def mouse_click(self):
        """Left click if activated turns into a face and makes children"""
        global selected_edge
        selected_edge = None

        if (self.mouse_inside() and self.active and not self.is_neighbour()):  # and self.face1 not in visitedfaces):
            self.active = False
            self.faceid = self.get_a_faceid()
            # self.set_parent_neighbour(self.faceid)
            start = 1
            if(len(all_objects)==1): #the first edge has to create more because it has no parent to fill the origin
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
        """Right click either link pair of activated edges
        or deletes a face and all its children"""
        global selected_edge
        if (self.mouse_inside()) and not self.active:
            selected_edge=None
            self.remove_traces()
            self.update_shape()
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
        self.polysize=current_facetype
        # delete the edges that were created by this, and its descendance
        Edge.activelist = dict()


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
