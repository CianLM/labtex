import copy
import math
from numbers import Number
from typing import Union
from labtex.unit import Unit
from labtex.unit import factorandbasedims

class Measurement:
    """Base Class for all single valued measurements with uncertainties and SI units.
    To instantiate use `Measurement(value, uncertainty, unit)`. For example,
    >>> x = Measurement(1.234, 0.01, "m")
    >>> print(x)
    1.23 ± 0.01 m
    """
    def __init__(self, value: float, uncertainty: float = 0, unit: Union[Unit,str] = ""):
        "Create a measurement with a value, uncertainty and SI Unit."
        self.value = value
        self.uncertainty = uncertainty
        self.relativeuncertainty = self.uncertainty / self.value if self.value != 0 else 0

        self.unit = unit if (isinstance(unit,Unit)) else Unit(unit)
    
    def __repr__(self):
        "Print string with sigfigs up to uncertainty."
        if(self.uncertainty == 0):
            return str(self.value) + " " + str(self.unit)

        sigdigits = -math.floor(math.log10(self.uncertainty))
        # To account for rounding up of uncertainty before applying it,
        # eg. 98 => sigdigits = -1 but round(98,-1) => 100 so we apply again to get -2.
        sigdigits = -math.floor(math.log10(round(self.uncertainty,sigdigits)))
        
        if(sigdigits >= 3): # Factored uncertainty e.g. (... ± 1) × 10^-2 
            return f"({round(self.value * 10**sigdigits)} ± {round(self.uncertainty * 10**sigdigits)}) × 10^{{{-sigdigits}}} {self.unit}"
        elif(sigdigits > 0): # Decimal uncertainty e.g. ± 0.1
            return f"{round(self.value,sigdigits)} ± {round(self.uncertainty,sigdigits)} {self.unit}"
        elif(sigdigits == 0): # Single digit uncertainty: remove decimal points from the float data type
            return f"{round(self.value)} ± {round(self.uncertainty)} {self.unit}"
        else: # Factored uncertainty e.g. (... ± 1) × 10^2
            return f"({round(self.value * 10**sigdigits)} ± {round(self.uncertainty * 10**sigdigits)}) × 10^{{{-sigdigits}}} {self.unit}"
    
    def __add__(self,obj):
        "Add two measurements."

        # Addition necessitates independent variables
        if(self == obj):
            return Measurement(
            self.value * 2,
            self.uncertainty * 2,
            self.unit
        )

        if(isinstance(obj,Measurement)):
            if(self.unit == obj.unit):
                return Measurement(
                    self.value + obj.value,
                    math.hypot(self.uncertainty,obj.uncertainty),
                    self.unit
            )
            factor1, basedims1 = factorandbasedims(self.unit)
            factor2, basedims2 = factorandbasedims(obj.unit)
            if(basedims1 == basedims2):
                return self + obj.to(self.unit)
            else:
                raise Exception(f"Cannot add measurements with different units: {self.unit} and {obj.unit}")

        # For a constant with no uncertainty
        if(isinstance(obj,Number)):
            return Measurement(
                self.value + obj,
                self.uncertainty,
                self.unit
            )
        if(isinstance(obj,list)):
            raise Exception("Cannot add a Measurement to a list. Convert list to MeasurementList first.")
        else:
            return NotImplemented
    
    def __radd__(self,obj):
        return self.__add__(obj)

    def __neg__(self):
        "Negate a measurement."
        return Measurement(
            -self.value,
            self.uncertainty,
            self.unit
        )
        
    def __sub__(self,obj):
        return self.__add__(-obj)
        
    def __rsub__(self,obj):
        return self.__neg__().__add__(obj)

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
            # If the unit objects share a dimension with different prefixes we need to convert
            # Note this cannot be implemented in the unit class as it affects the measurement value
            newobj = copy.deepcopy(obj)
            for unit in Unit.knownUnits:
                if (self.unit.units[unit]['power'] != 0 
                    and obj.unit.units[unit]['power'] != 0
                    and self.unit.units[unit]['prefix'] != obj.unit.units[unit]['prefix']):
                    newobj.value *= (Unit.prefixes[obj.unit.units[unit]['prefix']] / Unit.prefixes[self.unit.units[unit]['prefix']])**obj.unit.units[unit]['power']
                    newobj.unit.units[unit]['prefix'] = self.unit.units[unit]['prefix']
                    newobj.relativeuncertainty = newobj.uncertainty / newobj.value
            return Measurement(
                self.value * newobj.value,
                abs(self.value * newobj.value) * math.hypot(self.relativeuncertainty, newobj.relativeuncertainty),
                self.unit * newobj.unit
            )

        if(isinstance(obj,Number)):
            return Measurement(
                self.value * obj,
                self.uncertainty * abs(obj),
                self.unit
            )
        if(isinstance(obj,list)):
            raise Exception("Cannot multiply a Measurement by a list. Convert list to MeasurementList first.")
        else:
            return NotImplemented
            
    def __rmul__(self,obj):
        return self.__mul__(obj)

    
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
            newobj = copy.deepcopy(obj)
            for unit in Unit.knownUnits:
                if (self.unit.units[unit]['power'] != 0 
                    and obj.unit.units[unit]['power'] != 0
                    and self.unit.units[unit]['prefix'] != obj.unit.units[unit]['prefix']):
                    newobj.value *= (Unit.prefixes[obj.unit.units[unit]['prefix']] / Unit.prefixes[self.unit.units[unit]['prefix']])**obj.unit.units[unit]['power']
                    newobj.unit.units[unit]['prefix'] = self.unit.units[unit]['prefix']
                    newobj.relativeuncertainty = newobj.uncertainty / newobj.value
            return Measurement(
                self.value / newobj.value,
                abs(self.value / newobj.value) * math.hypot(self.relativeuncertainty,newobj.relativeuncertainty),
                self.unit / newobj.unit
            )

        if(isinstance(obj,Number)):
            return Measurement(
                self.value / obj,
                self.uncertainty / abs(obj),
                self.unit
            )
        if(isinstance(obj,list)):
            raise Exception("Cannot multiply a Measurement by a list. Convert list to MeasurementList first.")
        else:
            return NotImplemented

    def __rtruediv__(self,obj):
        "Reverse division to accommodate constant / measurement."
        if(isinstance(obj,Number)):
            return Measurement(
                obj / self.value,
                abs(obj / self.value) * self.relativeuncertainty,
                obj / self.unit
            )
        else:
            return NotImplemented

    def __pow__(self,obj):
        "Raising a measurement to a constant power."
        if(isinstance(obj,Measurement)):
            if(Unit.unitless(obj.unit)):
                return Measurement(
                    self.value ** obj.value,
                     abs(self.value ** obj.value) * math.sqrt(
                        (obj.value * self.relativeuncertainty)**2 + (math.log(obj.value) * obj.uncertainty)**2
                        ),
                    self.unit ** obj.value
                )
            else:
                raise Exception("Cannot raise a constant to a dimensional quantity. Units: " + str(self.unit))
        if(isinstance(obj,Number)):
            return Measurement(
                self.value ** obj,
                abs(self.value ** obj * obj) * self.relativeuncertainty,
                self.unit ** obj
            )
        else:
            return NotImplemented
    
    def __rpow__(self,obj):
        "Reverse power for constant ** measurement."
        if(isinstance(obj,Number)):
            if(Unit.unitless(self.unit)):
                return Measurement(
                    obj ** self.value,
                    abs(obj ** self.value  * math.log(obj)) * self.uncertainty,
                    ""
                )
            else:
                raise Exception("Cannot raise a constant to a dimensional quantity. Units: " + str(self.unit))
        else:
            return NotImplemented

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
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.unit}")

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
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.unit}")

    @staticmethod
    def tan(x):
        "Tangent function on a Measurement."
        if(Unit.unitless(x.unit)):
            return Measurement(
                math.tan(x.value),
                x.uncertainty / math.cos(x.value)**2 ,
                ""
            )
        else:
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.unit}")
    
    @staticmethod
    def log(x):
        "Natural log function on a Measurement."
        if(Unit.unitless(x.unit)):
            return Measurement(
                math.log(x.value),
                math.fabs(x.relativeuncertainty),
                ""
            )
        else:
            raise Exception(f"Log functions take in dimensionless quantities. Input has units: {x.unit}")
    
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
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.unit}")
    
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
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.unit}")

    @staticmethod
    def atan(x):
        "Inverse tangent function on a Measurement."
        if(Unit.unitless(x.unit)):
            return Measurement(
                math.atan(x.value),
                x.uncertainty / (1 + x.value**2),
                ""
            )
        else:
            raise Exception(f"Trigonometric functions take in dimensionless quantities. Input has units: {x.unit}")
 
    def to(self, unit : Union[str,Unit]):
        "Convert the units of a measurement to one with the same dimensions."
        unit = unit if isinstance(unit,Unit) else Unit(unit)
        from_factor, from_basedims = factorandbasedims(self.unit)
        to_factor, to_basedims = factorandbasedims(unit)
        if(from_basedims == to_basedims):
            return Measurement(
                self.value * from_factor / to_factor,
                self.uncertainty * from_factor / to_factor,
                unit
            )
        else:
            print(from_factor, from_basedims)
            print(to_factor, to_basedims)
            raise Exception(f"Dimension Error: Cannot convert from {self.unit} to {unit} because they have different dimensions.")
        
class M(Measurement):
    "Base Class for all single valued measurements with uncertainties and SI units."
    pass

