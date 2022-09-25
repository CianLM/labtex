import math
from re import template
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
# plot = sqeq.plot()
# # plot.show()


class TestLinearRegression(unittest.TestCase):
    def test_repr(self):
        self.assertEqual(
            LinearRegression.__repr__(eq), "m = 7 ± 1 V^{-1} K\nc = 27 ± 7 K"
        )

# import pandas as pd
# def func2(x,a,b,c,d):
#     return b*(np.cos(c*x) * np.exp(-x/a)) + d
# df = pd.read_excel('test/rabi_data.xlsx',sheet_name = 'data')
# df["y"] = df["y"] - min(df["y"])

# t = MeasurementList(df["x"],1,"ns")
# probability = MeasurementList(df["y"], 0.05, "")

# op = NonLinearRegression(func2,t,probability, init_params=(1e2,0.5,1e-2,0.4) )
# plt = op.plot(label="Data",graphnumber=4)
# plt.legend()
# plt.savefig("figures/rabi.png")
# plt.show()

class TestNonLinearRegression(unittest.TestCase):
    def test_nlr_repr(self):
        self.assertEqual(
            sqeq.__repr__(), "Optimal parameters: [33.2759282  -6.89522347]\nUncertainties: [2.976448764153751, 6.462296108511657]"
        )

# Template file creation is hard to test as it involves file creation, so this portion is tested manually.
# Latex template creation

doc = Document(
    title = "Lab Report Template", author = "CianLM",
    filename='test2.tex', silent=False
)

doc.add_table(
    nameandsymbols = ["Voltage, V","Temperature, T"],
    data = [voltages,temperatures],
    headers = ["Variables","Data"],
    caption = "Voltage and Temperature Correlation",
)

doc.add_table(
    nameandsymbols = ["Voltage, V", "Temperatures", "Testset"],
    data = [voltages,testset,testset],
    caption = "Voltage and Temperature Squared Correlation",
    style = "upright"
)

doc.add_table(
    nameandsymbols = ["Voltage, V", "Testset (dimless)", "Testset"],
    data = [voltages,temperatures,testset],
    caption = "Voltage and Temperature Squared Correlation",
    style = "upright",
    label = "custom_label"
)



# This approach is pythonic as it allows for the user to modify the plot
# before it is added to the document (e.g. adding a legend, changing the title, etc.) and it allows for the user
# to add multiple plots to the document without having to save them to disk. Note that the ax object is not returned
# as the user can access it via fig.axes[0] (or fig.gca() for the current axes) but it shouldn't be needed as the
# linear regression plot is a single axis plot. 

linreg = LinearRegression(voltages,temperatures)
fig = linreg.plot(xlabel="Voltage, V", ylabel="Temperature, T", title="Voltage and Temperature Plot")
doc.add_figure(fig, caption="Linear Regression of Voltage and Temperature", label="vtr")

sqrtreg = NonLinearRegression(func,voltages,temperatures)
fig2 = sqrtreg.plot(xlabel="Voltage, V", ylabel="Square Root of Temperature, T$^{\\frac{1}{2}}$", title="Non-Linear ($\sqrt{x}$) Curve Fit Voltage and Temperature Plot")
doc.add_figure(fig2, caption="Non-linear ($\sqrt{x}$) Regression of Voltage and Temperature")

squarereg = LinearRegression(voltages,temperatures**2)
fig3 = squarereg.plot(xlabel="Voltage, V", ylabel="Temperature Squared, $T^2$", title="Voltage and Temperature Squared Plot")
doc.add_figure(fig3, caption="Linear Regression of Voltage and Temperature Squared")

dt = 0.01
t = ML(np.arange(0, 30, dt),dt/2,"s")
nse1 = ML(np.random.randn(len(t)),0,'')                 # white noise 1
nse2 = ML(np.random.randn(len(t)) ,0,'')                # white noise 2

# # Two signals with a coherent part at 10Hz and a random part
omega_t = M(2 * np.pi * 10,0,"Hz") * t
omega_t = omega_t.to('')

s1 = ML.sin(omega_t) + nse1
s2 = ML.sin(omega_t) + nse2

fig, axs = plt.subplots(2, 1)
axs[0].plot(t.values(), s1.values(), t.values(), s2.values())
axs[0].set_xlim(0, 2)
axs[0].set_xlabel('time')
axs[0].set_ylabel('s1 and s2')
axs[0].grid(True)

cxy, f = axs[1].cohere(s1.values(), s2.values(), 256, 1. / dt)
axs[1].set_ylabel('coherence')

fig.tight_layout()

doc.add_figure(fig, caption="Two signals with a coherent part at 10Hz and a random part")






doc.save(overwrite=True)