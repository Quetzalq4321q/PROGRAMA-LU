"""
Resolución de sistemas de ecuaciones lineales A · x = b usando la factorización LU.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fractions import Fraction
from core.models import Matrix, Vector, SystemSolution
from core.matrix_ops import mat_vec_mul
from core.formatters import format_number, format_vector


def solve_system_lu(P: Matrix, L: Matrix, U: Matrix, b: Vector) -> SystemSolution:
    """
    Resuelve el sistema lineal Ax = b dada la descomposición P*A = L*U.
    Lanza ValueError si la matriz es singular (U[i][i] == 0).
    """
    n = len(P)
    use_frac = isinstance(L[0][0], Fraction)
    zero = Fraction(0) if use_frac else 0.0

    steps = []
    steps.append("==================================================")
    steps.append("RESOLUCIÓN DEL SISTEMA DE ECUACIONES LINEALES: A · x = b")
    steps.append("Estrategia: P·A·x = P·b  =>  L·(U·x) = P·b")
    steps.append("==================================================\n")

    # 1. Permutar b
    pb = mat_vec_mul(P, b)
    steps.append("Paso 1: Aplicar matriz de permutación al vector b (b* = P · b):")
    for i in range(n):
        steps.append(f"   b*_{{{i+1}}} = {format_number(pb[i], use_frac)}")
    steps.append("")

    # 2. Sustitución hacia adelante
    steps.append("Paso 2: Sustitución hacia adelante (L · y = b*):")
    y: Vector = [zero] * n
    for i in range(n):
        terms = [L[i][j] * y[j] for j in range(i)]
        s = sum(terms, zero)
        y[i] = (pb[i] - s) / L[i][i]
        steps.append(
            f"   y_{{{i+1}}} = ({format_number(pb[i], use_frac)} - {format_number(s, use_frac)}) "
            f"/ {format_number(L[i][i], use_frac)} = {format_number(y[i], use_frac)}"
        )
    steps.append("")

    # 3. Sustitución hacia atrás
    steps.append("Paso 3: Sustitución hacia atrás (U · x = y):")
    x: Vector = [zero] * n
    for i in range(n - 1, -1, -1):
        if U[i][i] == 0:
            raise ValueError(
                f"El pivote u_{{{i+1},{i+1}}} es CERO. El sistema no tiene solución única o es incompatible."
            )
        terms = [U[i][j] * x[j] for j in range(i + 1, n)]
        s = sum(terms, zero)
        x[i] = (y[i] - s) / U[i][i]
        steps.append(
            f"   x_{{{i+1}}} = ({format_number(y[i], use_frac)} - {format_number(s, use_frac)}) "
            f"/ {format_number(U[i][i], use_frac)} = {format_number(x[i], use_frac)}"
        )

    return SystemSolution(
        pb=pb,
        y=y,
        x=x,
        steps="\n".join(steps)
    )


if __name__ == "__main__":
    print("Módulo core/linear_system.py ejecutado directamente. Demostración:")
    from core.doolittle_pivot import lu_doolittle_pivot
    A = [
        [Fraction(2), Fraction(1), Fraction(-1)],
        [Fraction(-3), Fraction(-1), Fraction(2)],
        [Fraction(-2), Fraction(1), Fraction(2)]
    ]
    b = [Fraction(8), Fraction(-11), Fraction(-3)]
    res_lu = lu_doolittle_pivot(A)
    sol = solve_system_lu(res_lu.P, res_lu.L, res_lu.U, b)
    print("Solución x:")
    print(format_vector(sol.x))
