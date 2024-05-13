from __future__ import annotations
import numpy as np
import re

from dataclasses import field, dataclass
from material import Material
from math import radians, sin, cos
from itertools import pairwise


s = lambda angle: sin(radians(angle))
c = lambda angle: cos(radians(angle))

tm = lambda angle: np.array([[c(angle)**2, s(angle)**2, s(angle)*c(angle)],
                             [s(angle)**2, c(angle)**2, -s(angle)*c(angle)],
                             [-2*s(angle)*c(angle), 2*s(angle)*c(angle), c(angle)**2-s(angle)**2]])
 
@dataclass
class Ply():
    material: Material 
    t: float
    angle: float = 0
    _Q: np.ndarray = field(init=False)
    _S: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        T = tm(self.angle)
        self._Q = np.matmul(np.matmul(np.transpose(T), self.material.Q), T)
        self._S = np.matmul(np.matmul(np.transpose(T), self.material.S), T)


    @property
    def Q(self) -> np.ndarray:
        return self._Q.round(3)

    @property
    def S(self) -> np.ndarray:
        return self._S

class Laminat():

    def __init__(self, stacking_sequence:list[int], mat:Material, ply_thickness: float) -> None:
        self.stacking = stacking_sequence
        self.thickness = len(self.stacking)*ply_thickness
        self.plies = {a: Ply(mat, ply_thickness, a) for a in set(self.stacking)} # current limatation to laminates composed of one material and plies of same thickness
        self.ply_boundaries = np.arange(-self.thickness/2, self.thickness/2+ply_thickness, ply_thickness)
        self.ply_coords = list(pairwise(self.ply_boundaries))
        self._A = self._calc_A_matrix()
        self._B = self._calc_B_matrix()
        self._D = self._calc_D_matrix()
    
    def _calc_A_matrix(self) -> np.ndarray:

        A = np.zeros((3, 3)) 
        for a in self.stacking:
            p = self.plies[a]
            Q, t = p._Q, p.t
            A += Q*t
        return A

    def _calc_B_matrix(self) -> np.ndarray:
        
        B = np.zeros((3, 3))
        for i, a in enumerate(self.stacking):
            p = self.plies[a]
            Q, t = p._Q, p.t
            z_coords = self.ply_coords[i]
            B += 1/2*sum(z_coords)*Q*t
        return -B

    def _calc_D_matrix(self) -> np.ndarray:
        
        D = np.zeros((3, 3))
        for i, a in enumerate(self.stacking):
            p = self.plies[a]
            Q, t = p._Q, p.t
            z_coords = self.ply_coords[i]
            D += (1/12*t**2+(1/2*sum(z_coords))**2)*Q*t
        return D

    @property
    def A_matrix(self) -> np.ndarray:
        return self._A.round(3)

    @property
    def B_matrix(self) -> np.ndarray:
        return self._B.round(3)

    @property
    def D_matrix(self) -> np.ndarray:
        return self._D.round(3)

    @classmethod
    def from_string(cls, stacking_sequence:str,*, material:Material, ply_thickness: float, delimeter:str='/') -> Laminat:
        
        clean_pattern = re.compile(rf'[^\d{delimeter}]')
        distinct_delimeter = re.compile(rf'{delimeter}{{2,}}')
        clean_stacking_sequence = distinct_delimeter.sub(delimeter, clean_pattern.sub('', stacking_sequence)).strip(delimeter)
        
        if delimeter not in clean_stacking_sequence:
            raise ValueError(f'Provided stacking seuence ({stacking_sequence}) is not valid.')

        stackng = list(map(int, clean_stacking_sequence.split(delimeter)))

        return cls(stackng, material, ply_thickness=ply_thickness)


if __name__ == "__main__":
    
    mat = Material('Test', 125_000, 8_800, 5_300, 0.29)
    #print(mat.stiffness_matrix)
    # print(mat.compliance_matrix)
    ply = Ply(mat, 0.25, 135)
    print(ply.Q)
    # print(ply.compliance_matrix)

    stacking = [0, 45, 90,-45, 0, 0, -45, 90, 45, 0]

    lam = Laminat(stacking, mat, 0.25)
    print(lam.ply_boundaries)

    print(lam.A_matrix)
    print(lam.B_matrix)
    print(lam.D_matrix)


    #print(lam.thickness)
    #for a, p in lam._ply_angles.items():
    #    print(a)
    #    print(p.stiffness_matrix)

    test_sequence = '135/90/ 45 / 0//135 /0///135/90/45/0/45//'

    lam2 = Laminat.from_string(test_sequence, material = mat, ply_thickness=0.1)

    print(f'{lam2.stacking=}')
    print(lam2.B_matrix)

