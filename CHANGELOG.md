## Changelog

# Looking Forward

- Interface with statistical packages for non-linear regression
- Documentation
# v0.4.0

New Features:
- Unit Conversion of measurements between arbitrary units e.g. J to eV, mm^2 to m^2.
- Massive overhaul of unit parsing and `MeasurementList`s for extensibility and consistency.
- Added "/" support e.g. "m/s" parses the same as "m s^-1"
- Added elementwise uncertainties in `MeasurementList`s
- Added eV and unit conversions eg. eV to Joule
- Added support for more prefixes up to 10^{± 12} (as Peta breaks parsing of Pascals)

Other changes include:
- Added shorthand classes `M` and `ML` for `Measurement` and `MeasurementList` classes
- Exposed the `plt` plot object to the end user for customization
- Simplified and standardized printing of uncertainties
- Fixed Linear Regression statistical uncertainties
- Modularized testing
- Bug fixes of all kinds

