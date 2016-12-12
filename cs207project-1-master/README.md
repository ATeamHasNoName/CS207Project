# GitRdone4 Time Series

A flexible collection of python classs for manipulating and analyzing time series data.

[![Build Status](https://travis-ci.org/gitrdone4/cs207project.svg?branch=master)](https://travis-ci.org/gitrdone4/cs207project)

[![Coverage Status](https://coveralls.io/repos/github/gitrdone4/cs207project/badge.svg?branch=master)](https://coveralls.io/github/gitrdone4/cs207project?branch=master)

Final group project for Harvard's CS 207 course, [Systems Development for Computational Science](https://iacs-cs207.github.io/cs207-2016/) (Fall 2016).

### Overview

Time series are two-dimensional (or higher) arrays of numeric data, where ordered time-values are bound to specific data points that represent specific outcomes, measurements, or other values associated with specific times.  While time series data can be stored using traditional arrays or tables, the classes included in this library make working with these types of data sets in python easier by enforcing the core properties of a time series at a class level. For example, in a time series no two times can be repeated. And every represented value needs a time associated with it. By creating and manipulating data-sets using these classes, these properties are enforced at all times.

### Additional Features

1. Supports adding, subtracting, multiplying, and other manipulations on fixed-length data sets.
2. Support manipulation of time-series streams (i.e., data sets that are ongoing, and don't have fixed storage)
3. Supports piecewise linear interpolation of non-existing values within the domain of existing fixed-length data-sets.
4. Supports ongoing standard deviation and mean calculations for  stream-based datasets.

### Required Python Modules

- [NumPy](http://www.numpy.org)
- [pytest](http://doc.pytest.org/en/latest/)

### Developers:
- Jonne Seleva
- Nathaniel Burbank
- Nicholas Ruta
- Rohan Thavarajah