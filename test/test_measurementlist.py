from labtex import * 
import unittest

heights = MeasurementList([185,183,182,194,184,177],[5,4,5,6,7,10],"cm")
maxheight = Measurement(200,5,"cm")

class TestMeasurementListClass(unittest.TestCase):

    def test_print(self):
        self.assertEqual(
            repr(heights), "[185 ± 5, 183 ± 4, 182 ± 5, 194 ± 6, 184 ± 7, (18 ± 1) × 10^{1}] cm"
        )
    
    def test_addition(self):
        self.assertTrue(
            repr(heights + 1) ==  repr(1 + heights) == "[186 ± 5, 184 ± 4, 183 ± 5, 195 ± 6, 185 ± 7, (18 ± 1) × 10^{1}] cm"
        )

    def test_subtraction(self):
        self.assertEqual(
            repr(heights - 1), "[184 ± 5, 182 ± 4, 181 ± 5, 193 ± 6, 183 ± 7, (18 ± 1) × 10^{1}] cm"
        )
        self.assertEqual(
            repr(200 - heights), "[15 ± 5, 17 ± 4, 18 ± 5, 6 ± 6, 16 ± 7, (2 ± 1) × 10^{1}] cm"
        )

    def test_multiplication(self):
        self.assertTrue(
            repr(heights * 10) == repr(10 * heights) == "[(185 ± 5) × 10^{1}, (183 ± 4) × 10^{1}, (182 ± 5) × 10^{1}, (194 ± 6) × 10^{1}, (184 ± 7) × 10^{1}, (18 ± 1) × 10^{2}] cm" 
        )

    def test_division(self):
        self.assertEqual(
            repr(heights / 100), "[1.85 ± 0.05, 1.83 ± 0.04, 1.82 ± 0.05, 1.94 ± 0.06, 1.84 ± 0.07, 1.8 ± 0.1] cm"
        )
        self.assertEqual(
            repr(200 / heights), "[1.08 ± 0.03, 1.09 ± 0.02, 1.1 ± 0.03, 1.03 ± 0.03, 1.09 ± 0.04, 1.13 ± 0.06] cm^{-1}"
        )

    def test_exponentiation(self):
        self.assertEqual(
            repr(heights ** 2), "[(34 ± 2) × 10^{3}, (33 ± 1) × 10^{3}, (33 ± 2) × 10^{3}, (38 ± 2) × 10^{3}, (34 ± 3) × 10^{3}, (31 ± 4) × 10^{3}] cm^2"
        )
        self.assertEqual(
            repr( 10 ** (heights / maxheight)), "[8.4 ± 0.3, 8.2 ± 0.2, 8.1 ± 0.3, 9.3 ± 0.4, 8.3 ± 0.3, 7.7 ± 0.4] "
        )

    def test_functions(self):
        self.assertEqual(
            repr(MeasurementList.sin(heights/maxheight)), "[0.8 ± 0.02, 0.79 ± 0.02, 0.79 ± 0.02, 0.82 ± 0.02, 0.8 ± 0.03, 0.77 ± 0.03] "
        )
        self.assertEqual(
            repr(MeasurementList.cos(heights/maxheight)), "[0.6 ± 0.03, 0.61 ± 0.02, 0.61 ± 0.03, 0.57 ± 0.03, 0.61 ± 0.03, 0.63 ± 0.04] "
        )
        self.assertEqual(
            repr(MeasurementList.tan(heights/maxheight)), "[1.33 ± 0.09, 1.3 ± 0.08, 1.29 ± 0.09, 1.5 ± 0.1, 1.3 ± 0.1, 1.2 ± 0.1] "
        )
        self.assertEqual(
            repr(MeasurementList.log(heights/maxheight)), "[-0.08 ± 0.04, -0.09 ± 0.03, -0.09 ± 0.04, -0.03 ± 0.04, -0.08 ± 0.05, -0.12 ± 0.06] "
        )
        self.assertEqual(
            repr(MeasurementList.asin(heights/maxheight)), "[1.18 ± 0.09, 1.16 ± 0.08, 1.14 ± 0.08, 1.3 ± 0.2, 1.2 ± 0.1, 1.1 ± 0.1] "
        )
        self.assertEqual(
            repr(MeasurementList.acos(heights/maxheight)), "[0.39 ± 0.09, 0.42 ± 0.08, 0.43 ± 0.08, 0.2 ± 0.2, 0.4 ± 0.1, 0.5 ± 0.1] "
        )
        self.assertEqual(
            repr(MeasurementList.atan(heights/maxheight)), "[0.75 ± 0.09, 0.74 ± 0.08, 0.74 ± 0.08, 0.8 ± 0.2, 0.7 ± 0.1, 0.7 ± 0.1] "
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
            repr(t + heights) ==  repr(heights + t) == "[190 ± 5, 188 ± 4, 187 ± 5, 199 ± 6, 189 ± 7, (18 ± 1) × 10^{1}] cm"
        )

    def test_subtraction(self):
        self.assertEqual(
            repr(t - heights), "[-180 ± 5, -178 ± 4, -177 ± 5, -189 ± 6, -179 ± 7, (-17 ± 1) × 10^{1}] cm"
        )
        self.assertEqual(
            repr(heights - t), "[180 ± 5, 178 ± 4, 177 ± 5, 189 ± 6, 179 ± 7, (17 ± 1) × 10^{1}] cm"
        )

    def test_multiplication(self):
        self.assertTrue(
            repr(t * heights) == repr(heights * t) == "[(92 ± 3) × 10^{1}, (92 ± 3) × 10^{1}, (91 ± 3) × 10^{1}, (97 ± 4) × 10^{1}, (92 ± 4) × 10^{1}, (88 ± 5) × 10^{1}] cm^2"
        )
    
    def test_division(self):
        self.assertEqual(
            repr(t / heights), "[(270 ± 9) × 10^{-4}, (273 ± 8) × 10^{-4}, (275 ± 9) × 10^{-4}, (258 ± 9) × 10^{-4}, (27 ± 1) × 10^{-3}, (28 ± 2) × 10^{-3}] " 
        )
        self.assertEqual(
            repr(heights / t), "[37 ± 1, 37 ± 1, 36 ± 1, 39 ± 1, 37 ± 2, 35 ± 2] "
        ) 

    def test_exceptions(self):
        with self.assertRaises(Exception):
            heights + Measurement(101300,1e3,"Pa")

