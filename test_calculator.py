import unittest

from calculator import CalcError, calculate


class CalculateTest(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(calculate("1 + 2"), 3)
        self.assertEqual(calculate("5 - 8"), -3)
        self.assertEqual(calculate("4 * 2.5"), 10)
        self.assertEqual(calculate("7 / 2"), 3.5)
        self.assertEqual(calculate("10 % 3"), 1)
        self.assertEqual(calculate("2 ** 10"), 1024)

    def test_precedence_and_parentheses(self):
        self.assertEqual(calculate("1 + 2 * 3"), 7)
        self.assertEqual(calculate("(1 + 2) * 3"), 9)
        self.assertEqual(calculate("-2 ** 2"), -4)
        self.assertEqual(calculate("(-2) ** 2"), 4)

    def test_errors(self):
        for expr in ["1 / 0", "", "1 +", "abc", "__import__('os')", "2 ** 99999"]:
            with self.assertRaises(CalcError, msg=expr):
                calculate(expr)


if __name__ == "__main__":
    unittest.main()
