# Light Curve Similarity Search

A python command line utility to searching for similar light curves useing kernelised distance and vantage points.

### Usage

Usage: ./simsearch param1 param2

param1: The input file name that contain time series object
param2: The top K most similar time series


For example:

python3 ./simsearch.py 10 # Will return ValueError - No input file containing time series passed

python3 ./simsearch.py 169975.dat_folded.txt 10

### Developers:

Created by Team 8 (Yihang Yan, Spandan Madan, Leonard Loo, Tomas Gudmundsson) for Team 2