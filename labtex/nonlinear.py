from typing import Any
from labtex.measurement import Measurement
from labtex.measurementlist import MeasurementList

import matplotlib.pyplot as plt 
from numpy import array, linspace
from scipy.optimize import curve_fit

plt.style.use('seaborn-muted')
# seaborn-whitegrid
# seaborn-muted
# seaborn-dark-palette
# seaborn-darkgrid
# seaborn-talk / seaborn-paper / seaborn-poster / seaborn-notebook
# ggplot
# bmh
plt.rcParams.update({
    "text.usetex" : True,
    "font.family" : "serif",
    "font.size" : 12,
    "figure.autolayout" : True,
    "legend.framealpha": 1.0,
    # resolution
    "figure.dpi" : 300,
})

class NonLinearRegression:
    "Curve fit two MeasurementLists to a function."
    def __init__(self,func : Any,x : MeasurementList, y : MeasurementList, init_params : list = None):
        self.func = func
        self.x = x
        self.y = y

        popt, pcov = curve_fit(func, self.x.values(), self.y.values(), sigma=self.y.uncertainties(), p0=init_params or None, absolute_sigma=True)
        self.optimal_params = popt
        self.param_uncertainties = [pcov[i][i]**0.5 for i in range(len(popt))]
        # return [ (popt[i], pcov[i][i]**0.5) for i in range(len(popt)) ]


    def __repr__(self):
        return f"Optimal parameters: {self.optimal_params}\nUncertainties: {self.param_uncertainties}"

    def plot(self, title: str = "", xnameandsymbol : str = "", ynameandsymbol: str = "", showline : bool = True, graphnumber : int = 0, *args, **kwargs):
        xvals = self.x.values()
        yvals = self.y.values()
        plt.figure(graphnumber)
        plt.errorbar(xvals, yvals, yerr = self.y.uncertainties(),fmt='o',*args, **kwargs)
        plt.autoscale(enable=True, axis='x', tight=True)
        if showline:
            # extend +- 10% of the range
            rangex = max(xvals) - min(xvals)
            xspace = linspace(min(xvals) - 0.1 * rangex, max(xvals) + 0.1 * rangex, 100)
            plt.plot(xspace, [
                self.func(x, *self.optimal_params) for x in xspace
                ], label="Predicted")
            # minyspace = [self.func(x, *(self.optimal_params - self.param_uncertainties)) for x in xspace]
            # maxyspace = [self.func(x, *(self.optimal_params + self.param_uncertainties)) for x in xspace]
            # minimize over all 2**n combinations of the optimal parameters instead
            minyspace = [
                min([ 
                        self.func(x, 
                             *[self.optimal_params[i] + (-1)**(j >> i) * self.param_uncertainties[i] for i in range(len(self.optimal_params))]
                        ) for j in range(2**len(self.optimal_params))
                    ])
                 for x in xspace
                ]
            maxyspace = [
                max([
                        self.func(x,
                            *[self.optimal_params[i] + (-1)**(j >> i) * self.param_uncertainties[i] for i in range(len(self.optimal_params))]
                        ) for j in range(2**len(self.optimal_params))
                    ])
                    for x in xspace
                ]
            plt.fill_between(xspace, minyspace, maxyspace, alpha=0.2, label='Uncertainty')
        
        plt.title(title)
        plt.xlabel(xnameandsymbol + f"{', ($ ' + str(self.x.unit) + '$)' if self.x.unit != '' else ''}")
        plt.ylabel(ynameandsymbol + f"{', ($ ' + str(self.y.unit) + '$)' if self.y.unit != '' else ''}")
        return plt
