# To run tests, if you are in the root of the project:
#   source test/venv/bin/activate
#   python3 -m unittest test.testing
# These commands activate a virtual environment and run this script respectively.

import unittest

from labtex import *


# Unit Class
class TestUnitClass(unittest.TestCase):

    def test_powerparsing(self):
        self.assertEqual(repr(Unit("m^2")), "m^2")
    
    def test_prefixparsing(self):
        self.assertEqual(repr(Unit("um")), "um")

    def test_mmparsing(self):
        self.assertEqual(repr(Unit("mm^2")), "mm^2")

    def test_generalparsing(self):
        self.assertEqual(repr(Unit("kgm^2 AJ^-10")), "kg A J^{-10} m^2")

    def test_maxparsing(self):
        self.assertEqual( 
            repr(Unit("ng^-5us^-4mA^-3cK^-2C^-1kJ^1MV^2N^3GW^4T^5Pa^6Hzm^101")),
            "ng^{-5} us^{-4} mA^{-3} cK^{-2} C^{-1} kJ MV^2 N^3 GW^4 T^5 Pa^6 Hz m^101"
    )
    
    def test_exceptions(self):
        with self.assertRaises(Exception):
            Unit("u")
        with self.assertRaises(Exception):
            Unit("m^2f")
        with self.assertRaises(Exception):
            Unit("5")
        with self.assertRaises(Exception):
            Unit("^5")
        with self.assertRaises(Exception):
            Unit("q^5")

    def test_methods(self):
        self.assertTrue(Unit.unitless(Unit("")))
        self.assertTrue(not Unit.unitless(Unit("m")))

        self.assertTrue(Unit.singular(Unit("m^2")))
        self.assertTrue(not Unit.singular(Unit("Vm")))

    def unit_conversion(self):
        self.assertTrue(
            Unit("m") * 1e-9 == 1e-9 * Unit("m") == Unit("m") / 1e9 == 1e-9 / Unit("m^-1") == Unit("nm")
        )
        self.assertTrue(
            Unit("mm^2") * 1e-4 == Unit("m^2")
        )
        self.assertTrue(
            Unit("mm^-2") * 1e-4 == Unit("m^-2")
        )


# Measurement Class 
x = Measurement(1.1,0.3,"m")
y = Measurement(2.22,0.4,"m")
z = Measurement(314,10,"V")

class TestMeasurementClass(unittest.TestCase):

    def test_addition(self):
        self.assertTrue( repr(x + y) == repr(y + x) == "3.3 ± 0.5 m")
        self.assertTrue( repr(z + 3) == repr(3 + z) == "320 ± 10 V" )

    def test_subtraction(self):
        self.assertEqual( repr(x - y), "-1.1 ± 0.5 m")
        self.assertEqual( repr(y - x), "1.1 ± 0.5 m")

        self.assertEqual( repr(z - 3), "310 ± 10 V")
        self.assertEqual( repr(3 - z), "-310 ± 10 V")

    def test_multiplication(self):
        self.assertTrue( repr(x * y) == repr(y * x) == "2.4 ± 0.8 m^2")
        self.assertTrue( repr(x * z) == repr(z * x) == "340 ± 90 V m")
        self.assertTrue( repr(z * 3) == repr(3 * z) == "940 ± 30 V")

    def test_division(self):
        self.assertEqual( repr(x / y), "0.5 ± 0.2 ")
        self.assertEqual( repr(x / z), "(4 ± 1) × 10^{-3} V^{-1} m")
        self.assertEqual( repr(z / 3), "105 ± 3 V")
        self.assertEqual( repr(3 / z), "(96 ± 4) × 10^{-4} V^{-1}")

    def test_exponentiation(self):
        self.assertTrue( repr(x * x) == repr(x ** 2) == "1.2 ± 0.7 m^2")
        self.assertEqual( repr(2 ** x), "2.1 ± 0.6 ")

    def test_functions(self):
        self.assertEqual( repr(Measurement.sin(x/y)), "0.5 ± 0.1 ")
        self.assertEqual( repr(Measurement.cos(x/y)), "0.88 ± 0.08 ")
        self.assertEqual( repr(Measurement.tan(x/y)), "0.5 ± 0.2 ")
        self.assertEqual( repr(Measurement.log(x/y)), "-0.7 ± 0.3 ")
        self.assertEqual( repr(Measurement.asin(x/y)), "0.5 ± 0.2 ")
        self.assertEqual( repr(Measurement.acos(x/y)), "1.1 ± 0.2 ")
        self.assertEqual( repr(Measurement.atan(x/y)), "0.5 ± 0.2 ")

    def test_exceptions(self):
        with self.assertRaises(Exception):
            x + z
        with self.assertRaises(Exception):
            z - x
        with self.assertRaises(Exception):
            Measurement.sin(x)
        


heights = MeasurementList([185,183,182,194,184,177],5,"cm")
maxheight = Measurement(200,5,"cm")

