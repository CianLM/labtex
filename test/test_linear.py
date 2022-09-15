from labtex import *
import unittest

# Two MeasurementLists to be used in the rest of the tests
voltages = MeasurementList([1.3,3,5,7,8.5,10],1,"V")
temperatures = MeasurementList([23,55,67,82,88,96],[5,3,7,10,5,6],"K")
testset = MeasurementList([1.3,3,5,7,8.5,10],[1,1,2,1,1,1],"")
# Linear Regression
eq = LinearRegression(voltages,temperatures)

def func(x,A,B):
    return A*x**0.5 + B

sqeq = NonLinearRegression(func,voltages,temperatures)
plt = sqeq.plot()
# plt.show()


class TestLinearRegression(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(
            LinearRegression.__repr__(eq), "m = 7 ± 1 V^{-1} K\nc = 27 ± 7 K"
        )

class TestNonLinearRegression(unittest.TestCase):
    def test_nlr_repr(self):
        self.assertEqual(
            sqeq.__repr__(), "Optimal parameters: [33.2759282  -6.89522347]\nUncertainties: [2.976448764153751, 6.462296108511657]"
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
    data = [voltages,temperatures],
    title = "Non-Linear Curve Fit Voltage and Temperature Plot",
    xnameandsymbol = "Voltage, V",
    ynameandsymbol = "Temperature, T",
    caption = "Non-Linear Regression of Voltage and Temperature",
    nonlinear_func = func,
    nonlinear_params = [1,1]
)

doc.graph(
    data = [voltages,temperatures**2],
    title = "Voltage and Temperature Squared Plot",
    xnameandsymbol = "Voltage, V",
    ynameandsymbol = "Temperature$^2$, $T^2$",
    caption = "Linear Regression of Voltage and Temperature"
)

doc.save("test",overwrite=True)