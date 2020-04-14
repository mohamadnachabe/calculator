from calculator.calculator_optimisation import evaluate_o
from calculator.calculator import evaluate
from memory_profiler import profile
import unittest
import time

from calculator.utils import find_operation_up_to_next_add_or_sub, find_operations_in_operators


class TestCalculator(unittest.TestCase):

    @profile
    def test_complex(self):
        t1 = '(4 + 4) * 344 + (((6 + 7) * 1333) + 2 + 100000) * (30 + 2 - 9 + 30 + 2)' \
             ' + (4 + 4) * 344 * (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)' \
             ' + (4 + 4) * 344 * (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)' \
             ' + (4 + 4) * 344 * (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)' \
             ' + (4 + 4) * 344 * (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)' \
             ' + (4 + 4) * 344 + (((6 + 7) * 1333)) '
        r = evaluate_o(t1)
        self.assertEqual(r, eval(t1))

    def test_exponent(self):
        t2 = '2^(2+2+2) + 2 - 2 + 2'
        r = evaluate_o(t2)
        self.assertEqual(r, 66)

    def test_simple(self):
        t3 = '(1+1)'
        r = evaluate_o(t3)
        self.assertEqual(r, eval(t3))

    def test_with_python_eval(self):
        t = '5+8-9*3'
        self.assertEqual(eval(t), evaluate_o(t))

    def test_with_python_eval__(self):
        t = '8-9*3'
        print(evaluate_o(t))
        self.assertEqual(eval(t), evaluate_o(t))

    def test_exp(self):
        t = '(4 + 4) * 344 + ( ((6 + 7) * 1333) + 2 + 100000 ) * (30 + 2)'
        self.assertEqual(evaluate_o(t), eval(t))

    def test_exp69(self):
        t = '(6 + 7) + (30 + 2)'
        self.assertEqual(evaluate_o(t), eval(t))

    def test_exp60(self):
        t = '(6 + 7) * (30 + 2)'
        self.assertEqual(evaluate_o(t), eval(t))

    def test_exp_dup(self):
        t = '((6 + 7) * 1333) + (2 + 100000) - 9 * 9 '
        self.assertEqual(evaluate_o(t), eval(t))

    def test_exp_3(self):
        t = '4*6*7*9-1-2-6-8+2+(4+5)+7*1-8+6+6+20*4*6*7*9-1-2-6-8+2+(4+5)+7*1-8+6+6+204*6*7*9-1-2-6-8+2+(4+5)+7*1-8+6'

        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate_o, t)

        print(evaluate_o.__name__ + ' is ' + "{:.2f}".format(t2 / t1) + ' times slower than ' + eval.__name__)

        self.assertEqual(a1, a2)

    def test_exp_4(self):
        t = '(9-1)-(8+2)'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate_o, t)

        print(evaluate_o.__name__ + ' is ' + "{:.2f}".format(t2 / t1) + ' times slower than ' + eval.__name__)

        self.assertEqual(a1, a2)

    def test_exp_44(self):
        t = '4*6*7*(9-1)-2-6-(8+2)+(4+5)+7*1-8+6+6+20'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate, t)

        self.assertEqual(a1, a2)

    def test_exp_5(self):
        t = '4*6*7*9.8-1-2-6.6'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate_o, t)

        self.assertEqual(a1, a2)

    def test_exp_compare_with_other_impl(self):
        t = '4*6*7.666*9-1-2-6-8+2+(4+5)+7*1-8+6+6+20'
        a1, t1 = execute_timed(evaluate, t)
        a2, t2 = execute_timed(evaluate_o, t)
        a2, t3 = execute_timed(eval, t)

        print(evaluate_o.__name__ + ' is ' + "{:.2f}".format(t2 / t3) + ' times slower than ' + eval.__name__)
        print(evaluate_o.__name__ + ' is ' + "{:.2f}".format(t1 / t2) + ' times faster than ' + evaluate.__name__)
        print(evaluate.__name__ + ' is ' + "{:.2f}".format(t1 / t3) + ' times slower than ' + eval.__name__)

        self.assertEqual(a1, a2)

    def test_exp_hard(self):
        t = '77 - 3 * 4 * (12-2) + 11'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate_o, t)

        self.assertEqual(a1, a2)

    def test_exp_hard_tt(self):
        t = '1 - (5-5) + 5.5'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate_o, t)

        self.assertEqual(a1, a2)

    def test_exp_hard_t(self):
        t = '1 - (5-5)'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate_o, t)

        self.assertEqual(a1, a2)

    def test_exp_hard_4(self):
        t = '77 - (12-2)'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate_o, t)

        self.assertEqual(a1, a2)

    def test_exp_hard_2(self):
        t = '1 - 3 * 12 * 2'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate_o, t)

        self.assertEqual(a1, a2)

    def test_exp_division(self):
        t = '1/3 + 1/(2*7)*8'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate_o, t)

        print(a2)

        self.assertEqual(a1, a2)

    def test_(self):
        t = '2*2*2*2*2*64 + 5'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate_o, t)

        print(a2)

        self.assertEqual(a1, a2)

    def test_op(self):
        operations = ['-', '*', '*']
        numbers = ['2', '4', '5', '5']
        os = 0
        i = find_operation_up_to_next_add_or_sub(operations, os + 1)
        j = find_operations_in_operators(operations, os, i) + 1

        self.assertEqual(2, i)
        self.assertEqual(j, 3)

    def test_double_map(self):
        d = {}
        d['test'] = {}
        d['test']['one'] = 'two'


def stress(t):
    start = time.time()
    tps = 0
    while time.time() - start < 1:
        evaluate_o(t)
        tps += 1

    print('tps: ' + str(tps) + '\n')


def execute_timed(func, arg):
    start = time.time()
    result = func(arg)
    elapsed = time.time() - start
    return result, elapsed


if __name__ == '__main__':
    unittest.main()
