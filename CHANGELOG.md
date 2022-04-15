## Changelog

# To Be Implemented

- Derived Unit Conversion
- Better ML support with numpy (and a single unit (e.g. different implementation from M)
    - User can specify type of uncertainty to be used in a list
- M and ML classes
- m, s, kg, V, etc. global variables for multiplication which instantiate measurements with no error
- Documentation

# v0.4.0

Massive overhaul of unit parsing and `MeasurementList`s.
- Added eV and unit conversions eg. eV to Joule
- Added support for more prefixes up to 10^{\pm 12} (as Peta breaks parsing of Pascals)
- Corrected Unit Ordering
- Expose the plot to the end user for customization
- Added "/" support e.g. "m/s" parses the same as "m s^-1"
- Minor bug fixes

