
from .measurement import Measurement, MeasurementList

import matplotlib.pyplot as plt 

plt.style.use('seaborn-whitegrid')


class LinearRegression:
    "Linearly regress two MeasurementLists."
    def __init__(self,x : MeasurementList, y : MeasurementList):
        self.x = x
        self.y = y

        assert len(x) == len(y)

        # TODO Support weighted regression
        n = len(x)
        w = [ 1 / n] * n

        xmean = sum(w*x) / sum(w)
        ymean = sum(w*y) / sum(w)

        D = sum(w*(x - xmean) ** 2)

        m = 1 / D * sum(w * (x - xmean) * y)

        c = ymean - m * xmean

        d = y - x*m - c.value
        Delta_m = (1/D * sum(w * d ** 2) / (n - 2) ) ** 0.5
        Delta_c = ( (1 / sum(w) + xmean ** 2 / D) * sum( w * d ** 2 ) / (n - 2) ) ** 0.5       

        # Line of best fit parameters
        self.lobf =  {
            "m": Measurement(m.value,Delta_m.value,m.unit),
            "c": Measurement(c.value,Delta_c.value,c.unit)
        }

    def __repr__(self):
        return f"{self.lobf['m']}{' + ' if self.lobf['c'].value > 0 else ' '}{self.lobf['c']}"

    def savefig(self,filename : str = "figure", title: str = "", xlabel : str = "", ylabel: str = ""):
        plt.errorbar(self.x.tolist(),self.y.tolist(),yerr = self.y.uncertainty,fmt='o')
        plt.plot(self.x.tolist(),(self.x*self.lobf["m"].value+self.lobf["c"].value).tolist())
        plt.title(title)
        plt.xlabel(xlabel + f", ({self.x.unit})")
        plt.ylabel(ylabel + f", ({self.y.unit})")
        plt.savefig(filename)
