import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import unittest
from fractions import Fraction
from core.doolittle_pivot import lu_doolittle_pivot
from core.matrix_ops import matmul, matrix_equal


class TestDoolittlePivot(unittest.TestCase):
    def test_pivot_with_zero_initial(self):
        A = [
            [Fraction(0), Fraction(2), Fraction(1)],
            [Fraction(1), Fraction(-1), Fraction(1)],
            [Fraction(2), Fraction(1), Fraction(-1)]
        ]
        res = lu_doolittle_pivot(A)
        self.assertTrue(res.is_correct)
        self.assertIsNotNone(res.PA)

        # Verificar P * A == L * U
        self.assertTrue(matrix_equal(matmul(res.P, A), matmul(res.L, res.U)))
        self.assertEqual(res.det_A, 9)

    def test_pivot_4x4(self):
        A = [
            [Fraction(2), Fraction(1), Fraction(-1), Fraction(2)],
            [Fraction(4), Fraction(5), Fraction(-3), Fraction(6)],
            [Fraction(-2), Fraction(5), Fraction(-2), Fraction(6)],
            [Fraction(4), Fraction(11), Fraction(-4), Fraction(8)]
        ]
        res = lu_doolittle_pivot(A)
        self.assertTrue(res.is_correct)
        self.assertTrue(matrix_equal(matmul(res.P, A), matmul(res.L, res.U)))


if __name__ == "__main__":
    unittest.main()
