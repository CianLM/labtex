import unittest

# from unit import Unit
# from measurement import Measurement, MeasurementList
# from linear import LinearRegression
# from document import Document
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
        self.assertEqual(repr(Unit("kgm^2 AJ^-10")), "kg A J^-10 m^2")

    def test_maxparsing(self):
        self.assertEqual( 
            repr(Unit("ng^-5us^-4mA^-3cK^-2C^-1kJ^1MV^2N^3GW^4T^5Pa^6Hzm^101")),
            "ng^-5 us^-4 mA^-3 cK^-2 C^-1 kJ^1 MV^2 N^3 GW^4 T^5 Pa^6 Hz m^101"
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
        self.assertEqual( repr(x / z), "0.004 ± 0.001 V^-1 m")
        self.assertEqual( repr(z / 3), "105 ± 3 V")
        self.assertEqual( repr(3 / z), "0.0096 ± 0.0003 V^-1")

    def test_exponentiation(self):
        self.assertTrue( repr(x * x) == repr(x ** 2) == "1.2 ± 0.7 m^2")
        self.assertEqual( repr(2 ** x), "2.1 ± 0.6 ")

    def test_functions(self):
        self.assertEqual( repr(Measurement.sin(x)), "0.9 ± 0.1 ")
        self.assertEqual( repr(Measurement.cos(x)), "0.5 ± 0.3 ")
        self.assertEqual( repr(Measurement.tan(x)), "2 ± 1 ")
        self.assertEqual( repr(Measurement.log(x)), "0.1 ± 0.3 ")
        self.assertEqual( repr(Measurement.asin(x/2)), "0.6 ± 0.2 ")
        self.assertEqual( repr(Measurement.acos(x/2)), "1.0 ± 0.2 ")
        self.assertEqual( repr(Measurement.atan(x/2)), "0.5 ± 0.2 ")



heights = MeasurementList([185,183,182,194,184,177],5,"cm")

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
            repr(200 / heights), "[1.08, 1.09, 1.1, 1.03, 1.09, 1.13] ± 0.03 cm^-1"
        )

    def test_exponentiation(self):
        self.assertEqual(
            repr(heights ** 2), "[34000, 33000, 33000, 38000, 34000, 31000] ± 2000 cm^2"
        )

    def test_functions(self):
        self.assertEqual(
            repr(MeasurementList.sin(heights)), "[0, 1, 0, -1, 1, 1] ± 4 "
        )
        self.assertEqual(
            repr(MeasurementList.cos(heights)), "[-1, 1, 1, 1, 0, 0] ± 4 "
        )
        self.assertEqual(
            repr(MeasurementList.tan(heights)), "[0, 0, 0, 0, 0, 0] ± 100 "
        )
        self.assertEqual(
            repr(MeasurementList.log(heights)), "[5.22, 5.21, 5.2, 5.27, 5.21, 5.18] ± 0.03 "
        )
        self.assertEqual(
            repr(MeasurementList.asin(heights/200)), "[1.2, 1.2, 1.1, 1.3, 1.2, 1.1] ± 0.1 "
        )
        self.assertEqual(
            repr(MeasurementList.acos(heights/200)), "[0.4, 0.4, 0.4, 0.2, 0.4, 0.5] ± 0.1 "
        )
        self.assertEqual(
            repr(MeasurementList.atan(heights/200)), "[0.7, 0.7, 0.7, 0.8, 0.7, 0.7] ± 0.1 "
        )

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
            repr(t / heights), "[0.027, 0.027, 0.027, 0.026, 0.027, 0.028] ± 0.001 " 
        )
        self.assertEqual(
            repr(heights / t), "[37, 37, 36, 39, 37, 35] ± 1 "
        ) 

# Two MeasurementLists to be used in the rest of the tests
voltages = MeasurementList([1.33333,3,5,7,8.5,10],1,"V")
temperatures = MeasurementList([23,55,67,82,88,96],5,"C")




# Linear Regression

# eq = LinearRegression(voltages,temperatures)
# print(eq)



# Latex template creation
# doc = Document(title = "Lab Report Template",author = "CianLM")

# print(MeasurementList.sin(voltages))


# doc.table(
#     listheads = ["Voltage, V","Temperature, T"],
#     data = [voltages,temperatures],
#     # headers = ["Variables","Data"],
#     caption = "Voltage Temperature Correlation"
# )

# doc.table(
#     listheads = ["Voltage, V","Temperature, T"],
#     data = [voltages,temperatures],
#     caption = "Voltage Temperature Correlation",
#     style = "upright"
# )

# doc.graph(
#     data = [voltages,temperatures],
#     title = "Voltage Temperature Correlation",
#     xnameandsymbol = "Voltage, V",
#     ynameandsymbol = "Temperature, T",
#     caption = "Linear Regression of Voltage and Temperature"
# )

# doc.save("test")

if __name__ == '__main__':
    unittest.main(verbosity=2)