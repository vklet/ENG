from itertools import pairwise
from typing import Generator
import numpy as np
#import pyNastran

from dataclasses import dataclass
from pathlib import Path
from pyNastran.bdf.bdf import BDF
from pyNastran.bdf.cards.nodes import GRID

@dataclass
class Material:
    name: str
    type: str
    E: float
    G: float = 0
    nu: float = 0
    rho: float = 0

    def __post_init__(self):
        if not any((self.G, self.nu)):
            raise ValueError("Either G or nu must be defined!")
        if not self.G:
            self.G = self.E/(2*(1 + self.nu))
        if not self.nu:
            self.nu = self.E/(2*self.G) - 1

def get_others(node:int, nodes:list) -> list:
    out = list(nodes)
    out.remove(node)
    return out

def calculate_distances(node: GRID, others: dict) -> Generator:
    for n in others:
        v = np.array(node.xyz) - np.array(n.xyz)
        yield n.nid, np.sqrt(v.dot(v))



#def map_min_distance(nid: int, others:list, node_map:dict=None) -> dict:
#    if not node_map:
#        node_map = {}
#    others.remove(nid)
#
#    for i in others:



grids_file = Path('./grids.csv')

with open(grids_file, 'r') as f:
    grids = f.read().split()[1:]


bulk = BDF()

for g in grids:
    id, cid, *coords = g.split(',')
    id, cid = map(int, (id, cid))
    coords = list(map(float, coords))
    bulk.add_grid(nid=id, xyz=coords, cp=cid)

alu = Material('Aluminium', type='MAT1', E=71000, nu=0.34, rho=2.7e-6)

bulk.add_mat1(mid=1, E=alu.E, G=alu.G, nu=alu.nu, rho=alu.rho)
bulk.add_prod(pid=1, mid=1, A=0.01)

#print(type(bulk.nodes))

#nodes_list = list(bulk.node_ids)
#print(nodes_list)
#test = {n: list(calculate_distances(bulk.Node(n), bulk.Nodes(get_others(n, nodes_list)))) for n in nodes_list}
#print(test)

crod_nodes = list(pairwise([1, 2, 7, 8, 9, 5, 6, 4, 1]))




for eid, nodes in enumerate(crod_nodes, 1):
    bulk.add_crod(eid=eid, pid=1, nids=nodes)


#bulk.write_bdf(grids_file.with_suffix('.dat'))



