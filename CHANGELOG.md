## Changelog

# Looking Forward

- CSV data import workflow
- Numpy input integration
- Interface with statistical packages for non-linear regression

# v0.6.0
- Reworked the document object to be more versatile and to allow live editing of the document
- Improved generation of unit axis labelling
- Added numpy integration for instantiating MeasurementLists
- Added nonlinear regression
- Added parameter estimation region visualisation to plotting
- Improved unittesting
# v0.5.0
- New extensive ![Documentation](https://www.cianlm.dev/labtex)! Examples and guides to be added in future updates.
- Improved plot appearance with latex-style font
- Fixed table bugs when dimensionless quantities are involved
# v0.4.3
- Fixed negative error propagation bug
# v0.4.1
- Documentation/guides coming very soon
- Fixed exponential and inverse tangent error propagation
- Fixed other minor bugs
# v0.4.0

New Features:
- Unit conversion of measurements between arbitrary units e.g. J to eV, mm^2 to m^2.
- Massive overhaul of unit parsing and `MeasurementList`s for extensibility and consistency.
- Added "/" support e.g. "m/s" parses the same as "m s^-1"
- Added element-wise uncertainties in `MeasurementList`s
- Added eV and unit conversions eg. eV to Joule
- Added support for more prefixes up to 10^{± 12} (as Peta breaks parsing of Pascals)

Other changes include:
- Added shorthand classes `M` and `ML` for `Measurement` and `MeasurementList` classes
- Exposed the `plt` plot object to the end user for customization
- Simplified and standardized printing of uncertainties
- Fixed Linear Regression statistical uncertainties
- Modularized testing
- Bug fixes of all kinds

