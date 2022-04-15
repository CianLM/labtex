# labtex

## Purpose

This package provides a single solution to repetitive analysis tasks in a lab environment. If you are doing error propagation, linear regression or LaTeX tables/figures manually, this package automates the process.

## Features

- Measurement and MeasurementList classes with automatic:
  - Error propagation
  - Printing to correct significant figures
  - Unit parsing, propagation and conversion
- Linear regression
- Automatic table generation in three styles
- Automatic plot generation with matplotlib
- Template LaTeX file output with the generated figures and tables included

## Installation

Using `pip` or `pip3` the latest release can be installed with
```
pip3 install labtex
```

## Usage

For ease of use, you can import the package into your file's global namespace with
```python
from labtex import *
```
The rest of this section will assume the package is imported in this way. Alternatively do `import labtex as lt`.

Single measurements can be instantiated with `Measurement(value,uncertainty,unit)` where unit is a string that will be parsed.
```python
x = Measurement(1.1,0.3,"m")
y = Measurement(2.22,0.4,"m")
z = Measurement(314,10,"V")
```
Note that this unit parsing supports all combinations of common units, prefixes and powers of units, eg. any of "nm^2", "C^-1", "kg m^2 s^-2", "J^3" etc. are supported.

Measurement instances support all operations (`+-*/` and `**`) as well as math functions with the error and units automatically propagated. Some examples are shown below.
```python
print(x)
# 1.1 ± 0.3 m

print(x + y)
# 3.3 ± 0.5 m

print(x * z)
# 340 ± 90 V m

print(x ** 2)
# 1.2 ± 0.7 m^2

print(Measurement.tan(x / y))
# 2 ± 1 
```
Notice also that Measurements are rounded to the significant figures as dictated by the uncertainty.

For a list of measurements, the `MeasurementList` class functions identically to the `Measurement` class, only now taking a list of values. The uncertainty can be a list or a single value for all measurements.

```python
heights = MeasurementList([185,183,182,194,184,177],5,"cm")

print(heights)
# [185, 183, 182, 194, 184, 177] ± 5 cm

print(200 - heights)
# [15, 17, 18, 6, 16, 23] ± 5 cm
```

With two `MeasurementList` instances, they can be linearly regressed with the `LinearRegression` class.
```python
voltages = MeasurementList([1.3,3,5,7,8.5,10],5,"V")
temperatures = MeasurementList([23,55,67,82,88,96],20,"C")

lobf = LinearRegression(voltages,temperatures)

print(lobf)
# 8 ± 1 C V^-1 + 23 ± 6 C
```
Observe that printing all `Measurement` and `MeasurementList` instances rounds the value to the largest significant figure of the error, as is convention.


For LaTeX template file output, the `Document` class is used. Argument names are not required, they are shown here only for demonstration.
```python
doc = Document(title="Lab Report Template",author="CianLM")
```
Once `doc` has been instantiated, tables and graphs may be added to the document with their respective methods. Once again argument names are for demonstration and most are optional anyway.

```python
doc.table(
    listheads=["Voltage, V","Temperature, T"], 
    data=[voltages,temperatures],
    caption="Voltage and Temperature Table"
)
```
This inserts the following into the `doc` instance.
```latex
\begin{table}[ht]
        \centering
        \caption{Voltage Temperature Correlation}
        \label{tab:1}
        \begin{tabular}{*{7}c}
            \toprule
            Voltage, V, $\pm$ 3 V & 1 & 3 & 5 & 7 & 8 & 10 \\ 
            Temperature, T, $\pm$ 20 C & 20 & 60 & 70 & 80 & 90 & 100 \\ 
            \bottomrule
        \end{tabular}
    \end{table}
```
which results in
![](https://github.com/CianLM/labtex/raw/master/figures/readmetable.png)


Alternatively if an `upright` table is preferred, this may be specified through the `style` argument.
```python
doc.table(
    listheads = ["Voltage, V","Temperature, T"],
    data = [voltages,temperatures],
    caption = "Voltage Temperature Correlation",
    style = "upright"
)
```

Once again this inserts the following into the `doc` instance.
```latex
\begin{table}[ht]
        \centering
        \caption{Voltage Temperature Correlation}
        \label{tab:2}
        \begin{tabular}{*{2}c}
            \toprule
            Voltage, V, $\pm$ 3 V  & Temperature, T, $\pm$ 20 C  \\ 
            \midrule
              1 & 20  \\
              3 & 60  \\
              5 & 70  \\
              7 & 80  \\
              8 & 90  \\
              10& 100 \\
            \bottomrule
        \end{tabular}
    \end{table}
```
which results in
![](https://github.com/CianLM/labtex/raw/master/figures/readmetable2.png)

For a graph, a similar process occurs.
```python
doc.graph(
    data = [voltages,temperatures],
    title = "Voltage Temperature Correlation",
    xnameandsymbol = "Voltage, V",
    ynameandsymbol = "Temperature, T",
    caption = "Linear Regression of Voltage and Temperature"
)
# labtex: Wrote to 'figures/graph1.png'.
```

This generates the graph below and saves it to `figures/graph1.png`. If you want your graphs elsewhere than `figures/`, you may change `Document.graphfolder` at your convenience.

![](https://github.com/CianLM/labtex/raw/master/figures/graph1.png)

Once you have added all your tables and graphs to the `doc` object, you may save this file as shown below. The default write directory is `tex/` relative to root. This directory is also customisable with `Document.texfolder`.

```python
doc.save("test")
# labtex: Wrote to 'tex/test.tex'.
```


## Contributions

Feel free to submit a pull request or reach out with feature suggestions.
