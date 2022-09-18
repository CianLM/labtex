import math
from labtex import *
import unittest
import numpy as np
import matplotlib.pyplot as plt

# Two MeasurementLists to be used in the rest of the tests
voltages = MeasurementList([1.3,3,5,7,8.5,10],1,"V")
temperatures = MeasurementList([23,55,67,82,88,96],[5,3,7,10,5,6],"K")
testset = MeasurementList([1.3,3,5,7,8.5,10],[1,1,2,1,1,1],"")
# Linear Regression
eq = LinearRegression(voltages,temperatures)

def func(x,A,B):
    return A*x**0.5 + B

sqeq = NonLinearRegression(func,voltages,temperatures)
plot = sqeq.plot()
plot.show()


class TestLinearRegression(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(
            LinearRegression.__repr__(eq), "m = 7 ± 1 V^{-1} K\nc = 27 ± 7 K"
        )

import pandas as pd
def func2(x,a,b,c,d):
    return b*(np.cos(c*x) * np.exp(-x/a)) + d
df = pd.read_excel('test/rabi_data.xlsx',sheet_name = 'data')
df["y"] = df["y"] - min(df["y"])

t = MeasurementList(df["x"],1,"ns")
probability = MeasurementList(df["y"], 0.05, "")

op = NonLinearRegression(func2,t,probability, init_params=(1e2,0.5,1e-2,0.4) )
plt = op.plot(label="Data")
plt.legend()
# plt.show()
plt.savefig("figures/rabi.png")

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
    # nonlinear_params = [1,1]
)

doc.graph(
    data = [voltages,temperatures**2],
    title = "Voltage and Temperature Squared Plot",
    xnameandsymbol = "Voltage, V",
    ynameandsymbol = "Temperature$^2$, $T^2$",
    caption = "Linear Regression of Voltage and Temperature"
)

doc.save("test",overwrite=True)