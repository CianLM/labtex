import re
from typing import Union
import math

# TODO
# MeasurementList type compatability

class Unit:
    "SI Unit taking in a string."
    # Not Supported: mol (moles), cd (candela)
    baseUnits = ['m','g','s','A','C','K']

    derivedUnits = {
    'J':'kg m^2 s^-2',
    'V':'kg m^2 s^-3 A^-1',
    'N':'kg m s^-2',
    'W':'kg m^2 s^-3',
    'T':'kg s^-2 A^-1',
    'Pa':'kg m^-1 s^-2',
    'Hz': 's^-1'
    }

    # TODO: add eV (electron volts) and K (kelvin)

    knownUnits = list(derivedUnits.keys())
    knownUnits += baseUnits

    prefixes = {
    'a':1e-18,
    'f':1e-15,
    'p':1e-12,
    'n':1e-9,
    'u':1e-6,
    'm':1e-3,
    'c':1e-2,
    '':1,
    'k':1e3,
    'M':1e6,
    'G':1e9,
    'T':1e12,
    'P':1e15,
    'E':1e18
    }


    def __init__(self,unitString: Union[str,dict]):

        
        # Given user string input, parse the units, prefixes and powers
        if(type(unitString) == str):
            self.units = dict.fromkeys(Unit.knownUnits)
            for unit in self.units:
                self.units[unit] = {'prefix':'', 'power':0}
            self.parse( unitString.replace(' ','').replace('{','').replace('}','') )
        
        # Used internally to construct a Unit from a dictionary of its units
        else:
            self.units = unitString

    def __repr__(self):
        unitoutput = []
        for unit in Unit.knownUnits:
            if (self.units[unit]['power'] != 0):
                if(self.units[unit]['power'] != 1):
                    unitoutput.append(f"{self.units[unit]['prefix']}{unit}^{ self.units[unit]['power'] if self.units[unit]['power'] > 0 else '{' + str(self.units[unit]['power']) + '}'}")
                else:
                    unitoutput.append(f"{self.units[unit]['prefix']}{unit}")

        return " ".join(unitoutput)

    def parse(self,unitString):
        "Decompose string into its constituent SI units."

        # Match a prefix
        prefix = re.compile(f'([{"".join(prefix for prefix in Unit.prefixes.keys())}])')
        # Match a known unit
        # Compiles to '([gsAKCJVNWTm]|(?:Pa)|(?:Hz))' for default units
        unit = re.compile(f"([{''.join([ unit_str if len(unit_str) == 1 else '' for unit_str in Unit.knownUnits])}]|{'|'.join([ ('(?:' + unit_str + ')') for unit_str in filter(lambda x: len(x) > 1, Unit.knownUnits) ])})") 
        # Match a '^' followed optionally by '-' and then any number of digits
        rgxpower = re.compile('(\^)(\-?)(\d+)')
        flip = False

        i = 0
        while i < len(unitString):
            if (unitString[i] == "/"):
                flip = True
                i += 1

            prefixmatch = prefix.match(unitString[i:])
            prefixfound = prefixmatch is not None
            unitmatch = unit.match(unitString[i+prefixfound:])
            if (unitmatch is not None):
                unitname = unitmatch.group(1)
                powermatch = rgxpower.match(unitString[i+prefixfound+len(unitname):])
                powerlength = powermatch.span()[1] if powermatch != None else 0
                self.units[unitname] = {
                    'prefix': prefixmatch.group(1) if prefixfound else '',
                    'power': (-1)**(2-flip) * int(powermatch.group(2) + powermatch.group(3) if powermatch != None else 1)
                    }
                i += prefixfound + len(unitname) + powerlength

            # account for 'm' as a prefix match but no succeeding unit
            elif (prefixfound):
                unitmatch = unit.match(unitString[i:])
                if(unitmatch is not None):
                    unitname = unitmatch.group(1)
                    powermatch = rgxpower.match(unitString[i+len(unitname):])
                    powerlength = powermatch.span()[1] if powermatch != None else 0
                    self.units[unitname] = {
                        'prefix': '',
                        'power': (-1)**(2-flip) * int(powermatch.group(2) + powermatch.group(3) if powermatch else 1)
                        }
                    i += len(unitname) + powerlength
                
                else:
                    raise Exception(f"labtex-PE2: Error in unit parsing with unknown character: {unitString[i]} P:{prefixmatch} U:{unitmatch}")
            else:
                raise Exception(f"labtex-PE1: Error in unit parsing with unknown character: {unitString[i]} P:{prefixmatch} U:{unitmatch}")
        
    @staticmethod
    def unitless(self):
        return all([ dim['power'] == 0 for dim in self.units.values() ])

    @staticmethod
    def singular(self): # only a single dimension has a non zero power
        return sum([*map(lambda x: x['power'] != 0,self.units.values())]) == 1

    @staticmethod
    def singularunit(self):
        if(Unit.singular(self)):
            for unit in self.units.values():
                if(unit["power"] != 0):
                    return unit
        else:
            return False


    def __eq__(self,obj):
        "Check if two Units are the same."
        if (isinstance(obj,Unit)):
            return all(self.units[unit] == obj.units[unit] for unit in Unit.knownUnits)
        return False

    def __mul__(self,obj):
        "Multiply two Units."
        if(isinstance(obj,Unit)):
            newunits = {}
            for unit in Unit.knownUnits:
                if((self.units[unit]["power"] > 0) ^ (obj.units[unit]["power"] > 0) ):
                    newunits[unit] = {
                        "prefix": self.units[unit]["prefix"] + obj.units[unit]["prefix"],
                        "power": self.units[unit]["power"] + obj.units[unit]["power"]
                    }
                elif(self.units[unit]["prefix"] == obj.units[unit]["prefix"]):
                    newunits[unit] = {
                        "prefix": self.units[unit]["prefix"] if self.units[unit]["power"] + obj.units[unit]["power"] != 0 else "",
                        "power": self.units[unit]["power"] + obj.units[unit]["power"]
                        }
                else:
                    raise Exception("Measurements have different prefixes. Multiplication not supported.")
            return Unit(newunits)
        else:
            # We require only a single dimension present otherwise we dont know which dimension to change the prefix of.
            if(Unit.singular(self) and int(math.log10(obj)) == math.log10(obj)):
                singularunit = Unit.singularunit(self)
                multiplicativefactor = obj**(1/singularunit["power"])
                if(Unit.prefixes[singularunit["prefix"]] * multiplicativefactor in Unit.prefixes.values()):
                    newunits = self.units.copy()
                    for unit in Unit.knownUnits:
                        if(self.units[unit] == singularunit):
                            # find the key that corresponds to this value
                            newunits[unit] = {
                                "prefix": list(Unit.prefixes.keys())[list(Unit.prefixes.values()).index(
                                Unit.prefixes[singularunit["prefix"]] * multiplicativefactor
                            )],
                                "power": self.units[unit]["power"]
                            }

                    return Unit(newunits)
        return self

    def __rmul__(self,obj):
        return self.__mul__(obj)


    def __truediv__(self,obj):
        if(isinstance(obj,Unit)):
            newunits = {}
            for unit in Unit.knownUnits:
                if(self.units[unit]["power"] > 0 ^ obj.units[unit]["power"] > 0 ):
                    newunits[unit] = {
                        "prefix": self.units[unit]["prefix"] + obj.units[unit]["power"],
                        "power": self.units[unit]["power"] - obj.units[unit]["power"]
                    }
                elif(self.units[unit]["prefix"] == obj.units[unit]["prefix"]):
                    newunits[unit] = {
                        "prefix": self.units[unit]["prefix"] if self.units[unit]["power"] - obj.units[unit]["power"] != 0 else "",
                        "power": self.units[unit]["power"] - obj.units[unit]["power"]
                        }
                else:
                    raise Exception("Measurements have different prefixes. Division not supported.")
            return Unit(newunits)
        else:
            return self.__mul__(1/obj)
    
    def __rtruediv__(self,obj):
        newunits = {
            unit: {
                "prefix": self.units[unit]["prefix"],
                "power": -self.units[unit]["power"]
            } for unit in Unit.knownUnits 
        }

        tmpUnit = Unit(newunits)
        return tmpUnit.__mul__(obj)

    def __pow__(self,obj):
        newunits = { 
            unit: {
                "prefix": self.units[unit]["prefix"],
                "power": self.units[unit]["power"] * obj
            } for unit in Unit.knownUnits 
        }
        return Unit(newunits)

