import math
from typing import List, Union

from labtex.unit import Unit

class Measurement:
    def __init__(self, value: float, uncertainty: float = 0, unit: Union[Unit,str] = ""):
        "Create a measurement with a value, uncertainty and SI Unit."
        self.value = value
        self.uncertainty = uncertainty
        self.relativeuncertainty = self.uncertainty / self.value

        self.unit = unit if (isinstance(unit,Unit)) else Unit(unit)
    
    def __repr__(self):
        "Print string with sigfigs up to uncertainty."
        sigdigits = -math.floor(math.log10(self.uncertainty))
        # To account for rounding up of uncertainty before applying it,
        # eg. 98 => sigdigits = -1 but round(98,-1) => 100 so we apply again to get -2.
        sigdigits = -math.floor(math.log10(round(self.uncertainty,sigdigits)))
        
        if(sigdigits >= 3):
            return f"({round(round(self.value * 10**sigdigits),sigdigits)} ± {round(math.ceil(self.uncertainty * 10**sigdigits),sigdigits)}) × 10^{{{-sigdigits}}} {self.unit}"
        elif(sigdigits > 0):
            return f"{round(self.value,sigdigits) } ± {round(self.uncertainty,sigdigits)} {self.unit}"
        elif(sigdigits > -3): # remove decimal points from the float data type
            return f"{round(round(self.value),sigdigits)} ± {round(int(self.uncertainty),sigdigits)} {self.unit}"
        else:
            return f"({round(round(self.value,sigdigits) * 10**sigdigits)} ± {round(round(self.uncertainty,sigdigits) * 10**sigdigits)}) × 10^{{{-sigdigits}}} {self.unit}"
    
    def __add__(self,obj):
        "Add two measurements."

        # Addition necessitates independent variables
        if(self == obj):
            return Measurement(
            self.value * 2,
            self.uncertainty * 2,
            self.unit * 2
        )

        if(isinstance(obj,Measurement)):
            if(self.unit == obj.unit):
                return Measurement(
                    self.value + obj.value,
                    math.hypot(self.uncertainty,obj.uncertainty),
                    self.unit
            )
            else:
                raise Exception("Cannot add measurements with different units.")

        elif(isinstance(obj,MeasurementList)):
            if(self.unit == obj.unit):
                return MeasurementList(
                    [self.value + value for value in obj.values]
                )
            else:
                raise Exception("Cannot add measurement and MeasurementList with different units.")

        else:
            return Measurement(
                self.value + obj,
                self.uncertainty,
                self.unit
            )
    
    def __radd__(self,obj):
        "Reverse addition to accomodate constant + measurement."
        return Measurement(
            obj + self.value,
            self.uncertainty,
            self.unit
        )
        
    def __sub__(self,obj):
        "Subtract two measurements."
        
        # This only occurs if you do: x - x
        if(self == obj):
            return Measurement(
            0,
            0,
            self.unit * 2
        )

        if(isinstance(obj,Measurement)):
            if(self.unit == obj.unit):
                return Measurement(
                    self.value - obj.value,
                    math.hypot(self.uncertainty,obj.uncertainty),
                    self.unit
            )
            else:
                raise Exception("Cannot subtract measurements with different units.")
        
        elif(isinstance(obj,MeasurementList)):
            if(self.unit == obj.unit):
                return MeasurementList(
                    [self.value - value for value in obj.values]
                )
            else:
                raise Exception("Cannot subtract measurement and MeasurementList with different units.")

        else:
            return Measurement(
                self.value - obj,
                self.uncertainty,
                self.unit
            )
        
    def __rsub__(self,obj):
        "Reverse subtraction to accomodate constant - measurement."
        return Measurement(
            obj - self.value,
            self.uncertainty,
            self.unit
        )

    def __mul__(self,obj):
        "Multiply two measurements."

        # Multiplication necessitates independent variables
        # This occurs if you do: x * x
        if(self == obj):
            return Measurement(
            self.value ** 2,
            (self.value ** 2) * 2 * self.relativeuncertainty,
            self.unit ** 2
        )

        if(isinstance(obj,Measurement)):
            return Measurement(
                self.value * obj.value,
                (self.value * obj.value) * math.hypot(self.relativeuncertainty,obj.relativeuncertainty),
                self.unit * obj.unit
            )

        elif(isinstance(obj,MeasurementList)):
            return MeasurementList(
                    [ self * value for value in obj.values]
                )

        else:
            # if no unit conversion is possible,
            if(self.unit * obj == self.unit):
                return Measurement(
                    self.value * obj,
                    self.uncertainty * obj,
                    self.unit * obj
                )
            else: # otherwise unit conversion has happened, so
                return Measurement(
                    self.value,
                    self.uncertainty,
                    self.unit * obj
                )

            
    def __rmul__(self,obj):
        "Reverse multiplication to accomodate constant * measurement."
        oldrepr = Unit.__repr__(self.unit)
        if(Unit.__repr__(self.unit * obj) == oldrepr):
            return Measurement(
                self.value * obj,
                self.uncertainty * obj,
                self.unit * obj
            )
        else: # unit conversion has happened, so
            return Measurement(
                self.value,
                self.uncertainty,
                self.unit * obj
            )
    
    def __truediv__(self,obj):
        "Divide two measurements."

        # While nonsensical, this only occurs if you do: x / x
        if(self == obj):
            return Measurement(
            1,
            0,
            ""
        )

        if(isinstance(obj,Measurement)):
            return Measurement(
                self.value / obj.value,
                (self.value / obj.value) * math.hypot(self.relativeuncertainty,obj.relativeuncertainty),
                self.unit / obj.unit
            )

        elif(isinstance(obj,MeasurementList)):
            return MeasurementList(
                [self / value for value in obj.values]
            )

        else:
            oldrepr = Unit.__repr__(self.unit)
            if(Unit.__repr__(self.unit / obj) == oldrepr):
                return Measurement(
                    self.value / obj,
                    self.uncertainty / obj,
                    self.unit / obj
                )
            else: # unit conversion has happened, so
                return Measurement(
                    self.value,
                    self.uncertainty,
                    self.unit / obj
                )

    def __rtruediv__(self,obj):
        "Reverse division to accomodate constant / measurement."
        return Measurement(
            obj / self.value,
            (obj / self.value) * self.relativeuncertainty,
            obj / self.unit
        )

    def __pow__(self,obj):
        "Raising a measurement to a power."
        return Measurement(
            self.value ** obj,
            (self.value ** obj) * obj * self.relativeuncertainty,
            self.unit ** obj
        )
    
    def __rpow__(self,obj):
        "Reverse power for constant ** measurement."
        return Measurement(
            obj ** self.value,
            (obj ** self.value) * self.uncertainty,
            ""
        )

    # Static Functions applied to Measurements
    # All parameters are instances of Measurement
    @staticmethod
    def sin(x):
        "Sine function on a Measurement."
        if(Unit.unitless(x.unit)):
            return Measurement(
            math.sin(x.value),
            math.fabs(math.cos(x.value)) * x.uncertainty,
            ""
            )
        else:
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.units}")

    @staticmethod
    def cos(x):
        "Cosine function on a Measurement."
        if(Unit.unitless(x.unit)):
            return Measurement(
                math.cos(x.value),
                math.fabs(math.sin(x.value)) * x.uncertainty,
                ""
            )
        else:
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.units}")

    @staticmethod
    def tan(x):
        "Tangent function on a Measurement."
        if(Unit.unitless(x.unit)):
            return Measurement(
                math.tan(x.value),
                math.fabs( 1 / math.cos(x.value)**2 ) * x.uncertainty,
                ""
            )
        else:
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.units}")
    
    @staticmethod
    def log(x):
        "Natural log function on a Measurment."
        if(Unit.unitless(x.unit)):
            return Measurement(
                math.log(x.value),
                x.relativeuncertainty,
                ""
            )
        else:
            raise Exception(f"Log functions take in dimensionless quantities. Input has units: {x.units}")
    
    @staticmethod
    def asin(x):
        "Inverse sine function on a Measurement."
        if(Unit.unitless(x.unit)):
            return Measurement(
                math.asin(x.value),
                x.uncertainty / (math.sqrt(1 - x.value**2)),
                ""
            )
        else:
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.units}")
    
    @staticmethod
    def acos(x):
        "Inverse cosine function on a Measurement."
        if(Unit.unitless(x.unit)):
             return Measurement(
                math.acos(x.value),
                x.uncertainty / (math.sqrt(1 - x.value**2)),
                ""
            )
        else:
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.units}")

    @staticmethod
    def atan(x):
        "Inverse tangent function on a Measurement."
        if(Unit.unitless(x.unit)):
            return Measurement(
                math.atan(x.value),
                x.uncertainty / (math.sqrt(1 - x.value**2)),
                ""
            )
        else:
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.units}")



