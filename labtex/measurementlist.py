import math
from numbers import Number
from typing import List, Union
from numpy import array

from labtex.unit import Unit
from labtex.measurement import Measurement

class MeasurementList:
    """An extension of the measurement class to take list values. Can be instantiated in a number of ways:
    - Using lists for the values and the uncertainty
    
    `>>> MeasurementList([1,2,3],[0.1,0.2,0.3],"m")`

    - Using lists for the values and a single uncertainty for all measurements

    `>>> MeasurementList([1,2,3],0.1,"m")`

    - Using A list of `Measurement` instances

    `>>> MeasurementList( 
     ... [Measurement(1,0.1,"m"),Measurement(2,0.2,"m"),Measurement(3,0.3,"m")]
     ... )`

    """
    def __init__(self,measurements: Union[List[Number],List[Measurement]], uncertainty: Union[Number,List] = math.nan, unit: Union[Unit,str] = ""):
        
        if (all(isinstance(value,Measurement) for value in measurements)):
            if (all( value.unit == measurements[0].unit for value in measurements)):
                self.measurements = array(measurements)
                self.unit = measurements[0].unit
            else:
                raise Exception("MeasurementList Error: All measurements in a MeasurementList must have the same units.")
        
        elif (all(isinstance(value,Number) for value in measurements)):
            uncertainty = uncertainty if isinstance(uncertainty,List) else [uncertainty] * len(measurements)
            self.unit = unit if (isinstance(unit,Unit)) else Unit(unit)
            self.measurements = array([Measurement(value,uncertainty[i],self.unit) for i,value in enumerate(measurements)])

    def __repr__(self):
        "Print string with sigfigs up to uncertainty."            
        return f"[{', '.join([str(measurement)[:-(len(str(self.unit)) + 1)] for measurement in self])}] {self.unit}"

    def tableprint(self, novalues = False, nounits = False):
        "return string in printable LaTeX table format. Used in `Document().table()`."
        constantuncertainty = all(measurement.uncertainty == self.measurements[0].uncertainty for measurement in self)
        tableprint = ""
        if (constantuncertainty):
            sigdigits = -math.floor(math.log10(self.measurements[0].uncertainty))
            sigdigits = -math.floor(math.log10(round(self.measurements[0].uncertainty,sigdigits)))
            if(sigdigits > 0):
                if(not nounits):
                    tableprint += f", ($\\pm {round(self.measurements[0].uncertainty,sigdigits)}$ {self.unit})"
                if(not novalues):
                    tableprint += f"& { r' & '.join([str(round(measurement.value,sigdigits)) for measurement in self ] ) }"
            else: # remove decimal points from the float data type
                if(not nounits):
                    tableprint += f", ($\\pm {round(int(self.measurements[0].uncertainty),sigdigits)}$ {self.unit}) "
                if(not novalues):
                    tableprint += f"& { r' & '.join([ str(round(round(measurement.value),sigdigits)) for measurement in self ] ) }"
        else:
            if(not novalues):
                tableprint += f"& ${ r'$ & $'.join([str(measurement)[:-len(str(measurement.unit))] for measurement in self ] ) }$"

        return tableprint.replace('±','\pm').replace('×','\\times')

    def __len__(self):
        return len(self.measurements)

    def __getitem__(self,item):
        return self.measurements[item]

    def __iter__(self):
        yield from self.measurements

    def values(self):
        return [measurement.value for measurement in self]
    
    def uncertainties(self):
        return [measurement.uncertainty for measurement in self]
    
    def append(self,obj):
        if(isinstance(obj,MeasurementList)):
            return MeasurementList([*[measurement for measurement in self], *[measurement for measurement in obj]])
        elif(isinstance(obj,Measurement)):
            return MeasurementList([*[measurement for measurement in self], obj])
        else:
            raise Exception(f"Object of type {type(obj)} cannot be appended to a MeasurementList. Try a MeasurementList or a Measurement.")

            
    def __add__(self,obj):
        "Elementwise addition of two MeasurementLists. If a Measurement is added, it is added to all Measurements in the list."
        if(isinstance(obj,MeasurementList)):
            if(len(self) == len(obj)):
                return MeasurementList(
                    [measurement + obj[i] for i,measurement in enumerate(self)]
                )
            else:
                raise Exception(f"MeasurementList Error: Cannot add two MeasurementLists with different lengths: {len(self)} =/= {len(obj)}. If you want to append them use .append().")
        else:
            return MeasurementList(
                [measurement + obj for measurement in self]
            )

    def __radd__(self,obj):
        return self.__add__(obj)

    def __neg__(self):
        return MeasurementList(
            [-measurement for measurement in self]
        )

    def __sub__(self,obj):
        return self.__add__(-obj)
        
    def __rsub__(self,obj):    
        return self.__neg__().__add__(obj)

    def __mul__(self,obj):
        "Elementwise (aka inner) multiplication of two MeasurementLists. If a Measurement is used, it is multiplied by all Measurements in the list."
        if(isinstance(obj,MeasurementList)):
            if(len(self) == len(obj)):
                return MeasurementList(
                    [measurement * obj[i] for i,measurement in enumerate(self)]
                )
            else:
                raise Exception(f"MeasurementList Error: Cannot multiply two MeasurementLists with different lengths: {len(self)} =/= {len(obj)}. If you want to append them use .append().")
        else:
            return MeasurementList(
                [measurement * obj for measurement in self]
            )

    def __rmul__(self,obj):
        return self.__mul__(obj)
        
    def __truediv__(self,obj):
        "Elementwise division of two MeasurementLists. If a Measurement is used all Measurements in the list are divided by it."
        if(isinstance(obj,MeasurementList)):
            if(len(self) == len(obj)):
                return MeasurementList(
                    [measurement / obj[i] for i,measurement in enumerate(self)]
                )
            else:
                raise Exception(f"MeasurementList Error: Cannot divide two MeasurementLists with different lengths: {len(self)} =/= {len(obj)}. If you want to append them use .append().")
        else:
            return MeasurementList(
                [measurement / obj for measurement in self]
            )

    def __rtruediv__(self,obj):
        "Accomodates the division of a number or Measurement by a MeasurementList."
        return MeasurementList(
            [obj / measurement for measurement in self]
        )

    def __pow__(self,obj):
        return MeasurementList(
            [measurement ** obj for measurement in self]
        )

    def __rpow__(self,obj):
        return MeasurementList(
            [obj ** measurement for measurement in self]
        )

    @staticmethod
    def sin(x):
        return MeasurementList(
            [Measurement.sin(measurement) for measurement in x]
        )

    @staticmethod
    def cos(x):
        return MeasurementList(
            [Measurement.cos(measurement) for measurement in x]
        )

    @staticmethod
    def tan(x):
        return MeasurementList(
            [Measurement.tan(measurement) for measurement in x]
        )

    @staticmethod
    def log(x):
        return MeasurementList(
            [Measurement.log(measurement) for measurement in x]
        )

    @staticmethod
    def asin(x):
        return MeasurementList(
            [Measurement.asin(measurement) for measurement in x]
        )
    
    @staticmethod
    def acos(x):
        return MeasurementList(
            [Measurement.acos(measurement) for measurement in x]
        )

    @staticmethod
    def atan(x):
        return MeasurementList(
            [Measurement.atan(measurement) for measurement in x]
        )

class ML(MeasurementList):
    pass