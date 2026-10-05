"""
Módulo fachada para compatibilidad con código existente.
Reexporta todas las utilidades desde el nuevo paquete modular 'core'.
"""

from core import (
    Number, Matrix, Vector, LUResult, SystemSolution,
    parse_number, parse_matrix_text, parse_vector_text,
    copy_matrix, identity_matrix, matmul, mat_vec_mul, matrix_equal,
    format_number, format_matrix, format_vector, build_full_report,
    lu_doolittle_no_pivot, lu_doolittle_pivot, solve_system_lu
)

__all__ = [
    "Number", "Matrix", "Vector", "LUResult", "SystemSolution",
    "parse_number", "parse_matrix_text", "parse_vector_text",
    "copy_matrix", "identity_matrix", "matmul", "mat_vec_mul", "matrix_equal",
    "format_number", "format_matrix", "format_vector", "build_full_report",
    "lu_doolittle_no_pivot", "lu_doolittle_pivot", "solve_system_lu",
]
