# Light Curve Similarity Search

A python command line utility to searching for similar light curves using kernelised distance and vantage points.

### Usage

Usage: 
STEP 1 : Enter the command "./simsearch.sh" into the terminal
STEP 2 : Follow the prompts and supply the program the parameters it asks for

The parameters will be -
param1: The input file name that contain time series
param2: The number of top time series to return 


####### An example of how it should work out for a smaller dataset of 30 time series and 5 vantage points#########

(py35)spandanmadan1@Spandans-MacBook-Pro:~/Desktop/cs207project-1/SimSearch$ ./simsearch.sh 
This script checks the distance of a new time series against a database. Please enter the filename -
169975.dat_folded.txt
Now, enter the number of top results to return!
10
Not stored in disk, calculate distances
Working on vantage point:  0
Working on vantage point:  1
Working on vantage point:  2
Working on vantage point:  3
Working on vantage point:  4
IDs of the top  10 time series are 15,8,3,2,13,26,23,24,27,5
(py35) spandanmadan1@Spandans-MacBook-Pro:~/Desktop/cs207project-1/SimSearch$ 

####### Example End ##########3
### Developers:
Created by Team 8 (Yihang Yan, Spandan Madan, Leonard Loo, Tomas Gudmundsson) for Team 2
