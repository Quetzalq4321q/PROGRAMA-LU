import sys
from pathlib import Path
root_dir = str(Path(__file__).resolve().parent.parent)
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

import unittest
from fractions import Fraction
from core.parsers import parse_number, parse_matrix_text, parse_vector_text


class TestParsers(unittest.TestCase):
    def test_parse_numbers(self):
        self.assertEqual(parse_number("5"), Fraction(5, 1))
        self.assertEqual(parse_number("-3/4"), Fraction(-3, 4))
        self.assertEqual(parse_number("2.5"), Fraction(5, 2))
        self.assertEqual(parse_number("1,5"), Fraction(3, 2))
        self.assertAlmostEqual(parse_number("1.25", use_fractions=False), 1.25)

    def test_parse_matrix_plain(self):
        text = "2  -1  -2\n-4   6   3\n-4  -2   8"
        matrix = parse_matrix_text(text)
        self.assertEqual(len(matrix), 3)
        self.assertEqual(len(matrix[0]), 3)
        self.assertEqual(matrix[0][0], Fraction(2))
        self.assertEqual(matrix[1][0], Fraction(-4))

    def test_parse_matrix_matlab_style(self):
        text = "1 2; 3 4"
        matrix = parse_matrix_text(text)
        self.assertEqual(matrix, [[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]])

    def test_parse_matrix_brackets_and_commas(self):
        text = "[[1, 2], [3, 4]]"
        matrix = parse_matrix_text(text)
        self.assertEqual(matrix, [[Fraction(1), Fraction(2)], [Fraction(3), Fraction(4)]])

    def test_parse_vector(self):
        v = parse_vector_text("1, -2, 3/5", expected_len=3)
        self.assertEqual(v, [Fraction(1), Fraction(-2), Fraction(3, 5)])

    def test_parse_invalid_dimension(self):
        with self.assertRaises(ValueError):
            parse_matrix_text("1 2 3\n4 5")  # Filas desiguales

        with self.assertRaises(ValueError):
            parse_matrix_text("1 2 3\n4 5 6")  # No es cuadrada (2x3)


if __name__ == "__main__":
    unittest.main()
