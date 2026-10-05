"""
Operaciones matemáticas básicas con matrices y vectores.
Soporta aritmética de enteros, fracciones exactas y números de coma flotante.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fractions import Fraction
from core.models import Matrix, Vector, Number


def copy_matrix(A: Matrix) -> Matrix:
    """Crea una copia profunda de una matriz."""
    return [[val for val in row] for row in A]


def identity_matrix(n: int, use_fractions: bool = True) -> Matrix:
    """Genera la matriz identidad I de tamaño n x n."""
    one = Fraction(1) if use_fractions else 1.0
    zero = Fraction(0) if use_fractions else 0.0
    return [[one if i == j else zero for j in range(n)] for i in range(n)]


def matmul(A: Matrix, B: Matrix) -> Matrix:
    """Multiplica dos matrices A (m x k) y B (k x n)."""
    rows_A, cols_A = len(A), len(A[0])
    rows_B, cols_B = len(B), len(B[0])
    if cols_A != rows_B:
        raise ValueError(f"Dimensiones incompatibles para multiplicación: ({rows_A}x{cols_A}) y ({rows_B}x{cols_B})")

    zero = Fraction(0) if isinstance(A[0][0], Fraction) else 0.0
    result: Matrix = []
    for i in range(rows_A):
        row = []
        for j in range(cols_B):
            s = sum((A[i][k] * B[k][j] for k in range(cols_A)), zero)
            row.append(s)
        result.append(row)
    return result


def mat_vec_mul(A: Matrix, v: Vector) -> Vector:
    """Multiplica una matriz A (m x n) por un vector v (n)."""
    zero = Fraction(0) if isinstance(A[0][0], Fraction) else 0.0
    return [sum((A[i][j] * v[j] for j in range(len(v))), zero) for i in range(len(A))]


def matrix_equal(A: Matrix, B: Matrix, tol: float = 1e-9) -> bool:
    """Compara si dos matrices son iguales."""
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False

    for i in range(len(A)):
        for j in range(len(A[0])):
            val_a, val_b = A[i][j], B[i][j]
            if isinstance(val_a, Fraction) and isinstance(val_b, Fraction):
                if val_a != val_b:
                    return False
            else:
                if abs(float(val_a) - float(val_b)) > tol:
                    return False
    return True


if __name__ == "__main__":
    print("Módulo core/matrix_ops.py ejecutado directamente. Prueba de operaciones:")
    I = identity_matrix(3)
    print("Identidad 3x3:", I)
    print("I * I == I:", matrix_equal(matmul(I, I), I))