class TestMeasurementListClass(unittest.TestCase):

    def test_print(self):
        self.assertEqual(
            repr(heights), "[185, 183, 182, 194, 184, 177] ± 5 cm"
        )
    
    def test_addition(self):
        self.assertTrue(
            repr(heights + 1) ==  repr(1 + heights) == "[186, 184, 183, 195, 185, 178] ± 5 cm"
        )

    def test_subtraction(self):
        self.assertEqual(
            repr(heights - 1), "[184, 182, 181, 193, 183, 176] ± 5 cm"
        )
        self.assertEqual(
            repr(200 - heights), "[15, 17, 18, 6, 16, 23] ± 5 cm"
        )

    def test_multiplication(self):
        self.assertTrue(
            repr(heights * 10) == repr(10 * heights) == "[1850, 1830, 1820, 1940, 1840, 1770] ± 50 cm" 
        )

    def test_division(self):
        self.assertEqual(
            repr(heights / 100), "[1.85, 1.83, 1.82, 1.94, 1.84, 1.77] ± 0.05 cm"
        )
        self.assertEqual(
            repr(200 / heights), "[1.08, 1.09, 1.1, 1.03, 1.09, 1.13] ± 0.03 cm^{-1}"
        )

    def test_exponentiation(self):
        self.assertEqual(
            repr(heights ** 2), "([34, 33, 33, 38, 34, 31] ± 2) × 10^{3} cm^2"
        )

    def test_functions(self):
        self.assertEqual(
            repr(MeasurementList.sin(heights/maxheight)), "[0.8, 0.79, 0.79, 0.82, 0.8, 0.77] ± 0.02 "
        )
        self.assertEqual(
            repr(MeasurementList.cos(heights/maxheight)), "[0.6, 0.61, 0.61, 0.57, 0.61, 0.63] ± 0.03 "
        )
        self.assertEqual(
            repr(MeasurementList.tan(heights/maxheight)), "[1.3, 1.3, 1.3, 1.5, 1.3, 1.2] ± 0.1 "
        )
        self.assertEqual(
            repr(MeasurementList.log(heights/maxheight)), "[-0.08, -0.09, -0.09, -0.03, -0.08, -0.12] ± 0.04 "
        )
        self.assertEqual(
            repr(MeasurementList.asin(heights/maxheight)), "[1.2, 1.2, 1.1, 1.3, 1.2, 1.1] ± 0.1 "
        )
        self.assertEqual(
            repr(MeasurementList.acos(heights/maxheight)), "[0.4, 0.4, 0.4, 0.2, 0.4, 0.5] ± 0.1 "
        )
        self.assertEqual(
            repr(MeasurementList.atan(heights/maxheight)), "[0.7, 0.7, 0.7, 0.8, 0.7, 0.7] ± 0.1 "
        )
    def test_exceptions(self):
        with self.assertRaises(Exception):
            heights + MeasurementList([3],0.1,"V")
        with self.assertRaises(Exception):
            Measurement.sin(heights)

#Measurement and MeasurementList Interactions 
t = Measurement(5,0.1,"cm")

class TestMeasurementandListInteractions(unittest.TestCase):
    
    def test_addition(self):
        self.assertTrue(
            repr(t + heights) ==  repr(heights + t) == "[190, 188, 187, 199, 189, 182] ± 5 cm"
        )

    def test_subtraction(self):
        self.assertEqual(
            repr(t - heights), "[-180, -178, -177, -189, -179, -172] ± 5 cm"
        )
        self.assertEqual(
            repr(heights - t), "[180, 178, 177, 189, 179, 172] ± 5 cm"
        )

    def test_multiplication(self):
        self.assertTrue(
            repr(t * heights) == repr(heights * t) == "[920, 920, 910, 970, 920, 880] ± 30 cm^2"
        )
    
    def test_division(self):
        self.assertEqual(
            repr(t / heights), "([27, 27, 27, 26, 27, 28] ± 1) × 10^{-3} " 
        )
        self.assertEqual(
            repr(heights / t), "[37, 37, 36, 39, 37, 35] ± 1 "
        ) 

    def test_exceptions(self):
        with self.assertRaises(Exception):
            heights + Measurement(101300,1e3,"Pa")


# Two MeasurementLists to be used in the rest of the tests
voltages = MeasurementList([1.3,3,5,7,8.5,10],1,"V")
temperatures = MeasurementList([23,55,67,82,88,96],5,"C")




# Linear Regression
eq = LinearRegression(voltages,temperatures)

class TestLinearRegression(unittest.TestCase):
    def test_repr(self):
        self.assertTrue(
            LinearRegression.__repr__(eq) == "m = 8 ± 1 C V^{-1}\nc = 23 ± 6 C"
        )



# Template file creation is hard to test as it involves file creation, so this portion is tested manually.
# Latex template creation
doc = Document(title = "Lab Report Template",author = "CianLM")

doc.table(
    listheads = ["Voltage, V","Temperature, T"],
    data = [voltages,temperatures],
    # headers = ["Variables","Data"],
    caption = "Voltage Temperature Correlation"
)

doc.table(
    listheads = ["Voltage, V","Temperature, T"],
    data = [voltages,temperatures**2],
    caption = "Voltage Temperature Correlation",
    style = "upright"
)

doc.graph(
    data = [voltages,temperatures],
    title = "Voltage Temperature Correlation",
    xnameandsymbol = "Voltage, V",
    ynameandsymbol = "Temperature, T",
    caption = "Linear Regression of Voltage and Temperature"
)

doc.graph(
    data = [voltages,temperatures**2],
    title = "Voltage Temperature Correlation",
    xnameandsymbol = "Voltage, V",
    ynameandsymbol = "Temperature$^2$, $T^2$",
    caption = "Linear Regression of Voltage and Temperature"
)

doc.save("test")

if __name__ == '__main__':
    unittest.main(verbosity=2)