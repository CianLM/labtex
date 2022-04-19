import re
from typing import Union
import math

# TODO
# MeasurementList type compatability

class Unit:
    "SI Unit taking in a string."
    # Not Supported: mol (moles), cd (candela)
    baseUnits = ['m','g','s','A','K']

    derivedUnits = {
    'J': ['kg m^2 s^-2'],
    'V': ['kg m^2 s^-3 A^-1'],
    'N': ['kg m s^-2'],
    'W': ['kg m^2 s^-3'],
    'T': ['kg s^-2 A^-1'],
    'Pa': ['kg m^-1 s^-2'],
    'Hz': ['s^-1'],
    'C' : ['K'], # , lambda C: C + 273.15, lambda K: K - 273.15
    'eV' : ['kg m^2 s^-2', 1.602176634e-19],
    
    }

    knownUnits = list(derivedUnits.keys())
    knownUnits += baseUnits

    prefixes = {
    # 'a':1e-18,
    # 'f':1e-15,
    'p':1e-12,
    'n':1e-9,
    'u':1e-6,
    'm':1e-3,
    'c':1e-2,
    '' :1,
    'k':1e3,
    'M':1e6,
    'G':1e9,
    'T':1e12,
    # 'P':1e15, # breaks parsing for Pa (Pascals)
    # 'E':1e18
    }

    def __init__(self,unitString: Union[str,dict]):

        # Given user string input, parse the units, prefixes and powers
        if(type(unitString) == str):
            self.units = dict.fromkeys(Unit.knownUnits)
            for unit in self.units:
                self.units[unit] = {'prefix':'', 'power':0}
            self.parse(unitString.replace('{','(').replace('}',')'))
        
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

        # Match a prefix that is followed by a non-whitespace character
        prefix = re.compile(f'([{"".join(prefix for prefix in Unit.prefixes.keys())}])\\B')
        # Match a known unit
        # Compiles to '([JVNWTmgsACK]|(?:Pa)|(?:Hz))' for default (base + derived) units
        unit = re.compile(f"([{''.join([ unit_str if len(unit_str) == 1 else '' for unit_str in Unit.knownUnits])}]|{'|'.join([ ('(?:' + unit_str + ')') for unit_str in filter(lambda x: len(x) > 1, Unit.knownUnits) ])})") 
        # Match a '^' followed optionally by '-' and then any number of digits
        power = re.compile('(\^)(\-?)(\d+)')
        # power = re.compile(r'\^(?:-?\d+)')
        flip = False

        i = 0
        while i < len(unitString):
            if (unitString[i] == '/'):
                if (flip):
                    raise Exception("labtex Unit Parsing Error: Cannot have two '/' characters.")
                flip = True
                i += 1

            prefixmatch = prefix.match(unitString[i:])
            prefixfound = prefixmatch is not None
            # As all prefixes are of length 1
            unitmatch = unit.match(unitString[i+prefixfound:])
            # print(f"unitmatch: {unitmatch}")
            if (unitmatch is None):
                if (unitString[i] in ['(',')']):
                    raise Exception('labtex Unit Parsing Error: Parentheses are not supported. Use negative exponents or a \'/\' instead.')
                if (unitString[i] not in [' ','1']):
                    raise Exception(f'labtex Unit Parsing Error: Unknown character: \'{unitString[i]}\'. If this is intended, you can add it to the base units/prefixes with `Unit.baseUnits` and `Unit.prefixes`.')
                i += 1
                continue

            prefixstr = prefixmatch.group(1) if prefixfound else ''
            unitstr = unitmatch.group(1)
            powermatch = power.match(unitString[i+prefixfound+len(unitstr):])

            self.units[unitstr] = {
                "prefix": prefixstr,
                "power": (-1)**(2-flip) * int(powermatch.group(2) + powermatch.group(3) if powermatch else 1)
            }

            i += len(prefixstr) + len(unitstr) + (powermatch.span()[1] if powermatch else 0)

    @staticmethod
    def unitless(self):
        return all([ dim['power'] == 0 for dim in self.units.values() ])

    @staticmethod
    def singular(self): # a unit with a single dimension
        return sum([*map(lambda x: x['power'] != 0, self.units.values())]) == 1

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
                # If one of the units is unitless, return the other, where prefix='' and power=0 by default.
                if((self.units[unit]["power"] != 0) ^ (obj.units[unit]["power"] != 0) ):
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
                    raise Exception("Units have different prefixes. Multiplication not supported.")
            return Unit(newunits)
        else:
            return self

    def __rmul__(self,obj):
        return self.__mul__(obj)


    def __truediv__(self,obj):
        if(isinstance(obj,Unit)):
            newunits = {}
            for unit in Unit.knownUnits:
                if((self.units[unit]["power"] != 0) ^ (obj.units[unit]["power"] != 0 )):
                    newunits[unit] = {
                        "prefix": self.units[unit]["prefix"] + obj.units[unit]["prefix"],
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

class U(Unit):
    pass