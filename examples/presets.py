"""
Matrices y casos de prueba preconfigurados para demostraciones y pruebas rápidas.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from dataclasses import dataclass
from typing import List, Optional


@dataclass
class MatrixPreset:
    id: int
    title: str
    description: str
    dimension: int
    matrix_rows: List[List[str]]
    vector_b: Optional[List[str]]
    recommended_method: str  # "no_pivot" o "pivot"

    @property
    def matrix_text(self) -> str:
        """Devuelve la matriz en texto plano con espacios."""
        return "\n".join(["  ".join(row) for row in self.matrix_rows])

    @property
    def b_text(self) -> str:
        """Devuelve el vector b en texto separado por comas."""
        return ", ".join(self.vector_b) if self.vector_b else ""


PRESETS = [
    MatrixPreset(
        id=1,
        title="Ejemplo 1 (3x3 Clásico sin pivoteo)",
        description="Matriz 3x3 resoluble por Doolittle estándar sin requerir intercambio de filas.",
        dimension=3,
        matrix_rows=[
            ["2", "-1", "-2"],
            ["-4", "6", "3"],
            ["-4", "-2", "8"]
        ],
        vector_b=["-1", "13", "-7"],
        recommended_method="no_pivot"
    ),
    MatrixPreset(
        id=2,
        title="Ejemplo 2 (3x3 con pivoteo / a11=0)",
        description="Matriz con un cero en la primera posición diagonal. Requiere pivoteo parcial (P·A = L·U).",
        dimension=3,
        matrix_rows=[
            ["0", "2", "1"],
            ["1", "-1", "1"],
            ["2", "1", "-1"]
        ],
        vector_b=["4", "1", "1"],
        recommended_method="pivot"
    ),
    MatrixPreset(
        id=3,
        title="Ejemplo 3 (4x4 Completo)",
        description="Matriz 4x4 completa para verificar estabilidad y precisión.",
        dimension=4,
        matrix_rows=[
            ["2", "1", "-1", "2"],
            ["4", "5", "-3", "6"],
            ["-2", "5", "-2", "6"],
            ["4", "11", "-4", "8"]
        ],
        vector_b=["5", "9", "4", "2"],
        recommended_method="pivot"
    ),
    MatrixPreset(
        id=4,
        title="Ejemplo 4 (2x2 Rápido)",
        description="Sistema pequeño 2x2 ideal para comprobación inmediata a mano.",
        dimension=2,
        matrix_rows=[
            ["4", "3"],
            ["6", "3"]
        ],
        vector_b=["10", "12"],
        recommended_method="pivot"
    )
]


def get_preset_by_id(preset_id: int) -> Optional[MatrixPreset]:
    """Obtiene un preset por su identificador numérico."""
    for p in PRESETS:
        if p.id == preset_id:
            return p
    return None


if __name__ == "__main__":
    print("Módulo examples/presets.py ejecutado directamente. Lista de presets disponibles:")
    for p in PRESETS:
        print(f"[{p.id}] {p.title} - Dimensión: {p.dimension}x{p.dimension}")
        print(p.matrix_text)
        print("-" * 30)
