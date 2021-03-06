MODE="pygame"
from Point import Point
def centerpoint(points):
    mx = 0
    my = 0
    for x, y in points:
        mx += x
        my += y
    return (int(round(mx / len(points))), int(round(my / len(points))))

if(MODE=="pygame"):
    import pygame

    colors = tuple((x, y, z) for z in range(0, 255, 128) for y in range(0, 255, 128) for x in range(0, 255, 128))


    def initialise_drawing(w,h):
        global screen, shapes, s, curs, WIDTH, HEIGHT, above
        WIDTH=w ; HEIGHT=h
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
        shapes = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # objects that will be blitted first
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # working surface
        curs = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # objects that will be blitted over the rest
        above = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 0))
        shapes.fill((255,255,255,255))
    def polygon_shape(points,color,alpha=1,outline=False):
        if(isinstance(color,int)):
            color=colors[color%len(colors)]
        s.fill((0, 0, 0, 0))
        #print(color + (int(round(256*alpha)),))
        color_alpha = color + (int(alpha*255),)
        pygame.draw.polygon(s, color_alpha, [(p.x, p.y) for p in points])

        if(outline):
            pygame.draw.lines(s, (0,0,0), True, [(p.x, p.y) for p in points])
        ppoint = centerpoint(points[:2]*20+points)
        pygame.draw.circle(s, (255,255,255),ppoint,1)
        #pygame.draw.line(s,(255,128,128),points[0].as_tuple(),points[1].as_tuple(),2)
        shapes.blit(s, (0, 0))

    def polygon_cursor(points, color, alpha=1, outline=False):
        if (isinstance(color, int)):
            color = colors[color % len(colors)]
        s.fill((0, 0, 0, 0))
        #print(color + (int(round(256 * alpha)),))
        color_alpha = color + (int(alpha * 255),)
        pygame.draw.polygon(s, color_alpha, [(p.x, p.y) for p in points])
        if(outline):
            pygame.draw.lines(s, (0,0,0), True, [(p.x, p.y) for p in points])
        curs.blit(s, (0, 0))

    def create_orientation_data(face_id,poly):
        #return face's order in the list of similar shaped faces
        #and the number of similar shaped faces
        face_id=face_id%len(poly) #Python: returns positive modulo
        shape = len(poly[face_id])
        count=0
        max_count=0
        for key in poly:
            if(len(poly[key])==shape):
                max_count+=1
        for key in sorted(poly.keys()):
            if(key==face_id):
                return count, max_count #Always reached
            elif(len(poly[key])==shape):
                count+=1
        return None

    from colorsys import hls_to_rgb

    def polygon_orientation(points,orientation,face_count,max_count,outline=0,case_count=0):
        #Draw a little triangles to show the reached orientation on the face.
        line = (points+points)[orientation:orientation+2]
        print(line,orientation,orientation+2)
        perpendicular = Point(centerpoint(points))-centerpoint(line)
        tangent=(line[1]-line[0])/max_count
        perpendicular=perpendicular/perpendicular.length()*tangent.length()
        perp=perpendicular.clone()/tangent.length()
        #Match the border angle
        if(len(points)==4):
            perpendicular/=2 #/(tan(45)/2)
        elif(len(points)==3):
            perpendicular/=(3**0.5)*2 #/(tan(30)/2)
        elif(len(points)==6):
            perpendicular/=2/(3**0.5) #/(tan(60)/2)
        if(perpendicular.length()<4):
            perpendicular/=perpendicular.length()/4
        tri = line[0]+tangent*face_count,line[0]+tangent*(face_count+1)
        tri += Point(centerpoint(tri))+perpendicular,


        c = face_count/(max_count)
        color = tuple(int(x*255) for x in hls_to_rgb(c,0.5,1))
        print(color)

        pygame.draw.polygon(above, color, [(p.x, p.y) for p in tri])



        #quad = line[0]+tangent*face_count,line[0]+tangent*(face_count+1)
        #quad = quad[0], quad[1], quad[1]+perp, quad[0]+perp

        if(outline==1):
            p3 = Point(centerpoint(points))
            tri2 = tri[:2]+(p3,)
            print(tri2)
            pygame.draw.polygon(above, color, [(p.x, p.y) for p in tri2])
            pygame.draw.lines(above, (0,0,0),0, [(p.x, p.y) for p in (tri2+tri2)[1:4]])
            color1 = tuple(int(x*255) for x in hls_to_rgb(c,0.45,1))
            #color2 = tuple(int(x*255) for x in hls_to_rgb((c+0.5)%1,0.5,1))
            #pygame.draw.polygon(above, (0,0,0), [(p.x, p.y) for p in quad])
            #pygame.draw.line(above,(255,255,255),tri[0].as_tuple(),tri[1].as_tuple())
            #pygame.draw.lines(above,color2,0,[(p.x, p.y) for p in tri[1:]+tri[:1]],2)
            #pygame.draw.circle(shapes,color,centerpoint(points),3)
            s.fill((0,0,0,0))
            pygame.draw.polygon(s, color1, [(p.x, p.y) for p in points])
            text = pygame.font.SysFont(None, int((points[1]-points[0]).length()/2)).render(str(case_count), True, (0,0,0))
            center=centerpoint(points)
            s.blit(text, (center[0] - text.get_width() / 2, center[1] - text.get_height() / 2))
            pygame.draw.lines(above, (0,0,0),1, [(p.x, p.y) for p in points],2)
            s.blit(above, (0,0))
            above.blit(s, (0,0))
        #else:
        #    pygame.draw.polygon(shapes, color, [(p.x, p.y) for p in points])

        if(outline==2):
            #pygame.draw.line(above,(0,0,0),tri[0].as_tuple(),tri[1].as_tuple())
            pygame.draw.lines(above,(0,0,0),0,[(p.x, p.y) for p in tri[1:]+tri[:1]],1)
            #pygame.draw.polygon(above, (255,255,255), [(p.x, p.y) for p in quad])
        #pygame.draw.lines(above, (0,0,255,255), True, [(p.x, p.y) for p in tri])
        case_color =  tuple(int(x*255) for x in hls_to_rgb(case_count/(max_count),0.7,0.7))
        pygame.draw.polygon(shapes, case_color, [(p.x, p.y) for p in points])
        text = pygame.font.SysFont(None, int((points[1]-points[0]).length()/2)).render(str(case_count), True, (0,0,0))
        center=centerpoint(points)
        shapes.blit(text, (center[0] - text.get_width() / 2, center[1] - text.get_height() / 2))


        shapes.blit(above, (0, 0))


    def empty_cursor():
        curs.fill((0,0,0,0))

    def empty_shapes():
        shapes.fill((0,0,0,0))

    def text_center(text,x,y,color,size):
        if(isinstance(color,int)):
            color=colors[color%len(colors)]
        text = pygame.font.SysFont(None, size).render(text, True, color)
        shapes.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))



    def refresh():
        screen.fill((255,255,255))
        screen.blit(shapes,(0,0))
        screen.blit(curs,(0,0))
        screen.blit(above,(0,0))
        pygame.display.update()
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                exit()
        #pygame.time.Clock().tick(120)

    def loop():
        clock = pygame.time.Clock()
        running=True
        print("Looping")
        while running:
            #print(running)
            clock.tick(10)
            #window.fill((255, 255, 255))
            #pygame.display.flip()
            for e in pygame.event.get():
                if e.type == pygame.MOUSEBUTTONDOWN:
                    print("Mouse!")
                if e.type == pygame.QUIT:
                    running = False
                    print("Quit!",flush=True)


    def save_screen(filename):
        pygame.image.save(screen, filename)
if(MODE=="tkinter"):
    pass