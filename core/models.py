"""
Modelos de datos, tipos y estructuras para la descomposición LU.
(Nombrado models.py para evitar colisión con el módulo estándar 'types' de Python).
"""

from dataclasses import dataclass, field
from fractions import Fraction
from typing import List, Union, Tuple, Optional

Number = Union[Fraction, float]
Matrix = List[List[Number]]
Vector = List[Number]


@dataclass
class LUResult:
    """Resultado de una descomposición LU."""
    method_name: str
    P: Matrix
    L: Matrix
    U: Matrix
    LU: Matrix
    PA: Optional[Matrix] = None
    det_A: Number = Fraction(0)
    is_correct: bool = True
    swaps: List[Tuple[int, int]] = field(default_factory=list)
    steps: str = ""


@dataclass
class SystemSolution:
    """Resultado de resolver Ax = b mediante LU."""
    pb: Vector
    y: Vector
    x: Vector
    steps: str = ""
