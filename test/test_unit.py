from labtex import *
import unittest

# Unit Class
class TestUnitClass(unittest.TestCase):

    def test_powerparsing(self):
        self.assertEqual(repr(Unit("m^2")), "m^2")
    
    def test_prefixparsing(self):
        self.assertEqual(repr(Unit("um")), "um")

    def test_mmparsing(self):
        self.assertEqual(repr(Unit("mm^2")), "mm^2")

    def test_generalparsing(self):
        self.assertEqual(repr(Unit("kgm^2 AJ^-10")), "J^{-10} m^2 kg A")

    def test_maxparsing(self):
        self.assertEqual( 
            repr(Unit("ng^-5us^-4mA^-3cK^-2C^-1kJ^1MV^2N^3GW^4T^5Pa^6Hzm^101")),
            "kJ MV^2 N^3 GW^4 T^5 Pa^6 Hz C^{-1} m^101 ng^{-5} us^{-4} mA^{-3} cK^{-2}"
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

    def test_slash_parsing(self):
        self.assertEqual(repr(Unit("m /s")), "m s^{-1}")
        self.assertEqual(repr(Unit("V/m")), "V m^{-1}")
        self.assertEqual(repr(Unit("kg / s^2m")), "m^{-1} kg s^{-2}")
        self.assertEqual(repr(Unit("ngs^2 / C^3 mm^-1")), "C^{-3} mm ng s^2")
