#Shows a partial net of the poly to click on to expand
#Once fully expanded, prints the partial tiling (dictionary)
#And takes a screenshot
#This helps rebuilding the tessellation net from an image
#Because otherwise it's hard to match the orientation of the faces

#main creates edges→loop
#fully expanded: second_main prints the net and takes a picture→return to main
#[Enter]→go to next polyhedron
import pprint
import pygame
from GeometryFunctions import *
from PolyAndTessNets import *

pp = pprint.PrettyPrinter(indent=4)
WIDTH = 800
HEIGHT = 800
EDGE_SIZE = 30
p1 = Point(300, 300)
p2 = Point(300+EDGE_SIZE, 300)
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
                    elif(e.button==4):
                        #wheel_up
                        pass
                    elif(e.button==5):
                        #wheel down
                        pass
            if e.type== pygame.KEYDOWN and e.key == pygame.K_RETURN:
                all_objects = []
                running=False
                #jump to step 2

            if e.type == pygame.QUIT:
                running = False
                print("Quit!", flush=True)
                exit()

class DummyParent():
    def __init__(self):
        self.favorite = None

class Edge():
    depth = 0
    numbering = set()
    shapes_functions = (None, None, None, triangle, square, None, hexagon, None, octagon, None, None, None, dodecagon)
    select_neighbour = None

    def get_a_faceid(self):
        number = 0
        while number in Edge.numbering:
            number+=1
            if(number not in Edge.numbering):
                Edge.numbering.add(number)
                return number
    def forget_faceid(self):
        Edge.numbering.remove(self.faceid)
    def is_neighbour(self):
       return self.other!=None
    def get_unique_p(self,other_p=0):
        self.pcount = max(self.pcount+1,other_p)
        return self.pcount
    def same_position(self,other):
        return distance(floatcenterpoint((self.coords)),floatcenterpoint(other.coords))<2
    def set_link(self,other):
        self.other = other
        other.other=self
        if(self.parent==other.parent and self.parent!=None):
            #self link
            #functions also when linking to same edge
            p = self.parent.get_unique_p()
            other.set_parent_neighbour(self.parent.faceid-p*self.parent.nextshape)
            self.set_parent_neighbour(self.parent.faceid+p*self.parent.nextshape)
        elif(self.same_position(other)):
            #internal link
            self.set_parent_neighbour(other.parent.faceid)
            other.set_parent_neighbour(self.parent.faceid)
        else:
            #external link
            p = self.parent.get_unique_p(other.parent.get_unique_p())
            other.pcount = p
            self.set_parent_neighbour(other.parent.faceid+p*other.parent.nextshape)
            other.set_parent_neighbour(self.parent.faceid+p*self.parent.nextshape)


        self.set_parent_neighbour(self.parent.faceid)
        other.set_parent_neighbour(other.parent.faceid)
    def __init__(self, coords, polysize, parent):
        self.pcount=0 #as face
        self.p = -1 #as pairing edge
        self.parent = parent
        self.other=None
        self.children=[]
        self.active = True
        self.coords = coords #pair
        self.p1, self.p2 = coords
        self.faceid=None
        self.nextshape = polysize
        shape = Edge.shapes_functions[self.nextshape]
        self.points = shape(self.p1, self.p2)
        self.neighbours = [None]*self.nextshape
        try:
            self.neighbours[0]=parent.faceid
        except:
            pass
        for edge in all_objects:
            if(edge!=self and self.same_position(edge)):
                self
                break


        #check with all the edges if same coords as this: must be internal neighbour
        self.draw()
    def refresh_shape(self,polysize):
        self.nextshape=polysize
        shape = Edge.shapes_functions[self.nextshape]
        self.points = shape(self.p1, self.p2)

    def draw(self):
        if(self.active):
            surf = get_surface(Edge.depth)
            pygame.draw.circle(surf, (0, 0, 0), self.p1.as_tuple(), 2)
            pygame.draw.circle(surf, (0, 0, 0), self.p2.as_tuple(), 2)
            pygame.draw.line(surf, (0, 0, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)
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

            draw_text(1,str(self.faceid),*center,(0,0,0),EDGE_SIZE/2)


    def draw_cursor(self):
        surf = get_surface(2)
        if(self.active):
            if True: #self.is_parent_favorite(): #self.face1 not in visitedfaces:
                pygame.draw.line(surf, (0, 255, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)
                if (self.mouse_inside()):
                    pygame.draw.polygon(surf, (0, 128, 255, 128), [(p.x, p.y) for p in self.points])
                    center = centerpoint(self.points)
                    border = centerpoint((self.p1.as_tuple(), self.p2.as_tuple()))
                    #pygame.draw.line(surf, (250, 250, 250), border, center, 3)
                    #draw_text(2,str(self.faceid),*center,(0,0,0),EDGE_SIZE/2)
                else:
                    center = centerpoint(self.points)
                    border = centerpoint((self.p1.as_tuple(), self.p2.as_tuple()))
                    #pygame.draw.line(surf, (250, 250, 250), border, center, 3)
                    draw_text(2,str(self.faceid),*center,(192,192,192),EDGE_SIZE/2)
                    draw_polygon(1,self.points,(0,0,0),0.1,0)
                    #pygame.draw.polygon(surf, (0, 0, 0, 16), [(p.x, p.y) for p in self.points])
            #else:
            #    pygame.draw.line(surf, (0, 0, 0), self.p1.as_tuple(), self.p2.as_tuple(), 1)

    def set_parent_neighbour(self,faceid):
        try:
            index = self.parent.children.index(self)
            self.parent.neighbours[index]=faceid
        except:
            pass

    def mouse_inside(self):
        mx, my = pygame.mouse.get_pos()
        return is_inside(Point(mx, my), self.points)

    def mouse_click(self):
        if (self.mouse_inside() and self.active):# and self.face1 not in visitedfaces):
            print(visitededges)
            self.active=False
            self.faceid = self.get_a_faceid()
            self.set_parent_neighbour(self.faceid)
            for i in range(1,len(self.points)):
                pa = self.points[i]
                pb = self.points[(i+1)%len(self.points)]
                #must reverse order since we want the shape to continue outside
                ed=Edge((pb, pa), self.nextshape, self)
                all_objects.append(ed)
                self.children.append(ed)
            #if(len(visitedfaces)==len(self.poly)):
            #    second_main()
    def mouse_right_click(self):
        if (self.mouse_inside()) and not self.active:
            self.remove_traces()
        elif(self.mouse_inside()) and self.active:
            pass
            #link stuff by pairs
    def remove_traces(self):
        if(self.other != None):
            self.other.other = None
            self.other.set_parent_neighbour(None)
            self.other=None
            self.set_parent_neighbour(None)
        if(not self.active):
            for ed in self.children:
                ed.remove_traces()
                all_objects.remove(ed)
        self.children=[]
        self.favorite=None
        self.parent.favorite=None
        self.active=True
            #delete the edges that were created by this, and its descendance

cubotahedron = {



}

if __name__ == "__main__":
    for working_poly in ["octahedron","cube","j89","j90","j12","j13","j17","j51","j84"]:
        global polyname
        polyname = working_poly
        poly = polys[working_poly]
        initialise_drawing()
        #pygame.scrap.init()
        #pygame.scrap.put(pygame.SCRAP_BMP,pygame.surfarray.array3d(screen))
        visitedfaces=set()
        visitededges=set()
        dummy=DummyParent()
        all_objects.append(Edge((p1, p2), poly, 0, poly[0][0],dummy))
        all_objects.append(Edge((p2, p1), poly, poly[0][0], 0,dummy))
        refresh()
        print(working_poly)
        loop()
