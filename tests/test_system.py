import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import unittest
from fractions import Fraction
from core.doolittle_pivot import lu_doolittle_pivot
from core.linear_system import solve_system_lu
from core.matrix_ops import mat_vec_mul


class TestLinearSystem(unittest.TestCase):
    def test_solve_3x3_system(self):
        A = [
            [Fraction(2), Fraction(1), Fraction(-1)],
            [Fraction(-3), Fraction(-1), Fraction(2)],
            [Fraction(-2), Fraction(1), Fraction(2)]
        ]
        b = [Fraction(8), Fraction(-11), Fraction(-3)]

        res_lu = lu_doolittle_pivot(A)
        sol = solve_system_lu(res_lu.P, res_lu.L, res_lu.U, b)

        # Comprobar A * x == b
        Ax = mat_vec_mul(A, sol.x)
        self.assertEqual(Ax, b)

        # Solución analítica esperada: x = [2, 3, -1]
        self.assertEqual(sol.x, [Fraction(2), Fraction(3), Fraction(-1)])


if __name__ == "__main__":
    unittest.main()
