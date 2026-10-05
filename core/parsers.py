"""
Módulo de parseo para matrices, vectores y números.
Convierte entradas en texto plano a matrices de objetos numéricos (Fraction o float).
"""

import sys
from pathlib import Path

# Asegurar que el directorio raíz del proyecto esté en sys.path si se ejecuta directamente
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from fractions import Fraction
import re
from typing import Optional
from core.models import Number, Matrix, Vector


def parse_number(token: str, use_fractions: bool = True) -> Number:
    """
    Convierte un string a Fraction o float.
    Soporta enteros ('3'), decimales ('1.5', '1,5'), y fracciones ('-3/4').
    """
    token = token.strip()
    if not token:
        raise ValueError("El valor ingresado está vacío.")

    if ',' in token and '/' not in token:
        token = token.replace(',', '.')

    if '/' in token:
        parts = token.split('/')
        if len(parts) == 2:
            num = int(parts[0].strip())
            den = int(parts[1].strip())
            if den == 0:
                raise ZeroDivisionError(f"Denominador cero en la fracción: '{token}'")
            frac = Fraction(num, den)
            return frac if use_fractions else float(frac)
        else:
            raise ValueError(f"Fracción inválida: '{token}'")

    if use_fractions:
        try:
            return Fraction(token)
        except Exception:
            return Fraction(float(token)).limit_denominator(1_000_000)
    else:
        return float(token)


def parse_matrix_text(text: str, use_fractions: bool = True) -> Matrix:
    """
    Parsea una matriz cuadrada N x N desde un string.
    Soporta:
    - Espacios, comas o tabuladores.
    - MATLAB: '1 2; 3 4'
    - Python: '[[1, 2], [3, 4]]'
    """
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("El texto de la matriz está vacío.")

    if cleaned.startswith('[') and cleaned.endswith(']'):
        inner = cleaned[1:-1].strip()
        if '[' in inner and ']' in inner:
            row_matches = re.findall(r'\[([^\]]+)\]', inner)
            rows_raw = row_matches if row_matches else inner.split(';')
        else:
            rows_raw = inner.split(';')
    elif ';' in cleaned:
        rows_raw = cleaned.split(';')
    else:
        rows_raw = cleaned.splitlines()

    matrix: Matrix = []
    for line in rows_raw:
        line = line.strip().strip('[]')
        if not line:
            continue

        if ',' in line:
            tokens = [t.strip() for t in line.split(',') if t.strip()]
        else:
            tokens = line.split()

        if not tokens:
            continue

        row = [parse_number(t, use_fractions) for t in tokens]
        matrix.append(row)

    if not matrix:
        raise ValueError("No se encontraron números válidos para formar la matriz.")

    n_cols = len(matrix[0])
    for i, row in enumerate(matrix):
        if len(row) != n_cols:
            raise ValueError(
                f"La fila {i + 1} tiene {len(row)} elementos, pero la fila 1 tiene {n_cols}. "
                f"Todas las filas deben tener la misma cantidad de columnas."
            )

    if len(matrix) != n_cols:
        raise ValueError(
            f"La matriz debe ser cuadrada (N x N). Dimensión detectada: {len(matrix)} filas x {n_cols} columnas."
        )

    return matrix


def parse_vector_text(text: str, expected_len: int, use_fractions: bool = True) -> Optional[Vector]:
    """Parsea un vector independiente b de tamaño esperado."""
    cleaned = text.strip()
    if not cleaned:
        return None

    cleaned = cleaned.replace('[', ' ').replace(']', ' ').replace(';', ' ')
    tokens = [t.strip() for t in cleaned.split(',') if t.strip()] if ',' in cleaned else cleaned.split()

    if not tokens:
        return None

    if len(tokens) != expected_len:
        raise ValueError(f"El vector b debe tener {expected_len} elementos, pero tiene {len(tokens)}.")

    return [parse_number(t, use_fractions) for t in tokens]


if __name__ == "__main__":
    print("Módulo core/parsers.py ejecutado directamente. Prueba de parseo:")
    sample = "2 -1 -2\n-4 6 3\n-4 -2 8"
    m = parse_matrix_text(sample)
    print(f"Matriz parseada exitosamente ({len(m)}x{len(m[0])}):", m)
