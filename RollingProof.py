import pickle
import time
from datetime import datetime
import json
import numpy
import sympy

from _libs.RollingProofImageGen import generate_stability_image, generate_image

GENERATE_PROOF = True
GENERATE_STAB = True
UPDATE_RESULTS = True
DUPLICATE_IMAGES = False

from _resources.symmetry_classes.symmetry_functions import canon_fo
from _resources.regular_faced_polyhedron_nets import all_nets
from _resources.uniform_tiling_supertiles import uniform_tilings as all_tilings

from _libs import CFOClassGenerator


def determine_n(tiling,net,polyname):#,startcase,startface,startorientation):
    # classes = CFOClassGenerator.explore_inside(tiling,net,polyname,canon_fo)
    # borders = CFOClassGenerator.explore_borders(tiling,net)
    N = sum(len(net[face])==len(tiling[cell]) and (face,o)==canon_fo(polyname,face,o)
            for face in net for cell in tiling for o in range(len(net[face])))
    classes = CFOClassGenerator.explore_inside(tiling, net, polyname, canon_fo)
    N2 = len(classes)
    # print(classes)
    # print("N=",N)
    size = max(len(elem) for elem in poly_symmetries[polyname])
    # if(size==1):
    #     input("Biggest symmetry class for %s:\n:::%i"%(polyname,size))
    # else:
    print("Biggest symmetry class for %s:\n:::%i"%(polyname,size))
    if(N2>N):
        print("[Error]Amount of classes bigger than amount of positions, N=%i<%i"%(N2,N))
    elif(N2<N):
        print("[Optimisation]Amount of classes smaller than amount of positions, N=%i<%i"%(N2,N))
    else:
    #     print("Amount of states smaller than amount of classes,
        print("[No optimisation]N=%i==%i"%(N,N2))
    return min(N+1,N2+1)

def sqrdist(tupl):
    return (tupl[0]*tupl[0])+(tupl[1]*tupl[1])

from _libs.SupertileCoordinatesGenerator import generate_supertile_coordinate_helpers

from math import copysign

def advance_on_integer(dx,dy):
    if abs(dx)>abs(dy):
        for x in range(abs(dx)+1):
            yield copysign(x,dx),int(x/dx*dy)
    else:
        for y in range(abs(dy)+1):
            yield int(y/dy*dx) ,copysign(y,dy)



