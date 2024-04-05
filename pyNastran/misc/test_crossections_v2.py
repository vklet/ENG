import math
from dataclasses import dataclass, field
from typing import Callable, Any

calculate_section_parameters = Callable[[list[float]], dict[str, Any]]

def calculate_elliptical_cross_section(dimensions: list[float]) -> dict[str, Any]:
    if len(dimensions) == 1:
        a = b = dimensions[0]
    else:
        a, b = dimensions
    area = math.pi/2*(a**2 + b**2)
    moments_of_inertia = (math.pi/4*a**3*b, math.pi/4*a*b**3)
    return {'area': area, 'moments_of_inertia': moments_of_inertia}

def calculate_rectangular_cross_section(dimensions: list[float]) -> dict[str, Any]:
    if len(dimensions) == 1:
        a = b = dimensions[0]
    else:
        a, b = dimensions
    area = a*b
    moments_of_inertia = (a**3*b/12, a*b**3/12)
    return {'area': area, 'moments_of_inertia': moments_of_inertia}

def calculate_triangular_cross_section(dimensions: list[float]) -> dict[str, Any]:
    if len(dimensions) == 1:
        a = b = dimensions[0]
    else:
        a, b = dimensions
    area = a*b/2
    moments_of_inertia = (a**3*b/36, a*b**3/36, a**2*b**2/72)
    return {'area': area, 'moments_of_inertia': moments_of_inertia}

section_functions = {'ellipse': calculate_elliptical_cross_section, 'rectangle': calculate_rectangular_cross_section, 'triangle': calculate_triangular_cross_section}

@dataclass(slots=True)
class Crossection():
    shape: str
    dimensions: list[float] = field(default_factory=list)
    area: float = field(init=False)
    moments_of_inertia: tuple[float] = field(init=False)
    
    def __post_init__(self) -> None:
        function = section_functions.get(self.shape)
        if not function:
            raise ValueError("No function defined")

        section_parameters = self._calculate_cross_section(function)
        self.area = section_parameters['area']
        self.moments_of_inertia = section_parameters['moments_of_inertia']
    
    def _calculate_cross_section(self, function: calculate_section_parameters):
        if not self.dimensions:
            raise ValueError("No parameters defined")
        return function(self.dimensions)

ellipse = Crossection('ellipse', [3, 5])
circle = Crossection('ellipse', [3])
rectangle = Crossection('rectangle', [6, 10])
quadrat = Crossection('rectangle', [6])
triangle = Crossection('triangle', [6])
triangle2 = Crossection('triangle', [6, 10])
print(ellipse)
print(circle)
print(rectangle)
print(quadrat)
print(triangle)
print(triangle2)
