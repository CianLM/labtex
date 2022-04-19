from labtex import *
import unittest

# Measurement Class 
x = Measurement(1.1,0.3,"m")
y = Measurement(2.22,0.4,"m")
z = Measurement(314,10,"V")

class TestMeasurementClass(unittest.TestCase):

    def test_addition(self):
        self.assertTrue( repr(x + y) == repr(y + x) == "3.3 ± 0.5 m")
        self.assertTrue( repr(z + 3) == repr(3 + z) == "(32 ± 1) × 10^{1} V" )

    def test_subtraction(self):
        self.assertEqual( repr(x - y), "-1.1 ± 0.5 m")
        self.assertEqual( repr(y - x), "1.1 ± 0.5 m")

        self.assertEqual( repr(z - 3), "(31 ± 1) × 10^{1} V")
        self.assertEqual( repr(3 - z), "(-31 ± 1) × 10^{1} V")

    def test_multiplication(self):
        self.assertTrue( repr(x * y) == repr(y * x) == "2.4 ± 0.8 m^2")
        self.assertTrue( repr(x * z) == repr(z * x) == "(35 ± 9) × 10^{1} V m")
        self.assertTrue( repr(z * 3) == repr(3 * z) == "(94 ± 3) × 10^{1} V")

    def test_division(self):
        self.assertEqual( repr(x / y), "0.5 ± 0.2 ")
        self.assertEqual( repr(x / z), "(4 ± 1) × 10^{-3} V^{-1} m")
        self.assertEqual( repr(z / 3), "105 ± 3 V")
        self.assertEqual( repr(3 / z), "(96 ± 3) × 10^{-4} V^{-1}")

    def test_exponentiation(self):
        self.assertTrue( repr(x * x) == repr(x ** 2) == "1.2 ± 0.7 m^2")
        self.assertEqual( repr(2 ** (x / y) ), "1.4 ± 0.2 ")

    def test_functions(self):
        self.assertEqual( repr(Measurement.sin(x/y)), "0.5 ± 0.1 ")
        self.assertEqual( repr(Measurement.cos(x/y)), "0.88 ± 0.08 ")
        self.assertEqual( repr(Measurement.tan(x/y)), "0.5 ± 0.2 ")
        self.assertEqual( repr(Measurement.log(x/y)), "-0.7 ± 0.3 ")
        self.assertEqual( repr(Measurement.asin(x/y)), "0.5 ± 0.2 ")
        self.assertEqual( repr(Measurement.acos(x/y)), "1.1 ± 0.2 ")
        self.assertEqual( repr(Measurement.atan(x/y)), "0.5 ± 0.2 ")

    def test_conversion(self):
        self.assertEqual( repr(Measurement(2,1,'cm^3').to('m^3')), "(2 ± 1) × 10^{-6} m^3")
        self.assertEqual( repr(x.to('cm')), "(11 ± 3) × 10^{1} cm")
        self.assertEqual( Measurement(1,0,"m^3 Pa / J Hz^3 s^3").to('').value, 1)

    def test_exceptions(self):
        with self.assertRaises(Exception):
            x + z
        with self.assertRaises(Exception):
            z - x
        with self.assertRaises(Exception):
            Measurement.sin(x)
        
