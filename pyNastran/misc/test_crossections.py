import math
from dataclasses import dataclass, field
from typing import Optional, Protocol

@dataclass(slots=True)
class Crossection(Protocol):
    shape: Optional[str] = None
    dimensions: list[float] = field(default_factory=list)
    area: float = field(init=False)

    def _calculate_cross_area(self) -> float:
        ...


@dataclass(slots=True)
class Ellipse():
    dimensions: list[float]
    area: float = field(init=False)
    shape: str = 'ellipse'

    def __post_init__(self) -> None:
        self.area = self._calculate_area()

    def _calculate_area(self) -> float:
        if len(self.dimensions) == 1:
            a = b = self.dimensions[0]
        else:
            a, b = self.dimensions
        return 1/2*math.pi*(a**2 + b**2)


ellipse = Ellipse(dimensions=[2, 3])
circle = Ellipse(shape='circle', dimensions=[2])

print(ellipse)
print(circle)




