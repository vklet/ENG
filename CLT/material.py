import numpy as np

from dataclasses import field, dataclass


@dataclass
class Material():
    name: str
    E1: float
    E2: float
    G12: float
    nu12: float
    nu21: float = field(init=False)

    # Stiffness and Compliance formulation
    Q: np.ndarray = field(init=False)
    S: np.ndarray = field(init=False)


    def __post_init__(self) -> None:
        
        denominator = 1-self.nu12**2*self.E2/self.E1
        Q11 = self.E1/denominator
        Q22 =  self.E2/denominator
        Q12 = self.nu12*Q22 # Q21 equals Q12, therefore omited
        Q33 = self.G12
        self.nu21 = self.nu12*self.E2/self.E1
        S11 = 1/self.E1
        S22 = 1/self.E2
        S12 = -self.nu12/self.E1 # S21 equals S12, therefore omited
        S33 = 1/self.G12

        rows = [0, 0, 1, 1, 2]
        cols = [0, 1, 0, 1, 2]
        self.Q = np.zeros((3, 3))
        self.S = np.zeros((3, 3))
        self.Q[rows, cols] = np.array([Q11, Q12, Q12, Q22, Q33])
        self.S[rows, cols] = np.array([S11, S12, S12, S22, S33])

    @property
    def stiffness_matrix(self) -> np.ndarray:
        return self.Q.round(3)

    @property
    def compliance_matrix(self) -> np.ndarray:
        return self.S


if __name__ == "__main__":
    mat = Material('Test', 125_000, 8_800, 5_300, 0.29)
    print(mat.stiffness_matrix)
    print(mat.compliance_matrix)

