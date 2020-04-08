import unittest
import time
from calculator.calculator import evaluate
from memory_profiler import profile


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
        self.assertEqual(r, 41334326161)

    def test_exponent(self):
        t2 = '2^(2*4)*5 +2'
        r = evaluate(t2)
        self.assertEqual(r, 1282)

    def test_simple(self):
        t3 = '(1+1)'
        r = evaluate(t3)
        self.assertEqual(r, 2)

    def test_with_python_eval(self):
        t = '2*5 + (5*(1+8)-9*3) + (1 + 99 * 8) + 22'
        self.assertEqual(evaluate(t), eval(t))


def stress(t):
    start = time.time()
    tps = 0
    while time.time() - start < 1:
        evaluate(t)
        tps += 1

    print('tps: ' + str(tps) + '\n')


if __name__ == '__main__':
    unittest.main()
