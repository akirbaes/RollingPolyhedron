MODE="pygame"

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
        global screen, shapes, s, curs, WIDTH, HEIGHT
        WIDTH=w ; HEIGHT=h
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
        shapes = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # objects that will be blitted first
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # working surface
        curs = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # objects that will be blitted over the rest
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
        ppoint = centerpoint(points+4*(points[0],))
        pygame.draw.circle(s, (0,0,0),ppoint,2)
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

    def empty_cursor():
        curs.fill((0,0,0,0))

    def empty_shapes():
        shapes.fill((0,0,0,0))

    def text_center(text,x,y,color,size):
        if(isinstance(color,int)):
            color=colors[color%len(colors)]
        s.fill((0,0,0,0))
        text = pygame.font.SysFont(None, size).render(text, True, color)
        shapes.blit(text, (x - text.get_width() / 2, y - text.get_height() / 2))



    def refresh():
        screen.fill((255,255,255))
        screen.blit(shapes,(0,0))
        screen.blit(curs,(0,0))
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
if(MODE=="tkinter"):
    pass