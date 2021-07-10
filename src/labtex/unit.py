import re
from typing import Union


class Unit:
    "SI Unit taking in a string."

    def __init__(self,unitString: Union[str,dict]):
        Unit.knownUnits = ['g','s','A','K','C','J','V','N','W','T','Pa','Hz','m']
        Unit.prefixes = {'n':1e-9,'u':1e-6,'q':1e-3,'c':1e-2,'k':1e3,'M':1e6,'G':1e9}
        
        # Given user string input, parse the units, prefixes and powers
        if(type(unitString) == str):
            self.units = dict.fromkeys(Unit.knownUnits)
            for unit in self.units:
                self.units[unit] = {'prefix':'','power':0}
            self.parse(unitString.replace(' ',''))
        
        # Used internally to construct a Unit from a dictionary of its units
        else:
            self.units = unitString

    def __repr__(self):
        unitoutput = []
        for unit in Unit.knownUnits:
            if (self.units[unit]['power'] != 0):
                if(self.units[unit]['power'] != 1):
                    unitoutput.append(f"{self.units[unit]['prefix']}{unit}^{self.units[unit]['power']}")
                else:
                    unitoutput.append(f"{self.units[unit]['prefix']}{unit}")

        return " ".join(unitoutput)

    def parse(self,unitString):
        "Decompose string into its constituent SI units."

        # Match a prefix
        prefix = re.compile('([numckMG])')
        # Match a known unit
        unit = re.compile('([gsAKCJVNWTm]|(?:Pa)|(?:Hz))')
        # Match a '^' followed optionally by '-' and then any number of digits
        rgxpower = re.compile('(\^)(\-?)(\d+)')

        i = 0
        while i < len(unitString):
            prefixmatch = prefix.match(unitString[i:])
            prefixfound = 1 if prefixmatch is not None else 0
            unitmatch = unit.match(unitString[i+prefixfound:])
            if (unitmatch is not None):
                unitname = unitmatch.group(1)
                powermatch = rgxpower.match(unitString[i+prefixfound+len(unitname):])
                powerlength = powermatch.span()[1] if powermatch != None else 0
                self.units[unitname] = {
                    'prefix': prefixmatch.group(1) if prefixfound else '',
                    'power': powermatch.group(2) + powermatch.group(3) if powermatch != None else 1
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
                        'power': powermatch.group(2) + powermatch.group(3) if powermatch else 1
                        }
                    i += len(unitname) + powerlength
            else:
                i += 1
        

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
                if(self.units[unit]["prefix"] == obj.units[unit]["prefix"]):
                    newunits[unit] = {
                        "prefix": self.units[unit]["prefix"],
                        "power": self.units[unit]["power"] + obj.units[unit]["power"]
                        }
                else:
                    raise Exception("Measurements have different prefixes. Multiplication not supported.")
            return Unit(newunits)
        else:
            return self

    def __rmul__(self,obj):
        return self

    def __truediv__(self,obj):
        if(isinstance(obj,Unit)):
            newunits = {}
            for unit in Unit.knownUnits:
                if(self.units[unit]["prefix"] == obj.units[unit]["prefix"]):
                    newunits[unit] = {
                        "prefix": self.units[unit]["prefix"],
                        "power": self.units[unit]["power"]-obj.units[unit]["power"]
                        }
                else:
                    raise Exception("Measurements have different prefixes. Division not supported.")
            return Unit(newunits)
        else:
            return self
    
    def __rtruediv__(self,obj):
        newunits = {
            unit: {
                "prefix": self.units[unit]["prefix"],
                "power": -self.units[unit]["power"]
            } for unit in Unit.knownUnits 
        }
        return Unit(newunits)
    
    def __pow__(self,obj):
        newunits = { 
            unit: {
                "prefix": self.units[unit]["prefix"],
                "power": self.units[unit]["power"] * obj
            } for unit in Unit.knownUnits 
        }
        return Unit(newunits)

