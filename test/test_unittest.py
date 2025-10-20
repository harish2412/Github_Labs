import math
import unittest
from src.bmi import calc_bmi, categorize_bmi

class TestBMI(unittest.TestCase):
    def test_calc_metric(self):
        self.assertTrue(math.isclose(calc_bmi(80, 1.80), 24.6913580247, rel_tol=1e-9))

    def test_calc_imperial(self):
        self.assertTrue(math.isclose(calc_bmi(180, 70, unit="imperial"), 25.8244897959, rel_tol=1e-9))

    def test_category_normal(self):
        self.assertEqual(categorize_bmi(22.0), "Normal")

    def test_bad_unit(self):
        with self.assertRaises(ValueError):
            calc_bmi(60, 1.70, unit="unknown")

if __name__ == "__main__":
    unittest.main()
