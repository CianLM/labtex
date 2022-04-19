from labtex.measurement import Measurement
from labtex.measurementlist import MeasurementList

import matplotlib.pyplot as plt 
from numpy import array

plt.style.use('seaborn-whitegrid')


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

    def plot(self, title: str = "", xname : str = "", yname: str = "", showline : bool = True, graphnumber : int = 0):
        plt.figure(graphnumber)
        plt.errorbar(self.x.values(),self.y.values(), yerr = self.y.uncertainties(),fmt='o')
        if showline:
            plt.plot(self.x.values(), (self.x * self.lobf["m"].value + self.lobf["c"].value).values() )
        plt.title(title)
        plt.xlabel(xname + f"{', ($' + str(self.x.unit) + '$)' if self.x.unit != '' else ''}")
        plt.xlabel(yname + f"{', ($' + str(self.y.unit) + '$)' if self.y.unit != '' else ''}")
        return plt
