import pygame
from GeometryFunctions import xgon, centerpoint
try:
    from exploration_results.unusedfaces import unusedfaces as unusedfacesdict
except:
    unusedfacesdict = dict()
def convertToTuple(points):
    return  tuple((int(x), int(y)) for x,y in points)
pygame.init()
def draw_polynet(surf,surface2,polyhedron,startface,startorientation,p1,p2,tilingname,polyname):
    unusedfaces = unusedfacesdict.get((tilingname,polyname),None) or []
    visited_faces = list()
    visits = [(startface,startorientation,p1,p2)]
    while(visits):
        face, orientation, p1, p2 = visits.pop()
        if(face in visited_faces):
            continue
        visited_faces.append(face)
        face_poly = xgon(len(polyhedron[face]),p1,p2)
        face_poly = face_poly[orientation:]+face_poly[:orientation] #align
        textsize = int(((p1.x-p2.x)**2+(p1.y-p2.y)**2)**0.5/2)
        center = centerpoint(face_poly)
        x,y = int(center[0]),int(center[1])
        if(face not in unusedfaces):
            color1 = (0,0,255)
            color2 = (0,0,128)
        else:
            color1 = (255,0,0)
            color2 = (128,0,0)
        if(face!=startface):
            pygame.draw.circle(surface2, color1,(x,y), int(textsize/2))
            surf.blit(surface2, (0, 0))
            pygame.draw.polygon(surface2, color1,convertToTuple(face_poly), 0)
            surf.blit(surface2, (0, 0))
            surface2.fill((0,0,0,0))
        pygame.draw.polygon(surf, color2,convertToTuple(face_poly), 1)
        text = pygame.font.SysFont(None, textsize).render(str(face), True, (0,0,0))
        surf.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))

        for index,nextface in enumerate(polyhedron[face]):
            face_shift = polyhedron[nextface].index(face)
            # Create a stub nextface at the edge of the current face
            nextface_stub = xgon(len(polyhedron[nextface]), face_poly[(index+1)%len(face_poly)], face_poly[index])
            # Reorient it
            pa, pb = nextface_stub[-face_shift], nextface_stub[(-face_shift+1)%len(nextface_stub)]
            orientation = polyhedron[nextface].index(face)
            visits.insert(0,(nextface,0,pa,pb))

def draw_background(surf,grid):
    for points, cell in grid.values():
        # print(points)
        pygame.draw.polygon(surf, (0,0,0), convertToTuple(points), 2)

def draw_polygon(surf,color,points,width):
    pygame.draw.polygon(surf, color, convertToTuple(points), width)

def wait_for_input():
    clock = pygame.time.Clock()
    running=True
    while running:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            break;
        if(len(pygame.event.get())==0):
            clock.tick(20)
        for e in pygame.event.get():
            if e.type == pygame.MOUSEBUTTONDOWN:
                #print("Resume with mouse",e.type,flush=True)
                running = False
            if e.type == pygame.KEYDOWN:
                running = False
                #print("Resume with key",e.key,flush=True)
            if e.type == pygame.QUIT:
                running = False
                print("Quit!",flush=True)
                pygame.quit()
def refresh():
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()

def draw_answer(filename,tilingname,polyname,visits,grid,polyhedron,p1,p2,startface,startorientation,w,h):
    #no need for startcase because grid and p1,p2 is enough
    surf = pygame.Surface((w,h))
    surf.fill((255,255,255))
    face = xgon(len(polyhedron[startface]),p1,p2)
    draw_background(surf,grid)
    surface2 = pygame.Surface((w,h), pygame.SRCALPHA)
    surface2.set_colorkey((0, 0, 0))
    surface2.set_alpha(100)

    pygame.draw.polygon(surf, (255,255,0), convertToTuple(face), 0)
    draw_polynet(surf,surface2,polyhedron,startface,startorientation,p1,p2,tilingname, polyname)

    surface2.set_alpha(255)
    text = pygame.font.SysFont(None, 30).render(tilingname+" with "+polyname, True, (0, 0, 0))
    pygame.draw.rect(surf, (255,255,255),(100+25+50,100+25+50,text.get_width()+2,text.get_height()+2))
    surf.blit(text, (101+25+50,101+25+50))
    # sub = screen.subsurface(rect)
    pygame.image.save(surf.subsurface([100+25+50,100+25+50,600-25,600-25]),filename)

if __name__ == "__main__":
    pass