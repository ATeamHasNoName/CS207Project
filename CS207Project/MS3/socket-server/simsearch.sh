echo "This script checks the distance of a new time series against a database. Please enter the filename -"
read filename
echo "Now, enter the number of top results to return!"
read topcount
python ../Distance_from_known_ts.py $filename $topcount
