from typing import Iterable, Union
from labtex.unit import Unit
from labtex.measurement import Measurement
from labtex.measurementlist import MeasurementList

import matplotlib.pyplot as plt 
from matplotlib.axes import Axes
from numpy import array, linspace

# plt.style.use('seaborn-whitegrid')
plt.rcParams.update({
    "text.usetex" : True,
    "font.family" : "serif",
    "font.size" : 12,
    "figure.autolayout" : True,
    "legend.framealpha": 1.0,
    # resolution
    "figure.dpi" : 300,
})

class LinearRegression:
    "Linearly regress two MeasurementLists."
    def __init__(self,x : MeasurementList, y : MeasurementList):
        self.x = x
        self.y = y
        x = array(self.x.values())
        y = array(self.y.values())

        assert len(x) == len(y)

        n = len(x)
        w = 1/array([measurement.uncertainty for measurement in self.y])**2

        xmean = sum(w * x) / sum(w)
        ymean = sum(w * y) / sum(w)

        D = sum(w * (x - xmean) ** 2)

        m = 1 / D * sum(w * (x - xmean) * y)

        c = ymean - m * xmean

        d = y - x*m - c
        # Statistical uncertainties
        Delta_m = (1/D * sum(w * d ** 2) / (n - 2) ) ** 0.5
        Delta_c = ( (1 / sum(w) + xmean ** 2 / D) * sum( w * d ** 2 ) / (n - 2) ) ** 0.5       

        # Line of best fit parameters
        self.lobf =  {
            "m": Measurement(m, Delta_m, self.y.unit / self.x.unit),
            "c": Measurement(c, Delta_c, self.y.unit)
        }

    def __repr__(self):
        return f"m = {self.lobf['m']}\nc = {self.lobf['c']}"

    def predict(self, x : Union[Measurement,Iterable]):
        return self.lobf["m"] * x + self.lobf["c"] if isinstance(x, Measurement) or isinstance(x, MeasurementList) else self.lobf["m"].value * x + self.lobf["c"].value

    def plot(self, ax : Axes = None, xlabel : str = "", ylabel: str = "", title: str = "", showline : bool = True, showfill : bool = True, *args, **kwargs):
        fig = plt.gcf()
        if (ax is None):
            ax = plt.gca()
        else:
            plt.sca(ax)

        
        ax.errorbar(self.x.values(),self.y.values(), yerr = self.y.uncertainties(),fmt='o', *args, **kwargs)
        ax.autoscale(enable=True, axis='x', tight=True)

        xvals = self.x.values()
        rangex = max(xvals) - min(xvals)
        xspace = linspace(min(xvals) - 0.1 * rangex, max(xvals) + 0.1 * rangex, 1000)
        if showline:
            ax.plot(xspace, xspace * self.lobf["m"].value + self.lobf["c"].value, label = "Predicted")
        if showfill:
            ax.fill_between(xspace,
             xspace * (self.lobf["m"].value + self.lobf["m"].uncertainty * (1 - 2 *(xspace < 0)) ) + self.lobf["c"].value + self.lobf["c"].uncertainty,
             xspace * (self.lobf["m"].value - self.lobf["m"].uncertainty * (1 - 2 * (xspace < 0)) ) + self.lobf["c"].value - self.lobf["c"].uncertainty,
             alpha=0.2
            )
        title and plt.title(title)
        xlabel and plt.xlabel(xlabel + f"{' (' + Unit.latex(self.x.unit) + ')' if self.x.unit != '' else ''}")
        ylabel and plt.ylabel(ylabel + f"{' (' + Unit.latex(self.y.unit) + ')' if self.y.unit != '' else ''}")
        return fig, ax
