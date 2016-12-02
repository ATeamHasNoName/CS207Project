#!/bin/sh

echo "Python starting"
echo "generate 1000 TS data..."
python genTSData.py
echo "Done."
echo "Randomly choose 20 vps and create 20 database indexes..."
python genDB.py
echo "Done."
python findKthSimilarity.py $1 $2
echo "All done."
