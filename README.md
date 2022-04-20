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
z = M(314,10,"V")
```
where `M` is an equivalent shorthand for `Measurement`. Note that the unit parsing supports all combinations of common units, prefixes and powers of units, eg. any of "nm^2", "C^-1", "kg m^2 s^-2", "J^3" etc. are supported.

Measurement instances support all operations (`+-*/` and `**`) as well as math functions with the error and units automatically propagated. Some examples are shown below.
```python
print(x)
# 1.1 ± 0.3 m

print(x + y)
# 3.3 ± 0.5 m

print(x * z)
# (35 ± 9) × 10^{1} V m

print(x ** 2)
# 1.2 ± 0.7 m^2

print(Measurement.tan(x / y))
# 0.5 ± 0.2  
```
Notice also that Measurements are rounded to the significant figures as dictated by the uncertainty.

For a list of measurements, the `MeasurementList` class functions identically to the `Measurement` class, only now taking a list of values. The uncertainty can be a list or a single value for all measurements.

```python
heights = MeasurementList([185,183,182,194,184,177],5,"cm")

print(heights)
# [185 ± 5, 183 ± 5, 182 ± 5, 194 ± 5, 184 ± 5, 177 ± 5] cm

print(200 - heights)
# [15 ± 5, 17 ± 5, 18 ± 5, 6 ± 5, 16 ± 5, 23 ± 5] cm
```
`MeasurementList`s also support all operations (`+-*/` and `**`) with themselves and with `Measurement`s. 

With two `MeasurementList` instances, they can be linearly regressed with the `LinearRegression` class.
```python
voltages = MeasurementList([1.3,3,5,7,8.5,10],1,"V")
temperatures = MeasurementList([23,55,67,82,88,96],[5,3,7,10,5,6],"C")

lobf = LinearRegression(voltages,temperatures)

print(lobf)
# m = 7 ± 1 V^{-1} C
# c = 27 ± 7 C
```
Observe that printing all `Measurement` and `MeasurementList` instances rounds the value to the largest significant figure of the error, as is convention.


For LaTeX template file output, the `Document` class can be used. Argument names are not required, they are shown here only for demonstration.
```python
doc = Document(title="Lab Report Template",author="CianLM")
```
Once `doc` has been instantiated, tables and graphs may be added to the document with their respective methods. Once again argument names are for demonstration and most are optional anyway.

```python
doc.table(
    nameandsymbol = ["Voltage, V","Temperature, T"],
    data = [voltages,temperatures],
    caption = "Voltage and Temperature Correlation"
)
```
This inserts the following into the `doc` instance.
```latex
\begin{table}[ht]
    \centering
    \caption{Voltage and Temperature Correlation}
    \label{tab:1}
    \begin{tabular}{c|cccccc}
        \toprule
            Voltage, V, ($\pm 1$ V) & 1 & 3 & 5 & 7 & 8 & 10 \\ 
            Temperature, T& $23 \pm 5 $ & $55 \pm 3 $ & $67 \pm 7 $ & $(8 \pm 1) \times 10^{1} $ & $88 \pm 5 $ & $96 \pm 6 $ \\ 
        \bottomrule
    \end{tabular}
\end{table}
```
which results in

![](https://github.com/CianLM/labtex/raw/master/figures/readmetable.png)


Alternatively if an `upright` table is preferred, this may be specified through the `style` argument.
```python
doc.table(
    nameandsymbol = ["Voltage, V", "Temperature, T"],
    data = [voltages,temperatures**2],
    caption = "Voltage and Temperature Sqaured Correlation",
    style = "upright"
)
```

Once again this inserts the following into the `doc` instance.
```latex
\begin{table}[ht]
    \centering
    \caption{Voltage and Temperature Sqaured Correlation}
    \label{tab:2}
    \begin{tabular}{*{2}c}
        \toprule
        Voltage, V, ($\pm 1$ V)  & Temperature, T \\ 
            \midrule
              1 & $(5 \pm 2) \times 10^{2} $  \\
              3 & $(30 \pm 3) \times 10^{2} $  \\
              5 & $(45 \pm 9) \times 10^{2} $  \\
              7 & $(7 \pm 2) \times 10^{3} $  \\
              8 & $(77 \pm 9) \times 10^{2} $  \\
              10& $(9 \pm 1) \times 10^{3} $ \\
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

This package is under active development. Feel free to submit a pull request or reach out with feature suggestions.