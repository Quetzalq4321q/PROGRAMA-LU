"""
Implementación del Método de Doolittle para Descomposición LU (Sin Pivoteo).
Ecuación fundamental: A = L · U
donde L es triangular inferior unitaria (l_ii = 1) y U es triangular superior.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fractions import Fraction
from core.models import Matrix, LUResult
from core.matrix_ops import identity_matrix, matmul, matrix_equal
from core.formatters import format_number, format_matrix


def lu_doolittle_no_pivot(A: Matrix) -> LUResult:
    """
    Realiza la descomposición LU de la matriz cuadrada A usando el algoritmo de Doolittle.
    Lanza ZeroDivisionError si se encuentra un pivote cero en la diagonal de U.
    """
    n = len(A)
    use_frac = isinstance(A[0][0], Fraction)
    zero = Fraction(0) if use_frac else 0.0
    one = Fraction(1) if use_frac else 1.0

    L = identity_matrix(n, use_fractions=use_frac)
    U = [[zero for _ in range(n)] for _ in range(n)]

    steps = []
    steps.append("==================================================")
    steps.append("DESCOMPOSICIÓN LU: MÉTODO DE DOOLITTLE (SIN PIVOTEO)")
    steps.append("Ecuación fundamental: A = L · U")
    steps.append(f"Dimensión de la matriz: {n} x {n}")
    steps.append("==================================================\n")

    for i in range(n):
        steps.append(f"--- PASO {i + 1}: Fila {i + 1} de U y Columna {i + 1} de L ---")

        # 1. Calcular fila i de U: u_ik = a_ik - sum(l_ij * u_jk)
        steps.append(f"1) Cálculo de los elementos de la fila {i + 1} de U:")
        for k in range(i, n):
            terms = [L[i][j] * U[j][k] for j in range(i)]
            s = sum(terms, zero)
            U[i][k] = A[i][k] - s

            if i == 0:
                steps.append(f"   u_{{{i+1},{k+1}}} = a_{{{i+1},{k+1}}} = {format_number(U[i][k], use_frac)}")
            else:
                formula_str = " - ".join([
                    f"({format_number(L[i][j], use_frac)} * {format_number(U[j][k], use_frac)})"
                    for j in range(i)
                ])
                steps.append(f"   u_{{{i+1},{k+1}}} = a_{{{i+1},{k+1}}} - [{formula_str}] = {format_number(U[i][k], use_frac)}")

        # 2. Verificar pivote
        if U[i][i] == 0:
            if i < n - 1:
                msg = (
                    f"¡ERROR!: Se encontró un pivote igual a CERO en la posición ({i + 1}, {i + 1}) "
                    f"[u_{{{i+1},{i+1}}} = 0].\n"
                    f"El método de Doolittle sin pivoteo no puede continuar debido a una división entre cero.\n"
                    f"Sugerencia: Seleccione 'Doolittle con pivoteo parcial (P·A = L·U)'."
                )
                steps.append(f"\n[!] {msg}")
                raise ZeroDivisionError(msg)

        # 3. Calcular columna i de L: l_ki = (a_ki - sum(l_kj * u_ji)) / u_ii
        if i < n - 1:
            steps.append(f"\n2) Cálculo de los multiplicadores en la columna {i + 1} de L (l_{{ii}} = 1):")
            for k in range(i + 1, n):
                terms = [L[k][j] * U[j][i] for j in range(i)]
                s = sum(terms, zero)
                diff = A[k][i] - s
                L[k][i] = diff / U[i][i]

                if i == 0:
                    steps.append(
                        f"   l_{{{k+1},{i+1}}} = a_{{{k+1},{i+1}}} / u_{{{i+1},{i+1}}} = "
                        f"{format_number(A[k][i], use_frac)} / {format_number(U[i][i], use_frac)} = "
                        f"{format_number(L[k][i], use_frac)}"
                    )
                else:
                    formula_str = " - ".join([
                        f"({format_number(L[k][j], use_frac)} * {format_number(U[j][i], use_frac)})"
                        for j in range(i)
                    ])
                    steps.append(
                        f"   l_{{{k+1},{i+1}}} = (a_{{{k+1},{i+1}}} - [{formula_str}]) / u_{{{i+1},{i+1}}} = "
                        f"{format_number(L[k][i], use_frac)}"
                    )
        steps.append("")

    # Determinante de A
    det_A = Fraction(1) if use_frac else 1.0
    for i in range(n):
        det_A *= U[i][i]

    P = identity_matrix(n, use_fractions=use_frac)
    LU = matmul(L, U)
    is_correct = matrix_equal(LU, A)

    return LUResult(
        method_name="Doolittle Clásico (A = L · U)",
        P=P,
        L=L,
        U=U,
        LU=LU,
        PA=None,
        det_A=det_A,
        is_correct=is_correct,
        swaps=[],
        steps="\n".join(steps)
    )


if __name__ == "__main__":
    print("Módulo core/doolittle.py ejecutado directamente. Demostración:")
    test_A = [
        [Fraction(2), Fraction(-1), Fraction(-2)],
        [Fraction(-4), Fraction(6), Fraction(3)],
        [Fraction(-4), Fraction(-2), Fraction(8)]
    ]
    res = lu_doolittle_no_pivot(test_A)
    print("Matriz L:")
    print(format_matrix(res.L))
    print("Matriz U:")
    print(format_matrix(res.U))
    print(f"Correcto: {res.is_correct}, det(A): {res.det_A}")
