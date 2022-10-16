from typing import Any
from labtex.unit import Unit
from labtex.measurementlist import MeasurementList

import matplotlib.pyplot as plt 
from matplotlib.axes import Axes
from numpy import linspace
from scipy.optimize import curve_fit

plt.style.use('seaborn-muted')
# seaborn-whitegrid
# seaborn-muted
# seaborn-dark-palette
# seaborn-darkgrid
# seaborn-talk / seaborn-paper / seaborn-poster / seaborn-notebook
# ggplot
# bmh

# To get the color cycle one can do:
# >>> plt.style.use('seaborn-muted')
# >>> prop_cycle = plt.rcParams['axes.prop_cycle']
# >>> colors = prop_cycle.by_key()['color']
# >>> colors
# ['#4878CF', '#6ACC65', '#D65F5F', '#B47CC7', '#C4AD66', '#77BEDB']
# >>> 

plt.rcParams.update({
    "text.usetex" : True,
    "font.family" : "serif",
    "font.size" : 12,
    "figure.autolayout" : True,
    "legend.framealpha": 1.0,
    # resolution
    "figure.dpi" : 300,
    # error bars
    "errorbar.capsize": 3,
})

class NonlinearRegression:
    "Curve fit two MeasurementLists to a function."
    def __init__(self,func : Any,x : MeasurementList, y : MeasurementList, init_params : list = None):
        self.func = func
        self.x = x
        self.y = y
        sigma = self.y.uncertainties() if all([i != 0 for i in self.y.uncertainties()]) else None

        popt, pcov = curve_fit(func, self.x.values(), self.y.values(), sigma=sigma, p0=init_params or None, absolute_sigma=True)
        self.optimal_params = popt
        self.param_uncertainties = [pcov[i][i]**0.5 for i in range(len(popt))]
        # return [ (popt[i], pcov[i][i]**0.5) for i in range(len(popt)) ]


    def __repr__(self):
        return f"Optimal parameters: {self.optimal_params}\nUncertainties: {self.param_uncertainties}"

    def predict(self, x):
        y = self.func(x, *self.optimal_params)
        if isinstance(y, MeasurementList):
            y.unit = self.y.unit
        return y

    def plot(self, ax : Axes = None, title: str = "", xlabel : str = "", ylabel: str = "", showline : bool = True, showfill : bool = True, *args, **kwargs):
        xvals = self.x.values()
        yvals = self.y.values()
        fig = plt.gcf()
        if (ax is None):
            ax = plt.gca()
            # this should be the same as fig.add_subplot(111) if fig is not None
            # else it should create a new figure and add a subplot to it
            # this is what we want
        else:
            plt.sca(ax)


        _e = ax.errorbar(xvals, yvals, yerr = self.y.uncertainties(), fmt='o',*args, **kwargs)
        ax.autoscale(enable=True, axis='x', tight=True)
        # extend +- 10% of the range
        rangex = max(xvals) - min(xvals)
        xspace = linspace(min(xvals) - 0.1 * rangex, max(xvals) + 0.1 * rangex, 1000)
        predicted =  [self.func(x, *self.optimal_params) for x in xspace]
        if showline:
            ax.plot(xspace,predicted, label="Predicted")
        if showfill:
            # minimize over all 2**n combinations of the optimal parameters instead
            minyspace = [
                min([ 
                        self.func(x, 
                             *[self.optimal_params[i] + (-1)**(j >> i) * self.param_uncertainties[i] for i in range(len(self.optimal_params))]
                        ) for j in range(2**len(self.optimal_params))
                    ] + [self.func(x, *self.optimal_params)]) for x in xspace
                ]
            maxyspace = [
                max([
                        self.func(x,
                            *[self.optimal_params[i] + (-1)**(j >> i) * self.param_uncertainties[i] for i in range(len(self.optimal_params))]
                        ) for j in range(2**len(self.optimal_params))
                    ] + [self.func(x, *self.optimal_params)]) for x in xspace
                ]
            ax.fill_between(xspace, minyspace, maxyspace, alpha=0.2, label='Uncertainty')
        
        title and plt.title(title)
        xlabel and plt.xlabel(xlabel + f"{' (' + Unit.latex(self.x.unit) + ')' if self.x.unit != '' else ''}")
        ylabel and plt.ylabel(ylabel + f"{' (' + Unit.latex(self.y.unit) + ')' if self.y.unit != '' else ''}")
        return fig, ax
