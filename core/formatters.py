"""
Módulo de formateo y visualización de matrices, números y reportes.
"""

import sys
from pathlib import Path

root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fractions import Fraction
from typing import Optional
from core.models import Number, Matrix, Vector, LUResult, SystemSolution


def format_number(val: Number, as_fraction: bool = True, decimals: int = 4) -> str:
    """Da formato legible a un número (fracción simplificada o decimal redondeado)."""
    if isinstance(val, Fraction):
        if as_fraction:
            if val.denominator == 1:
                return str(val.numerator)
            return f"{val.numerator}/{val.denominator}"
        else:
            f_val = float(val)
            if abs(f_val - round(f_val)) < 1e-10:
                return str(int(round(f_val)))
            return f"{f_val:.{decimals}f}".rstrip('0').rstrip('.')
    else:
        if as_fraction:
            frac = Fraction(val).limit_denominator(10000)
            if frac.denominator == 1:
                return str(frac.numerator)
            return f"{frac.numerator}/{frac.denominator}"
        else:
            if abs(val - round(val)) < 1e-10:
                return str(int(round(val)))
            return f"{val:.{decimals}f}".rstrip('0').rstrip('.')


def format_matrix(M: Matrix, as_fraction: bool = True, decimals: int = 4) -> str:
    """Convierte una matriz a texto alineado con columnas monoespaciadas y corchetes."""
    n_rows = len(M)
    n_cols = len(M[0])
    str_grid = [[format_number(M[i][j], as_fraction, decimals) for j in range(n_cols)] for i in range(n_rows)]
    col_widths = [max(len(str_grid[i][j]) for i in range(n_rows)) for j in range(n_cols)]

    lines = []
    for i in range(n_rows):
        row_str = "  ".join(str_grid[i][j].rjust(col_widths[j]) for j in range(n_cols))
        lines.append(f"[ {row_str} ]")
    return "\n".join(lines)


def format_vector(v: Vector, as_fraction: bool = True, decimals: int = 4) -> str:
    """Formatea un vector columna con corchetes y alineación."""
    elements = [format_number(x, as_fraction, decimals) for x in v]
    max_w = max(len(s) for s in elements) if elements else 1
    return "\n".join(f"[ {s.rjust(max_w)} ]" for s in elements)


def build_full_report(A: Matrix, res: LUResult, b: Optional[Vector] = None,
                      res_system: Optional[SystemSolution] = None,
                      as_fraction: bool = True, decimals: int = 4) -> str:
    """Construye un reporte textual completo con matrices y verificación."""
    lines = []
    lines.append("=" * 65)
    lines.append(f" RESULTADOS: DESCOMPOSICIÓN LU ({res.method_name})")
    lines.append("=" * 65)
    lines.append("")

    lines.append("1. MATRIZ ORIGINAL A:")
    lines.append(format_matrix(A, as_fraction, decimals))
    lines.append("")

    if res.PA is not None:
        lines.append("2. MATRIZ DE PERMUTACIÓN P:")
        lines.append(format_matrix(res.P, as_fraction, decimals))
        if res.swaps:
            swaps_str = ", ".join([f"Fila {r1} <-> Fila {r2}" for r1, r2 in res.swaps])
            lines.append(f"   Intercambios de filas realizados: {swaps_str}")
        else:
            lines.append("   (No fue necesario realizar intercambios de filas)")
        lines.append("")

        lines.append("3. MATRIZ PERMUTADA (P · A):")
        lines.append(format_matrix(res.PA, as_fraction, decimals))
        lines.append("")

    lines.append("4. MATRIZ TRIANGULAR INFERIOR L (Diagonal = 1):")
    lines.append(format_matrix(res.L, as_fraction, decimals))
    lines.append("")

    lines.append("5. MATRIZ TRIANGULAR SUPERIOR U:")
    lines.append(format_matrix(res.U, as_fraction, decimals))
    lines.append("")

    lines.append("6. VERIFICACIÓN DEL PRODUCTO:")
    target_name = "P · A" if res.PA is not None else "A"
    lines.append("   Matriz Producto (L · U):")
    lines.append(format_matrix(res.LU, as_fraction, decimals))
    if res.is_correct:
        lines.append(f"   ✓ VERIFICACIÓN EXITOSA: L · U coincide exactamente con {target_name}.")
    else:
        lines.append(f"   ✗ AVISO: Discrepancia numérica en L · U vs {target_name}.")
    lines.append("")

    lines.append(f"7. DETERMINANTE DE A: det(A) = {format_number(res.det_A, as_fraction, decimals)}")
    lines.append("")

    if res_system is not None and b is not None:
        lines.append("-" * 65)
        lines.append(" RESOLUCIÓN DEL SISTEMA LINEAL: A · x = b")
        lines.append("-" * 65)
        lines.append("Vector de términos independientes b:")
        lines.append(format_vector(b, as_fraction, decimals))
        lines.append("")

        if res.PA is not None:
            lines.append("Vector permutado b* = P · b:")
            lines.append(format_vector(res_system.pb, as_fraction, decimals))
            lines.append("")

        lines.append("Sustitución hacia adelante: Vector y (L · y = P · b):")
        lines.append(format_vector(res_system.y, as_fraction, decimals))
        lines.append("")

        lines.append("Sustitución hacia atrás: Vector x (U · x = y):")
        lines.append(format_vector(res_system.x, as_fraction, decimals))
        lines.append("")

    lines.append("=" * 65)
    return "\n".join(lines)


if __name__ == "__main__":
    print("Módulo core/formatters.py ejecutado directamente.")
    sample_m = [[Fraction(1, 3), Fraction(-4)], [Fraction(5, 2), Fraction(7)]]
    print("Muestra de matriz formateada:")
    print(format_matrix(sample_m))
