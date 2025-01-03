import unittest
from calc_functions import Calculator


class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(10), 10)
        self.assertEqual(self.calc.add(5), 15)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(5), -5)
        self.assertEqual(self.calc.subtract(10), -15)

    def test_multiply(self):
        self.calc.add(10)
        self.assertEqual(self.calc.multiply(5), 50)
        self.assertEqual(self.calc.multiply(0), 0)

    def test_divide(self):
        self.calc.add(10)
        self.assertEqual(self.calc.divide(2), 5)
        self.assertEqual(self.calc.divide(2), 2.5)

    def test_memory_operations(self):
        self.calc.memory_add(10)
        self.assertEqual(self.calc.memory, 10)
        self.calc.memory_subtract(5)
        self.assertEqual(self.calc.memory, 5)
        self.calc.memory_clear()
        self.assertEqual(self.calc.memory, 0)
        self.calc.add(20)
        self.calc.memory_add(self.calc.current_value)
        self.assertEqual(self.calc.memory_recall(), 20)

    def test_ceil(self):
        self.calc.add(10.1)
        self.assertEqual(self.calc.ceil(), 11)

    def test_sqrt(self):
        self.calc.add(16)
        self.assertEqual(self.calc.sqrt(), 4)
        with self.assertRaises(ValueError):
            self.calc.subtract(20)
            self.calc.sqrt()

    def test_remainder(self):
        self.calc.add(10)
        self.assertEqual(self.calc.remainder(3), 1)
        with self.assertRaises(ValueError):
            self.calc.remainder(0)

    def test_trigonometry(self):
        self.calc.add(90)
        self.assertAlmostEqual(self.calc.sin(), 1.0, places=5)
        self.calc.clear()
        self.calc.add(0)
        self.assertAlmostEqual(self.calc.cos(), 1.0, places=5)

    def test_pow(self):
        self.calc.add(2)
        self.assertEqual(self.calc.pow(3), 8)

    def test_floor(self):
        self.calc.add(10.9)
        self.assertEqual(self.calc.floor(), 10)

    def test_clear(self):
        self.calc.add(100)
        self.assertEqual(self.calc.clear(), 0)


if __name__ == '__main__':
    unittest.main()