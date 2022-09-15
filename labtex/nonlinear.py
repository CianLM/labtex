from typing import Any
from labtex.measurement import Measurement
from labtex.measurementlist import MeasurementList

import matplotlib.pyplot as plt 
from numpy import array, linspace
from scipy.optimize import curve_fit

plt.style.use('seaborn-whitegrid')
plt.rcParams.update({
    "text.usetex" : True,
    "font.family" : "serif",
    "font.size" : 12,
    "figure.autolayout" : True,
    "legend.framealpha": 1.0,
    # resolution
    # "figure.dpi" : 200,
})

class NonLinearRegression:
    "Curve fit two MeasurementLists to a function."
    def __init__(self,func : Any,x : MeasurementList, y : MeasurementList, init_params : list = None):
        self.func = func
        self.x = x
        self.y = y

        popt, pcov = curve_fit(func, self.x.values(), self.y.values(), sigma=self.y.uncertainties(), p0=init_params, absolute_sigma=True)
        self.optimal_params = popt
        self.param_uncertainties = [pcov[i][i]**0.5 for i in range(len(popt))]
        # return [ (popt[i], pcov[i][i]**0.5) for i in range(len(popt)) ]


    def __repr__(self):
        return f"Optimal parameters: {self.optimal_params}\nUncertainties: {self.param_uncertainties}"

    def plot(self, title: str = "", xnameandsymbol : str = "", ynameandsymbol: str = "", showline : bool = True, graphnumber : int = 0):
        xvals = self.x.values()
        yvals = self.y.values()
        plt.figure(graphnumber)
        plt.errorbar(xvals, yvals, yerr = self.y.uncertainties(),fmt='o')
        if showline:
            xspace = linspace(min(xvals), max(xvals), 100)
            plt.plot(xspace, [
                self.func(x, *self.optimal_params) for x in xspace
                ])
            plt.plot(xspace, [
            self.func(x, *(self.optimal_params - self.param_uncertainties)) for x in xspace
            ], '--')
            plt.plot(xspace, [
            self.func(x, *(self.optimal_params + self.param_uncertainties)) for x in xspace
            ], '--')
        
        plt.title(title)
        plt.xlabel(xnameandsymbol + f"{', ($ ' + str(self.x.unit) + '$)' if self.x.unit != '' else ''}")
        plt.ylabel(ynameandsymbol + f"{', ($ ' + str(self.y.unit) + '$)' if self.y.unit != '' else ''}")
        return plt
