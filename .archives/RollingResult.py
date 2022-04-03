"""DEV NOTE: unused class that was supposed to contain the result data of an exploration
Instead I'm using a dictionary"""

from dataclasses import dataclass
from _resources.tiling_dicts.archimedean_tilings import archimedean_tilings
from _resources.tiling_dicts import platonic_tilings
from _resources.tiling_dicts.isogonal_tilings import biisogonal_tilings
from _resources.TessellationPolyhedronAndTilings import net_tessellations

import os
import pickle


@dataclass
class RollingResult:
    tilingname: str
    tiling: dict
    polyname: str
    poly: dict
    startcell: int
    startface: int
    startorientation: int
    visited_places: dict
    mapping: dict
    bigarea: tuple
    smallarea: tuple
    exploration_type: int

    exploration_types = ["optimised", "allfaces", "isohedral"]

    def get_exploration_type(self):
        return RollingResult.exploration_types[self.exploration_type]
    def is_tessellation_polyhedron(self):
        return self.polyname==self.tilingname
    # def poly_id(self):
    #     polyname = self.polyname
    #     tess = self.is_tessellation_polyhedron()
    #     if (tess):
    #         polist = list(tessellation_polyhedrons.values())
    #         return "TP" + (str(polist.index(polyname)).zfill(2))
    #     else:
    #         polist = list(*d.values() for d in (plato_archi_nets, johnson_nets, prism_nets))
    #         return "P" + (str(polist.index(polyname)).zfill(3))

    def tiling_id(self):
        tilingname = self.tilingname
        tilists = list(*d.values() for d in (platonic_tilings, archimedean_tilings, biisogonal_tilings))
        netilist = list(net_tessellations.values())
        if (tilingname in tilists):
            return "T" + (str(tilists.index(tilingname)).zfill(3))
        if (tilingname in netilist):
            return "TP" + (str(netilist.index(tilingname)).zfill(2))

    def gen_name(self):
        name = "@".join(self.type_string(),self.tiling_id(),self.tilingname,self.polyname,
        "(%i,%i,%i)"%(self.startcell,self.startface,self.startorientation) )
        return name

    def get_unused_faces(self):
        if(self.get_exploration_type()=="allfaces"):
            allfaces = set(self.poly.keys())
            for visits in self.visited_places.values():
                allfaces = allfaces - {visits[1]}
                if not allfaces:
                    break
            return allfaces
        else:
            raise TypeError("Cannot determine unused faces for optimised search")

    def type_string(self):
        res = ""
        if(self.get_exploration_type() == "optimised"):
            res+="Visit["
        elif(self.get_exploration_type() == "allfaces"):
            res+="Roll["
        if(self.count_visited()==self.max_visitable()):
            res+="Full"
        else:
            res+=self.outside_type()
        if(self.get_exploration_type() == "allfaces"):
            if(self.get_unused_faces()):
                res+="Partial]"
            else:
                res+="Perfect]"
        else:
            res+="]"


    def max_visitable(self):
        smallarea = self.smallarea
        max_visitable = sum((smallarea[0]  < ccenter[0] < smallarea[2] ) and (
                    smallarea[1]  < ccenter[1] < smallarea[3] ) for ccenter in self.visited_places)
        return max_visitable

    def count_visited(self):
        return self.count_inside(self.smallarea)

    def visited_outside(self):
        smallarea = self.smallarea
        outside = sum(bool(self.visited_places[ccenter]) for ccenter in self.visited_places
                      if not (((smallarea[0] < ccenter[0] < smallarea[2]) and (
                    smallarea[1] < ccenter[1] < smallarea[3]))))
        return bool(outside)

    def count_inside(self,area):
        visited = sum(bool(self.visited_places[ccenter]) for ccenter in self.visited_places
                      if (((area[0] < ccenter[0] < area[2]) and (
                    area[1] < ccenter[1] < area[3]))))
        return visited

    def outside_type(self):
        xbarriers = self.bigarea[0], self.smallarea[0], self.smallarea[2], self.bigarea[2]
        ybarriers = self.bigarea[1], self.smallarea[1], self.smallarea[3], self.bigarea[3]
        reached_areas = 0
        for i in range(3):
            for j in range(3):
                if not (i==1 and j==1):
                    area = xbarriers[i],ybarriers[j],xbarriers[i+1],ybarriers[j+1]
                    if(self.count_inside(area)):
                        reached_areas+=1
        if(reached_areas>=7):
            return "Hollow" #"Checkered" #Holes
        elif(reached_areas>=2):
            return "Stripe" #"Banded" #Line
        elif(reached_areas==0):
            return "Zone"#Walled #Zone" #"Area" #Bounded #Zone
        else:
            return "X%i"%reached_areas

    def __post_init__(self):
        self.name = self.gen_name()
        xborder = -self.smallarea[0] #shoud be negative
        yborder = -self.smallarea[1]
        self.drawarea = (a+b for a,b in zip(self.smallarea,(xborder,yborder,-xborder,-yborder)))

    def pickle(self,foldername):
        try:os.mkdir(foldername)
        except:pass
        filename = foldername+os.sep+self.gen_name()+".pickle"
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        return filename

def pickle_load(filename):
    with open(filename) as f:
        loaded_obj = pickle.load(f)
    return loaded_obj