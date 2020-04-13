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

    def test_find_index_of_closing_bracket(self):
        t = u.find_index_of_closing_bracket(['(', '+', '(', '*', '+', '(', '-', ')', ')', '+', ')', '-', '+'], 2)
        self.assertEqual(8, t)

    def test_find_index_of_closing_bracket_2(self):
        t = u.find_index_of_closing_bracket(['(', '+', '(', '*', '+', '(', '-', ')', ')', '+', ')', '-', '+'], 0)
        self.assertEqual(10, t)

    def test_find_index_of_closing_bracket_3(self):
        t = u.find_index_of_closing_bracket(['(', '+', '(', '*', '+', '(', '-', ')', ')', '+', ')', '-', '+'], 5)
        self.assertEqual(7, t)

    def test_find_operations_in_operators(self):
        t = '(1+2+(3+4+5))'
        po = u.parse_operators(t)
        o = u.find_numbers_between_operators(po, 0, 7)
        self.assertEqual(5, o)

    def test_find_operations_in_operators11(self):
        t = '3 * 4 * (12-2)'
        po = u.parse_operators(t)
        o = u.find_numbers_between_operators(po, 0, 4)
        self.assertEqual(4, o)

    def test_find_operations_in_operators_2(self):
        t = '(1+2+3+4+5)'
        po = u.parse_operators(t)
        o = u.find_numbers_between_operators(po, 0, 5)
        self.assertEqual(5, o)

    def test_find_operations_in_operators_3(self):
        t = '((1+2)+((3+4)+5))'
        po = u.parse_operators(t)
        o = u.find_numbers_between_operators(po, 0, 11)
        self.assertEqual(5, o)

    def test_find_operations_in_operators_4(self):
        t = '((1+2)+((3+4)+5))'
        po = u.parse_operators(t)
        o = u.find_numbers_between_operators(po, 5, 10)
        self.assertEqual(3, o)

    def test_find_operations_in_operators_5(self):
        t = '((1+2)+((3+4)+5+9))'
        po = u.parse_operators(t)
        o = u.find_numbers_between_operators(po, 5, 11)
        self.assertEqual(4, o)

    def test_find_operations_in_operators_6(self):
        t = '1+2+2'
        po = u.parse_operators(t)
        o = u.find_numbers_between_operators(po, 0, 1)
        self.assertEqual(3, o)


if __name__ == '__main__':
    unittest.main()