def is_roller(tiling,tilingname,net,polyname):

    if not any(len(n) == len(ne) for n in tiling.values() for ne in net.values()):
        return

    borders=generate_supertile_coordinate_helpers(tiling,tilingname)
    #print(borders)
    classes, transformations, groups = CFOClassGenerator.generate_CFO_classes(tiling, net, polyname, tilingname, None)
    # print("Classes:",classes)
    # print("Transformations:",transformations)
    # print("Groups:",groups)
    """Turn class transformation into integers"""
    if transformations!=0:
        cts = set()
        ctsd = dict()
        for cfo,rotations in transformations.items():
            for rotation,endcfo in rotations.items():
                if rotation not in borders:
                    print(rotation,"does not have coordinates infos!")
                    raise PermissionError
                axiscoords = borders[rotation]
                startid = CFOClassGenerator.cfo_class_index(classes, cfo)
                endid = CFOClassGenerator.cfo_class_index(classes, endcfo)
                # if(startid==endid):
                #     print(startid,endid)
                #     print("So those are in")
                #     exit()
                cts.add((startid,endid,axiscoords))
                ctsd.setdefault(startid,set())
                ctsd[startid].add((endid,axiscoords))
        print("ctsd",ctsd)

        tiling_sides = set(len(n) for n in tiling.values())
        poly_sides = set(len(n) for n in net.values())
        incompatible = len(tiling_sides-poly_sides)
        all_data = [dict() for x in groups]
        stability = [False]*len(groups)
        has_image = False
        """For every group, explore the transformations up to N supertiles away to build symmetry vectors"""
        for groupindex,group in enumerate(groups):
            # print(groupindex,group)
            startingstate = group[0]

            if startingstate not in ctsd:
                continue
            N=len(group)
            print("Group %i/%i"%(groupindex,len(groups)),"N=",N)

            symmetries = []
            min_symmetries = []

            to_explore = [(startingstate,0,0,0)]
            explored = set()
            while(to_explore):
                st,x,y,s=to_explore.pop(0)
                #print(len(explored),N*N*N)
                #print(N,s,x,y)
                if(s>N+1):
                    continue
                next = ctsd[st]
                if (st,x,y) not in explored:
                    #if((x,y) not in filled_supertiles and CFOClassGenerator.has_all_tiles(coordinates[(x, y)],classes,tiling)):
                    #    filled_supertiles.add((x,y))
                        #if(len(filled_supertiles)==len(coordinates)):
                        #    break
                    explored.add((st,x,y))
                    for next_st,(dx,dy) in next:
                        if next_st == startingstate and (x+dx,y+dy)!=(0,0):
                            nx,ny=x+dx,y+dy
                            if([nx,ny] not in symmetries):
                                symmetries += [[nx, ny]]

                            if(len(min_symmetries)<1 and [nx,ny] not in min_symmetries):
                                min_symmetries += [[nx, ny]]
                            elif((len(min_symmetries)>0 or sqrdist((nx,ny))<=max(sqrdist(sym) for sym in min_symmetries)) and [nx,ny] not in min_symmetries):
                                min_symmetries+=[[nx,ny]]
                                #print(symmetries)

                                matrix = numpy.array(min_symmetries)
                                #print("Made",symmetries)
                                # lambdas, V = numpy.linalg.eig(matrix.T)
                                _, inds = sympy.Matrix(matrix).T.rref()
                                while((len(inds)<len(min_symmetries))):
                                    #print("Syms",symmetries)
                                    #input(str(symmetries)+" had lin dep")
                                    for size, index in reversed(sorted((sqrdist(sym), id) for id, sym in enumerate(min_symmetries))):
                                        symtest = min_symmetries[:index]+min_symmetries[index+1:]
                                        #print("Symtest",symtest)
                                        matrix = numpy.array(symtest)
                                        _, inds = sympy.Matrix(matrix).T.rref()
                                        if len(inds)==len(symtest):
                                            min_symmetries=symtest
                                            #print(symmetries)
                                            break
                                    matrix = numpy.array(min_symmetries)
                                    _, inds = sympy.Matrix(matrix).T.rref()
                                #print(symmetries)

                            #symmetries.add((x+dx,y+dy))
                        if (next_st,x+dx,y+dy) not in explored and -N<=x+dx<=N and -N<=y+dy<=N:
                            to_explore.insert(0,(next_st,x+dx,y+dy,s+1))

                    if([-1,0]in min_symmetries or [1,0] in min_symmetries)and([0,1] in min_symmetries or [0,-1] in min_symmetries):
                        print("Break early found minimal symmetry")
                        to_explore = []
                        break
            # print("Symmetries:",symmetries)
            print("Min Symmetries:",min_symmetries)
            all_data[groupindex]["symmetry_vectors"]=min_symmetries
            if(len(min_symmetries)<=1):
                print("Not enough symmetries to cover the plane")
                if len(min_symmetries)==1:
                    all_data[groupindex]["type"]="band"
                else:
                    all_data[groupindex]["type"]="area"
                continue
            """mx = min(x for (x,y) in min_symmetries+[(0,0)])
            my = min(y for (x,y) in min_symmetries+[(0,0)])
            Mx = max(x for (x,y) in min_symmetries+[(0,0)])
            My = max(y for (x,y) in min_symmetries+[(0,0)])
            N = max(max(abs(x),abs(y)) for (x,y) in min_symmetries)+1
            coordinates = {(i, j): set() for i in range(mx, Mx+1, 1) for j in range(my, My+1, 1)}"""
            filled_supertiles = set()
            to_explore = [(startingstate,0,0)]
            explored = set()
            """Using the symmetry vectors, fill a N*2 space"""
            def between(border1, border2, value):
                borders = min(border1, border2)
                borderm = max(border1, border2)
                return borders<=value<=borderm

            def lines_to_fill(points, y):
                xes = []
                for i in range(4):
                    segment = points[i], points[(i+1)%4]
                    if(between(segment[0][1],segment[1][1],y)):
                        if(segment[1][1]-segment[0][1]==0):
                            #point = min(segment[0][0],segment[1][0])
                            xes.append(segment[0][0])
                            xes.append(segment[1][0])
                        else:
                            point = int(round((y-segment[0][1])/(segment[1][1]-segment[0][1])*(segment[1][0]-segment[0][0])))
                            xes.append(point)
                print(xes)
                xes=sorted(set(xes))
                if(len(xes)!=2):
                    print(xes,"too many or too few points of comparison")
                    xes=2*xes

                res = [(x,y) for x in range(xes[0],xes[-1],1)]
                return res

            def find_opposite_border(point, points, vec1, vec2):
                for (i,j) in (-1,0),(1,0),(-1,-1),(1,1),(1,-1),(-1,1),(0,1),(0,-1):
                    checkpoint = point[0]+vec1[0]*i+vec2[0]*j, point[1]+vec1[1]*i+vec2[1]*j
                    if checkpoint in points:
                        yield checkpoint
                return None

            def frange(start,end,step):
                while start<end:
                    yield(start)
                    start+=step
            def fill_parallelogram_opt(vec1, vec2):
                #http://alienryderflex.com/polygon_fill/
                points = (0.5,0.5),(vec1[0]+0.5,vec1[1]+0.5),(vec1[0]+vec2[0]+0.5,vec1[1]+vec2[1]+0.5), (vec2[0]+0.5,vec2[1]+0.5)
                points = (0,0),vec1,(vec1[0]+vec2[0],vec1[1]+vec2[1]), vec2
                points = (-0.5,-0.5),(vec1[0]-0.5,vec1[1]-0.5),(vec1[0]+vec2[0]-0.5,vec1[1]+vec2[1]-0.5), (vec2[0]-0.5,vec2[1]-0.5)
                print(points)
                miny = min(y for x,y in points)
                maxy = max(y for x,y in points)
                minx = min(x for x,y in points)
                maxx = max(x for x,y in points)
                coordinates = set()
                for y in frange(miny,maxy+1,1):
                    nodesx = list()
                    corners = 4;
                    for i in range(corners):
                        j = (i-1)%corners
                        if(points[i][1]<y and points[j][1]>=y or points[j][1]<y and points[i][1]>=y):
                            nodesx.append(int(points[i][0]+(y-points[i][1])/(points[j][1]-points[i][1])*(points[j][0]-points[i][0])))
                    nodesx.sort()
                    print(nodesx)
                    for n in range(0,len(nodesx),2):
                        for x in frange(nodesx[n],nodesx[n+1]+1,1):
                            coordinates.add((int(x),int(y)))
                print("Filled coordinates:",coordinates)
                return coordinates
            from _libs.GeometryFunctions import ptAngle,ptAdd
            def remove_outsiders(points,vec1,vec2):
                pc = (0,0)
                if(ptAngle(vec1,pc,vec2)>0):
                    corners = vec1,pc,vec2,ptAdd(vec1,vec2)
                else:
                    corners = vec2,pc,vec1,ptAdd(vec1,vec2)
                to_remove = set()
                for point in points:
                    if point in corners:
                        continue
                    for i in range(len(corners)):
                        j=(i+1)%len(corners)
                        if(ptAngle(corners[i], corners[j], point))<0:
                            to_remove.add(point)
                            break
                return points-to_remove


            def fill_parallelogram(vec1, vec2):
                points = (0,0),vec1,(vec1[0]+vec2[0],vec1[1]+vec2[1]), vec2
                # points = (0,0),vec1, vec2
                miny = min(y for x,y in points)
                maxy = max(y for x,y in points)
                minx = min(x for x,y in points)
                maxx = max(x for x,y in points)
                meanx = (vec1[0]+vec2[0])/4
                meany = (vec1[1]+vec2[1])/4
                coordinates = {(i,j) for i in range(minx, maxx + 1, 1) for j in range(miny, maxy + 1, 1)}
                return coordinates
                # coordinates = set()
                # for y in range(miny, maxy+1, 1):
                #     for pos in lines_to_fill(points,y):
                #         coordinates.add(pos)
                #cleanup
                allcoords = list(coordinates)
                index=0
                to_remove = set()
                while index<len(allcoords):
                    c1=allcoords[index]
                    for c2 in find_opposite_border(c1,allcoords,vec1,vec2):
                        index2 = allcoords.index(c2)
                        # print(sqrdist(c1)>sqrdist(c2),sqrdist(c1),sqrdist(c2))
                        d1,d2 = sqrdist((c1[0]-meanx,c1[1]-meany)),sqrdist((c2[0]-meanx,c2[1]-meany))
                        if(d1==d2):
                            if(sqrdist(c1)>sqrdist(c2)):
                                to_remove.add(c1)
                                print("Removing",c1,sqrdist(c1),"over",c2,sqrdist(c2))
                            else:
                                to_remove.add(c2)
                                print("Removing",c2,sqrdist(c2),"over",c1,sqrdist(c1))
                            # to_remove.add(max(c1,c2))
                            # print("Removing",max(c1,c2)," max of",c1,c2,sqrdist(c1),sqrdist(c2))
                        elif(d1>d2):
                            to_remove.add(c1)
                            print("Removing",c1,sqrdist(c1),"over",c2,sqrdist(c2))
                        else:
                            to_remove.add(c2)
                            print("Removing",c2,sqrdist(c2),"over",c1,sqrdist(c1))
                            # allcoords[index],allcoords[index2]=allcoords[index2],allcoords[index]
                            # c1=allcoords[index]
                        # print("Removing",allcoords[index2],sqrdist(allcoords[index2]),"over",allcoords[index],sqrdist(allcoords[index]))
                        # allcoords.pop(index2)
                    index+=1
                print(coordinates)
                print(coordinates-to_remove)
                print(len(coordinates),">?",len(coordinates-to_remove))
                # input(str((len(coordinates),">?",len(allcoords))))
                # exit()

                coordinates=coordinates-to_remove
                coordinates.add(tuple(vec1))
                coordinates.add(tuple(vec2))
                coordinates.add((0,0))
                return coordinates

            def explore_parallelogram(vec1,vec2, rules, to_explore):
                points = fill_parallelogram(vec1, vec2)
                points = remove_outsiders(points,vec1,vec2)
                print("Points to fill:",points)
                explored_states = {point:set() for point in points}
                startingpoint = to_explore[0]
                for nx,ny in find_opposite_border(startingpoint[1:],points, vec1,vec2):
                    to_explore.append((startingpoint[0], nx,ny))
                # symmetrypoint =
                # if(symmetrypoint):
                #     to_explore.append((startingpoint[0],symmetrypoint[0],symmetrypoint[1]))

                while (to_explore):
                    print(to_explore)
                    st, x, y = to_explore.pop(0)
                    next = rules[st]
                    if st not in explored_states[(x, y)]:
                        # print(st,x,y)
                        explored_states[(x, y)].add(st)
                        if ((x, y) not in filled_supertiles and CFOClassGenerator.has_all_tiles(explored_states[(x, y)],
                                                                                                classes, tiling)):
                            filled_supertiles.add((x, y))
                            print("\r", len(filled_supertiles), "/", len(explored_states), end="")

                        for next_st, (dx, dy) in list(next):
                            nx = x + dx
                            ny = y + dy
                            if(nx,ny) in explored_states and next_st not in explored_states[(nx,ny)] and (next_st,nx,ny) not in to_explore:
                                to_explore.insert(0, (next_st, nx, ny))
                            for nx, ny in find_opposite_border((nx,ny),points, vec1,vec2):
                                if (nx, ny) in explored_states and next_st not in explored_states[(nx, ny)] and (
                                next_st, nx, ny) not in to_explore:
                                    to_explore.insert(0, (next_st, nx, ny))
                return explored_states
            explored_states = explore_parallelogram(min_symmetries[0],min_symmetries[1], ctsd, to_explore)
            """After the exploration, gather results"""
            print()
            is_roller=True

            all_data[groupindex]["exploration"]=explored_states
            for coord,states in explored_states.items():
                if not(CFOClassGenerator.has_all_tiles(states, classes, tiling)):
                    is_roller = False
            if(is_roller):
                print(tilingname,polyname,"%i/%i"%(groupindex+1,len(groups)),"is a roller in -%i:%i"%(N,N))
                stability[groupindex]=True
                type = "roller"
                all_data[groupindex]["type"]= type
            else:
                is_quasi_roller = True
                for coord,states in explored_states.items():
                    if not(CFOClassGenerator.has_all_compatible_tiles(states, classes, tiling, net)):
                        is_quasi_roller = False
                stability[groupindex]=is_quasi_roller
                print(tilingname,polyname,"%i/%i"%(groupindex+1,len(groups)),"is not a roller in -%i:%i"%(N,N))
                if(is_quasi_roller):
                    type="quasi_roller"
                    all_data[groupindex]["type"]= type
                else:
                    type="non-roller"
                    all_data[groupindex]["type"]= "hollow"
                if(N):
                    graph = [[bool((i, j) in filled_supertiles)+bool(explored_states[(i,j)]) for i in range(-N//2, N//2 + 1, 1) if (i,j) in explored_states] for j in range(-N//2, N//2+1, 1)]
                    CFOClassGenerator.prettyprint_012(graph)
                    #input()
            if(GENERATE_PROOF):
                if not any(stability[:groupindex]) or DUPLICATE_IMAGES:
                    generate_image(tiling, net, tilingname, polyname, classes, group, groups, borders, min_symmetries, explored_states, type)
        """Done with all the groups"""
        is_stable = not False in stability
        results = dict()
        results["all_data"]=all_data
        results["stability"]=is_stable
        if True in stability and not incompatible:
            results["type"]="roller"
        elif True in stability and incompatible:
            results["type"]="quasi_roller"
        elif "hollow" in (result["type"] for result in all_data if "type" in result.keys()):
            results["type"]="hollow"
        elif "band" in (result["type"] for result in all_data if "type" in result.keys()):
            results["type"]="band"
        elif "area" in (result["type"] for result in all_data if "type" in result.keys()):
            results["type"]="area"
        elif len(groups)==0:
            results["type"]="area"
        else:
            results["type"]="unknown"
        #for now, let's ignore hollow plane that are not quasi?
        results["polyhedron"]=polyname
        results["tiling"]=tilingname

        """Stability tiles"""
        #for every tile
        #it every face and orientation on it are in a roller group
        #then it is a stable position
        #so it's more like: for every group:
        #   if it has a tile it's representative of that tile's stability
        #for every tile:
        #   if every representative is roller, then the tile is stable

        #[pos][c] is stable if it is equal to maxfo[c]
        if True in stability:
            min_size_area = \
            min((len(res["exploration"]), index) for index, res in enumerate(all_data) if "exploration" in res.keys())[
                1]
            fill_area = {pos: [0 for cell in tiling] for pos in all_data[min_size_area]["exploration"]}
            maxfo = [sum(len(n) for n in net.values() if len(n) == len(neigh)) for tile, neigh in
                     sorted(tiling.items())]
            cell_stability = [0 for cell in tiling]
            for index,group in enumerate(groups):
                for clas in group:
                    for c,f,o in classes[clas]:
                        cell_stability[c] += stability[index]
            for index, result in enumerate(all_data):
                if "exploration" in result.keys():
                    for pos, group in result["exploration"].items():
                        for clas in group:
                            for c, f, o in classes[clas]:
                                try:
                                    fill_area[pos][c] += stability[index]
                                except KeyError:
                                    pass


            stable_spots = {pos:[counter == maxfo[cell] for cell,counter in enumerate(celldata)] for pos,celldata in fill_area.items()}
            stable_spots = {pos:[cell_stability[cell]==maxfo[cell] and maxfo[cell]!=0 for cell in range(len(tiling))] for pos in fill_area}
            type=("roller","quasi-roller")[bool(incompatible)]
            if(GENERATE_STAB):
                generate_stability_image(tilingname, polyname, tiling, net, borders, type, stable_spots)

            results["stability"]=all(cell_stability[cell]==maxfo[cell] for cell in range(len(tiling)))

            results["CFO_classes"]=classes
            results["CFO_class_groups"]=groups
            results["class_to_supertile_coordinates"]=ctsd
        return results
    else:
        if(classes):
            results = {"type":"area"}
            return results

    #else no cmpatibility

start_time = time.time()
def timer():
    global start_time
    old_time = start_time
    start_time=time.time()
    return start_time-old_time
def timerstring():
    s=str(timer())
    if("." in s):
        s=s[:s.index(".")+2]
    return s.ljust(5)+"s "
def timestamp():
    return datetime.now().strftime("%H:%M:%S")

if __name__ == "__main__":
    timer()
    print(timestamp())
    rollers = list()
    quasirollers = list()
    rollersdata = dict()
    all_results = dict()
    from _resources.symmetry_classes.poly_symmetries import poly_symmetries
    import _resources.symmetry_classes.symmetry_functions
    def canon_fo(polyname, face, orientation):
        return _resources.symmetry_classes.symmetry_functions.canon_fo(polyname, face, orientation, poly_symmetries)


    # for tilingname, polyname in [["3^6","j8"]]:
#     for tilingname, polyname in [
# ["3^6;3^2x4x3x4", "cuboctahedron"],
# ["3^6;3^2x6^2", "truncated_tetrahedron"],
# ["(3^3x4^2;3^2x4x3x4)1", "cuboctahedron"],
# ["(3^3x4^2;3^2x4x3x4)1", "j1"],
# ["(3^3x4^2;3^2x4x3x4)1", "j27"]
#         ]:

    # showcase = [("3unhv48 (3^6;3^2x4x3x4;3^2x4x3x4)", "cuboctahedron")]
    for tilingname, polyname in ((t,p) for t in all_tilings.keys() for p in all_nets.keys()):
    # for tilingname, polyname in [["3^6;3^2x4x3x4","j89"]]:
    # for tilingname, polyname in [["3^2x4x3x4;3x4x6x4","j29"]]:
    # for tilingname, polyname in [["4^4","cube"]]:
        tiling = all_tilings[tilingname]
        net = all_nets[polyname]
        print(tilingname,polyname)
        results = is_roller(tiling,tilingname,net,polyname)
        all_results[(tilingname,polyname)]=results
        if(results==None):
            rollersdata[(tilingname,polyname)]=" "
        elif(results["type"]=="roller"):
            if((tilingname,polyname) not in rollers):
                rollers.append((tilingname,polyname))
            if results["stability"]:
                rollersdata[(tilingname,polyname)]="SPR"
            else:
                rollersdata[(tilingname,polyname)]="PR"
        elif(results["type"]=="quasi_roller"):
            quasirollers.append((tilingname,polyname))
            if results["stability"]:
                rollersdata[(tilingname,polyname)]="SQPR"
            else:
                rollersdata[(tilingname,polyname)]="QPR"
        elif(results["type"]=="hollow"):
            rollersdata[(tilingname,polyname)]="HPR"
        elif(results["type"]=="band"):
            rollersdata[(tilingname,polyname)]="br"
        elif(results["type"]=="area"):
            rollersdata[(tilingname,polyname)]="ar"
        else:
            rollersdata[(tilingname,polyname)]="x"
    print()
    if(UPDATE_RESULTS):
        with open('rolling_results.pickle', 'wb') as handle:
            pickle.dump(all_results, handle, protocol=pickle.HIGHEST_PROTOCOL)
        with open('rollersdata.pickle', 'wb') as handle:
            pickle.dump((rollersdata,tuple(all_tilings.keys()),tuple(all_nets.keys())), handle, protocol=pickle.HIGHEST_PROTOCOL)
    #output_table(all_nets,all_tilings,rollersdata)
    json_object = json.dumps(all_results, indent=4)
    with("rolling_results.json", "w") as f:
        f.write(json_object)
    for tilingname,polyname in rollers:
        print(tilingname,polyname)
    print(len(rollers))
    print("Tilings:",len(all_tilings))
    print(timestamp())
    print("Total duration:",timerstring())