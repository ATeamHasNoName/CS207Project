============
CS207 Project for Team 8 - ATeamHasNoName
============

This project was developed for the harvard graduate class CS207.

Project Overview
========

This repository enables management of time series data, which is usually composed of times and values (times being optional). Such data can come often in real life appications where any quantity is being measured over time. This project offers two fold advantages over logging information in standard arrays - Firstly, it handles the data by utilizing efficient data structures optimized to handle faster calculations. Secondly,it is robust structure optiized to handle time series data - with checks and tests being forced on the data input and output making the workflow more robust. Some specific functions optimized in this project include - insertion & deletion of time series, online mean and standard deviation calculation. Further, it allows finding the closest time series in a database to a new time series entered by a client.

Specific Functionalities 
===================

1. Supports adding, subtracting, multiplying, and other manipulations on fixed-length data sets.
2. Support manipulation of time-series streams (i.e., data sets that are ongoing, and don't have fixed storage)
3. Supports piecewise linear interpolation of non-existing values within the domain of existing fixed-length data-sets.
4. Supports ongoing standard deviation and mean calculations for stream-based datasets.


Installation and Testing
========================
1. Clone the repository using 'git clone '
2. Open Terminal and enter into the cloned directory
3. Run 'python setup.py install' in terminal
4. To run tests, run 'python setup.py test' in the terminal.


Requirements
=======================

* pytest
* numpy


Developers
===========

* Spandan Madan
* Leonard Loo
* Yihang Yan
* Tomas Arnar Gudmundsson


Note
====

This project has been set up using PyScaffold 2.5.7. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.