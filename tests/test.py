from calculator.calculator import evaluate
from memory_profiler import profile
import unittest
import time


class TestCalculator(unittest.TestCase):

    @profile
    def test_complex(self):
        t1 = '(4 + 4) * 344 + (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)' \
             ' + (4 + 4) * 344 * (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)' \
             ' + (4 + 4) * 344 * (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)' \
             ' + (4 + 4) * 344 * (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)' \
             ' + (4 + 4) * 344 * (((6 + 7) * 1333) + 2 + 100000) * (30 + 2)' \
             ' + (4 + 4) * 344 + (((6 + 7) * 1333)) '
        r = evaluate(t1)
        self.assertEqual(r, eval(t1))

    def test_exponent(self):
        t2 = '2^2*4*5 +2'
        r = evaluate(t2)
        self.assertEqual(r, 82)

    def test_with_python_eval1(self):
        t = '2*5 + 5*1+8-9*3 - 2*5 + 5*1+8-9*3'
        self.assertEqual(eval(t), evaluate(t))

    def test_simple(self):
        t3 = '(1+1)'
        r = evaluate(t3)
        self.assertEqual(r, eval(t3))

    def test_with_python_eval(self):
        t = '2*5 + 5*1+8-9*3 + 1 + 99 * 8 + 22'
        self.assertEqual(evaluate(t), eval(t))

    def test_with_python_eval3(self):
        t = '2*5 + 5*1+8-9*3 + 1 + 99 * 8 + 22 + (5*7*7*9-9-0-8+7+5+(8+9)*7)'
        self.assertEqual(evaluate(t), eval(t))

    def test_exp(self):
        t = '(4 + 4) * 344 + ( ((6 + 7) * 1333) + 2 + 100000 ) * (30 + 2)'
        self.assertEqual(evaluate(t), eval(t))

    def test_exp_3(self):
        t = '4*6*7*9-1-2-6-8+2+(4+5)+7*1-8+6+6+20*4*6*7*9-1-2-6-8+2+(4+5)+7*1-8+6+6+204*6*7*9-1-2-6-8+2+(4+5)+7*1-8+6'

        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate, t)

        print(evaluate.__name__ + ' is ' + "{:.2f}".format(t2 / t1) + ' times slower than ' + eval.__name__)

        self.assertEqual(a1, a2)

    def test_exp_4(self):
        t = '4*6*7*9-1-2-6-8+2+(4+5)+7*1-8+6+6+20'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate, t)

        self.assertEqual(a1, a2)

    def test_exp_hard(self):
        t = '77 - 3 * 4 * (12-2) + 11'
        a1, t1 = execute_timed(eval, t)
        a2, t2 = execute_timed(evaluate, t)

        self.assertEqual(a1, a2)

    def test_sub_prec(self):
        t = '1+5+7-9+2-9'

        self.assertEqual(evaluate(t), eval(t))


def stress(t):
    start = time.time()
    tps = 0
    while time.time() - start < 1:
        evaluate(t)
        tps += 1

    print('tps: ' + str(tps) + '\n')


def execute_timed(func, arg):
    start = time.time()
    result = func(arg)
    elapsed = time.time() - start
    return result, elapsed


if __name__ == '__main__':
    unittest.main()
