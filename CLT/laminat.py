from __future__ import annotations
import numpy as np
import re

from dataclasses import field, dataclass
from material import Material
from math import radians, sin, cos

@dataclass
class Ply():
    material: Material 
    t: float
    angle: float
    _Q: np.ndarray = field(init=False)
    _S: np.ndarray = field(init=False)

    def __post_init__(self) -> None:
        s = sin(radians(self.angle))
        c = cos(radians(self.angle))
        T = np.array([[c**2, s**2, s*c],
                      [s**2, c**2, -s*c],
                      [-2*s*c, 2*s*c, c**2-s**2]])
        self._Q = np.matmul(np.matmul(np.transpose(T), self.material.stiffness_matrix),T)
        self._S = np.matmul(np.matmul(np.transpose(T), self.material.compliance_matrix),T)

    @property
    def stiffness_matrix(self) -> np.ndarray:
        return self._Q.round(3)

    @property
    def compliance_matrix(self) -> np.ndarray:
        return self._S

class Laminat():
    def __init__(self, stacking_sequence:list[int], mat:Material, ply_thickness: float) -> None:
        self.stacking = stacking_sequence
        self.thickness = len(self.stacking)*ply_thickness
        self._ply_angles = {a: Ply(mat, ply_thickness, a) for a in set(self.stacking)} # current limatation to laminates composed of one material and plies of same thickness
        self._A = self._calc_A_matrix(ply_thickness)
    
    def _calc_A_matrix(self, ply_thickness:float) -> np.ndarray:
        ply_stiffness_matrices = [self._ply_angles[a]._Q for a in self.stacking]
        return np.sum(ply_stiffness_matrices, axis=0)*ply_thickness

    # TODO
    def _calc_B_matrix(self) -> np.ndarray:
        pass

    def _calc_D_matrix(self) -> np.ndarray:
        pass

    @property
    def A_matrix(self) -> np.ndarray:
        return self._A.round(3)

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
    #ply = Ply(mat, 0.25, 135)
    #print(ply.stiffness_matrix)
    # print(ply.compliance_matrix)

    stacking = [0, 45, 90,-45, 0, 0, -45, 90, 45, 0]

    lam = Laminat(stacking, mat, 0.25)

    print(lam.A_matrix)

    #print(lam.thickness)
    #for a, p in lam._ply_angles.items():
    #    print(a)
    #    print(p.stiffness_matrix)

    #test_sequence = '0/ 45 / 90//135 /0///135/90/45/0///'

    #lam2 = Laminat.from_string(test_sequence, material = mat, ply_thickness=0.1)

    #print(f'{lam2.stacking=}')

