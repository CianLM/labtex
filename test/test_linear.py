from labtex import *
import unittest

# Two MeasurementLists to be used in the rest of the tests
voltages = MeasurementList([1.3,3,5,7,8.5,10],1,"V")
temperatures = MeasurementList([23,55,67,82,88,96],[5,3,7,10,5,6],"K")
testset = MeasurementList([1.3,3,5,7,8.5,10],[1,1,2,1,1,1],"")
# Linear Regression
eq = LinearRegression(voltages,temperatures)

class TestLinearRegression(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(
            LinearRegression.__repr__(eq), "m = 7 ± 1 V^{-1} K\nc = 27 ± 7 K"
        )

# Template file creation is hard to test as it involves file creation, so this portion is tested manually.
# Latex template creation
doc = Document(title = "Lab Report Template", author = "CianLM")

doc.table(
    nameandsymbol = ["Voltage, V","Temperature, T", 'testset'],
    data = [voltages,temperatures,testset],
    # headers = ["Variables","Data"],
    caption = "Voltage and Temperature Correlation"
)

doc.table(
    nameandsymbol = ["Voltage, V", "Temperature, T", "Testset"],
    data = [voltages,temperatures,testset],
    caption = "Voltage and Temperature Squared Correlation",
    style = "upright"
)

doc.graph(
    data = [voltages,temperatures],
    title = "Voltage and Temperature Plot",
    xnameandsymbol = "Voltage, V",
    ynameandsymbol = "Temperature, T",
    caption = "Linear Regression of Voltage and Temperature"
)

doc.graph(
    data = [voltages,temperatures**2],
    title = "Voltage and Temperature Squared Plot",
    xnameandsymbol = "Voltage, V",
    ynameandsymbol = "Temperature$^2$, $T^2$",
    caption = "Linear Regression of Voltage and Temperature"
)

doc.save("test",overwrite=True)