class MeasurementList:
    "An extension of the measurement class to take list values."
    def __init__(self,values: Union[List[float],List[Measurement]], uncertainty: float = math.nan, unit: Union[Unit,str] = ""):
        
        if (all( isinstance(value,Measurement) and value.unit == values[0].unit for value in values )):
            self.uncertainty = max(value.uncertainty for value in values)
            self.unit = values[0].unit

            self.values = [Measurement(measurement.value,measurement.uncertainty,self.unit) for measurement in values]

        else:
            # Take sigma/sqrt(n) if uncertainty is not given
            if(uncertainty == math.nan):
                mean = sum(values) / len(values) 
                cas = [ (value - mean) ** 2 for value in values ]
                self.uncertainty = math.sqrt( 1 / len(values) * sum(cas) )
            else:
                self.uncertainty = uncertainty

            self.unit = unit if (isinstance(unit,Unit)) else Unit(unit)
            self.values = [ Measurement(value,self.uncertainty,self.unit) for value in values ]

    def __repr__(self):
        "Print string with sigfigs up to uncertainty."
        sigdigits = -math.floor(math.log10(self.uncertainty))
        # To account for rounding up of uncertainty before applying it
        sigdigits = -math.floor(math.log10(round(self.uncertainty,sigdigits)))

        if(sigdigits >= 3):
            return f"({[round(round(m.value * 10**sigdigits),sigdigits) for m in self.values]} ± {round(math.ceil(self.uncertainty * 10**sigdigits),sigdigits)}) × 10^{{{-sigdigits}}} {self.unit}"
        elif(sigdigits > 0):
            return f"{[ round(m.value,sigdigits) for m in self.values]} ± {round(self.uncertainty,sigdigits)} {self.unit}"
        elif(sigdigits > -3): # remove decimal points from the float data type
            return f"{[ round(round(m.value),sigdigits) for m in self.values ]} ± {round(int(self.uncertainty),sigdigits)} {self.unit}"
        else:
            return f"({[round(round(m.value,sigdigits) * 10**sigdigits) for m in self.values]} ± {round(round(self.uncertainty,sigdigits) * 10**sigdigits)}) × 10^{{{-sigdigits}}} {self.unit}"


    def tableprint(self,flags : str = "uv"): # u -> uncertainty, v -> values
        "return string in printable LaTeX table format. Used in 'Document().table()'."
        sigdigits = -math.floor(math.log10(self.uncertainty))
        sigdigits = -math.floor(math.log10(round(self.uncertainty,sigdigits)))

        tableprint = ""
        if(sigdigits > 0):
            if("u" in flags):
                tableprint += f"$\\pm$ {round(self.uncertainty,sigdigits)} {self.unit}"
            if("v" in flags):
                tableprint += f"& { r' & '.join([str(round(measurement.value,sigdigits)) for measurement in self.values ] ) }"
        else: # remove decimal points from the float data type
            if("u" in flags):
                tableprint += f"$\\pm$ {round(int(self.uncertainty),sigdigits)} {self.unit} "
            if("v" in flags):
                tableprint += f"& { r' & '.join([str(round(round(measurement.value),sigdigits)) for measurement in self.values ] ) }"

        return tableprint

    def __len__(self):
        return len(self.values)

    def __getitem__(self,item):
        return self.values[item]

    def __iter__(self):
        yield from self.values
    
    def tolist(self):
        return [measurement.value for measurement in self.values]

    def append(self,obj):
        if(isinstance(obj,MeasurementList)):
            return MeasurementList(*[value for value in self.values],*[value for value in obj])
        elif(isinstance(obj,Measurement)):
            return MeasurementList(*[value for value in self.values],obj)
        else:
            raise Exception(f"Object of type {type(obj)} cannot be appended to a MeasurementList. Try a MeasurementList or a Measurement.")

            
    def __add__(self,obj):
        if(isinstance(obj,MeasurementList)):
            if(self.unit == obj.unit):
                return MeasurementList(
                    [self.values[i] + obj[i] for i in range(len(self))]
                )
            else:
                raise Exception("Unit Error: Cannot add MeasurementLists with different units.")
        else:
            try:
                return MeasurementList(
                    [value + obj for value in self.values]
                )
            except:
                raise Exception(f"Type Error: Addition not supported between '{type(self)}' and '{type(obj)}'.")

    def __radd__(self,obj):
        return MeasurementList(
            [obj + value for value in self.values]
        )

    def __sub__(self,obj):
        if(isinstance(obj,MeasurementList)):
            if(self.unit == obj.unit):
                return MeasurementList(
                    [self.values[i] - obj[i] for i in range(len(self))]
                )
            else:
                raise Exception("Unit Error: Cannot subtract MeasurementLists with different units.")
        else:
            return MeasurementList(
                [value - obj for value in self.values]
            )
        
    def __rsub__(self,obj):    
        return MeasurementList(
            [obj - value for value in self.values]
        )

    def __mul__(self,obj):
        if(hasattr(obj,'__len__') and len(self) == len(obj) ):
            return MeasurementList(
                [self.values[i] * obj[i] for i in range(len(self))]
            )
        else:
            return MeasurementList(
                [value * obj for value in self.values]
            )

    def __rmul__(self,obj):
        if(hasattr(obj,'__len__') and len(self) == len(obj) ):
            return MeasurementList(
                [ obj[i] * self.values[i] for i in range(len(self))]
            )
        else:
            return MeasurementList(
                [obj * value for value in self.values]
            )
        
    def __truediv__(self,obj):
        if(hasattr(obj,'__len__') and len(self) == len(obj) ):
            return MeasurementList(
                [self.values[i] / obj[i] for i in range(len(self))]
            )
        else:
            return MeasurementList(
                [value / obj for value in self.values]
            )

    def __rtruediv__(self,obj):
        if(hasattr(obj,'__len__') and len(self) == len(obj) ):
            return MeasurementList(
                [obj[i] / self.values[i] for i in range(len(self))]
            )
        else:
            return MeasurementList(
                [obj / value for value in self.values]
            )

    def __pow__(self,obj):
        return MeasurementList(
            [value ** obj for value in self.values]
        )

    def __rpow__(self,obj):
        return MeasurementList(
            [obj ** value for value in self.values]
        )

    @staticmethod
    def sin(x):
        return MeasurementList(
            [Measurement.sin(measurement) for measurement in x.values]
        )

    @staticmethod
    def cos(x):
        return MeasurementList(
            [Measurement.cos(measurement) for measurement in x.values]
        )

    @staticmethod
    def tan(x):
        return MeasurementList(
            [Measurement.tan(measurement) for measurement in x.values]
        )

    @staticmethod
    def log(x):
        return MeasurementList(
            [Measurement.log(measurement) for measurement in x.values]
        )

    @staticmethod
    def asin(x):
        return MeasurementList(
            [Measurement.asin(measurement) for measurement in x.values]
        )
    
    @staticmethod
    def acos(x):
        return MeasurementList(
            [Measurement.acos(measurement) for measurement in x.values]
        )

    @staticmethod
    def atan(x):
        return MeasurementList(
            [Measurement.atan(measurement) for measurement in x.values]
        )