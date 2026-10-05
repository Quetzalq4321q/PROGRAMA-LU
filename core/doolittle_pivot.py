"""
Implementación del Método de Doolittle con Pivoteo Parcial.
Ecuación fundamental: P · A = L · U
donde P es la matriz de permutación, L es triangular inferior unitaria, y U es triangular superior.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fractions import Fraction
from typing import List, Tuple
from core.models import Matrix, LUResult
from core.matrix_ops import identity_matrix, matmul, matrix_equal, copy_matrix
from core.formatters import format_number, format_matrix


def lu_doolittle_pivot(A: Matrix) -> LUResult:
    """
    Realiza la descomposición LU con pivoteo parcial (P * A = L * U).
    Intercambia filas para situar en la diagonal el valor máximo en valor absoluto.
    """
    n = len(A)
    use_frac = isinstance(A[0][0], Fraction)
    zero = Fraction(0) if use_frac else 0.0
    one = Fraction(1) if use_frac else 1.0

    U = copy_matrix(A)
    L = identity_matrix(n, use_fractions=use_frac)
    P = identity_matrix(n, use_fractions=use_frac)

    steps = []
    swaps: List[Tuple[int, int]] = []
    sign_det = 1

    steps.append("==================================================")
    steps.append("DESCOMPOSICIÓN LU: CON PIVOTEO PARCIAL (P · A = L · U)")
    steps.append("Ecuación fundamental: P · A = L · U")
    steps.append(f"Dimensión de la matriz: {n} x {n}")
    steps.append("==================================================\n")

    for i in range(n):
        steps.append(f"--- PASO {i + 1}: Búsqueda de pivote y eliminación para columna {i + 1} ---")

        # 1. Búsqueda del pivote parcial
        max_row = i
        max_val = abs(U[i][i])
        for r in range(i + 1, n):
            val_r = abs(U[r][i])
            if val_r > max_val:
                max_val = val_r
                max_row = r

        # 2. Intercambio de filas
        if max_row != i:
            steps.append(
                f"-> Pivoteo requerido: Elemento máximo en columna {i + 1} está en fila {max_row + 1} "
                f"({format_number(U[max_row][i], use_frac)})."
            )
            steps.append(f"   Intercambiando Fila {i + 1} <---> Fila {max_row + 1}.")

            U[i], U[max_row] = U[max_row], U[i]
            P[i], P[max_row] = P[max_row], P[i]

            for c in range(i):
                L[i][c], L[max_row][c] = L[max_row][c], L[i][c]

            swaps.append((i + 1, max_row + 1))
            sign_det *= -1
        else:
            steps.append(
                f"-> No se requiere intercambio de filas (pivote actual en fila {i + 1}: "
                f"{format_number(U[i][i], use_frac)})."
            )

        pivot = U[i][i]
        if pivot == 0:
            steps.append(f"   [AVISO] El pivote en ({i+1},{i+1}) es CERO. La matriz es singular.")
        else:
            # 3. Eliminación gaussiana hacia abajo
            if i < n - 1:
                steps.append(f"\n   Cálculo de multiplicadores m_{{k{i+1}}} y actualización de filas:")
                for r in range(i + 1, n):
                    factor = U[r][i] / pivot
                    L[r][i] = factor
                    steps.append(
                        f"   • Multiplicador m_{{{r+1},{i+1}}} = l_{{{r+1},{i+1}}} = "
                        f"{format_number(U[r][i], use_frac)} / {format_number(pivot, use_frac)} = "
                        f"{format_number(factor, use_frac)}"
                    )
                    steps.append(f"     Fila {r+1} = Fila {r+1} - ({format_number(factor, use_frac)}) * Fila {i+1}")
                    U[r][i] = zero
                    for c in range(i + 1, n):
                        U[r][c] -= factor * U[i][c]
        steps.append("")

    det_U = Fraction(1) if use_frac else 1.0
    for i in range(n):
        det_U *= U[i][i]
    det_A = sign_det * det_U

    PA = matmul(P, A)
    LU = matmul(L, U)
    is_correct = matrix_equal(LU, PA)

    return LUResult(
        method_name="Doolittle con Pivoteo Parcial (P · A = L · U)",
        P=P,
        L=L,
        U=U,
        LU=LU,
        PA=PA,
        det_A=det_A,
        is_correct=is_correct,
        swaps=swaps,
        steps="\n".join(steps)
    )


if __name__ == "__main__":
    print("Módulo core/doolittle_pivot.py ejecutado directamente. Demostración:")
    test_A = [
        [Fraction(0), Fraction(2), Fraction(1)],
        [Fraction(1), Fraction(-1), Fraction(1)],
        [Fraction(2), Fraction(1), Fraction(-1)]
    ]
    res = lu_doolittle_pivot(test_A)
    print("Matriz P:")
    print(format_matrix(res.P))
    print("Matriz L:")
    print(format_matrix(res.L))
    print("Matriz U:")
    print(format_matrix(res.U))
    print(f"Correcto: {res.is_correct}, det(A): {res.det_A}")
