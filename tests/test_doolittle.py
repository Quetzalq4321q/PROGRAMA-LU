import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import unittest
from fractions import Fraction
from core.doolittle import lu_doolittle_no_pivot
from core.matrix_ops import matmul, matrix_equal


class TestDoolittleNoPivot(unittest.TestCase):
    def test_doolittle_success(self):
        A = [
            [Fraction(2), Fraction(-1), Fraction(-2)],
            [Fraction(-4), Fraction(6), Fraction(3)],
            [Fraction(-4), Fraction(-2), Fraction(8)]
        ]
        res = lu_doolittle_no_pivot(A)
        self.assertTrue(res.is_correct)

        # L debe ser triangular inferior unitaria
        self.assertEqual(res.L[0][0], 1)
        self.assertEqual(res.L[1][1], 1)
        self.assertEqual(res.L[2][2], 1)
        self.assertEqual(res.L[0][1], 0)
        self.assertEqual(res.L[0][2], 0)
        self.assertEqual(res.L[1][2], 0)

        # U debe ser triangular superior
        self.assertEqual(res.U[1][0], 0)
        self.assertEqual(res.U[2][0], 0)
        self.assertEqual(res.U[2][1], 0)

        # L * U == A
        self.assertTrue(matrix_equal(matmul(res.L, res.U), A))
        self.assertEqual(res.det_A, 24)

    def test_doolittle_zero_pivot_exception(self):
        # Matriz con a11 = 0
        A = [
            [Fraction(0), Fraction(2)],
            [Fraction(1), Fraction(3)]
        ]
        with self.assertRaises(ZeroDivisionError):
            lu_doolittle_no_pivot(A)


if __name__ == "__main__":
    unittest.main()
