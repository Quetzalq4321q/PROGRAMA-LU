"""
Paquete core del Analizador de Descomposición LU.
Exporta las funciones principales y tipos de datos.
"""

from core.models import Number, Matrix, Vector, LUResult, SystemSolution
from core.parsers import parse_number, parse_matrix_text, parse_vector_text
from core.matrix_ops import copy_matrix, identity_matrix, matmul, mat_vec_mul, matrix_equal
from core.formatters import format_number, format_matrix, format_vector, build_full_report
from core.doolittle import lu_doolittle_no_pivot
from core.doolittle_pivot import lu_doolittle_pivot
from core.linear_system import solve_system_lu

__all__ = [
    "Number", "Matrix", "Vector", "LUResult", "SystemSolution",
    "parse_number", "parse_matrix_text", "parse_vector_text",
    "copy_matrix", "identity_matrix", "matmul", "mat_vec_mul", "matrix_equal",
    "format_number", "format_matrix", "format_vector", "build_full_report",
    "lu_doolittle_no_pivot",
    "lu_doolittle_pivot",
    "solve_system_lu",
]
