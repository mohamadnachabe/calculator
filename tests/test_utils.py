import unittest

import calculator.utils as u


class TestCalculatorUtils(unittest.TestCase):

    def test_find(self):
        s = ['*', '*', '-']
        n = ['4', '6', '7', '9']
        t1 = u.find_operation_up_to_next_add_or_sub(s, 0)
        t2 = u.find_operations_in_operators(s, 0, 3)

        self.assertEqual(['*', '*'], s[:t1])
        self.assertEqual(['4', '6', '7'], n[:t2])


if __name__ == '__main__':
    unittest.main()
