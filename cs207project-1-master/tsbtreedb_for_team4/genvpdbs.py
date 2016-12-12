#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# CS207 Group Project Part 7
# Created by Team 2 (Jonne Seleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah) for Team 4

import sys
import os
import random
import numpy as np

from unbalancedDB import connect
from crosscorr import kernel_dist, standardize
from makelcs import clear_dir
from settings import LIGHT_CURVES_DIR, DB_DIR, TS_LENGTH
import arraytimeseries as ats

# Global variables

HELP_MESSAGE = \
"""
Generate Vantage Point Index DBs

A python command line utility to generate vantage point DBs from light-curve files.

Usage: ./genvpdbs  [optional flags]

Optional flags:
  -h, --help    Show this help message and exit.
"""

def load_ts(LIGHT_CURVES_DIR):
    """Loads time series text files; returns dict keyed to filename"""
    timeseries_dict = {}
    for file in os.listdir(LIGHT_CURVES_DIR):
        if file.startswith("ts-") and file.endswith(".txt"):
            filepath = LIGHT_CURVES_DIR + file
            data = np.loadtxt(filepath)
            times, values = data.T
            ts = ats.ArrayTimeSeries(times=times,values=values)
            timeseries_dict[file] = ts
    return timeseries_dict

def pick_vantage_points(timeseries_dict,n=20):
    """Selects n light curves at random to serve as vantage points"""
    return random.sample(timeseries_dict.keys(), n)

def calc_distances(vp_k,timeseries_dict):
    """Calculates kernel distance between vantage point and all loaded light curves"""
    distances = []
    vp = standardize(timeseries_dict[vp_k])
    for k in timeseries_dict:
        if k != vp_k:
            k_dist = kernel_dist(vp, standardize(timeseries_dict[k]))
            distances.append((k_dist,k))
    return distances

def save_vp_dbs(vp,timeseries_dict):
    """ Creates unbalanced binary tree databases and saves them to disk"""
    sorted_ds = calc_distances(vp,timeseries_dict)

    # ts-13.txt -> vp_dbs/ts-13.dbdb
    db_filepath = DB_DIR + vp[:-4] + ".dbdb"
    db = connect(db_filepath)

    for dist_to_vp,ts_fn in sorted_ds:
        db.set(dist_to_vp, ts_fn)

    db.commit()
    db.close()

def create_vpdbs(n,LIGHT_CURVES_DIR):
    """
    Executes functions above:
        (1) Creates timeseries_dict from time series files on disk
        (2) Picks 20 vantage points at random
        (3) Calculates kernel distance between vantage points and generated time series (This can take a while)
        (4) Saves kernel distance indexes to disk as binary tree databases
    """
    print("Creating %d vantage point dbs" % n,end="")
    timeseries_dict = load_ts(LIGHT_CURVES_DIR)
    vantage_points = pick_vantage_points(timeseries_dict,n)
    clear_dir(DB_DIR)
    for vp in vantage_points:
        print('.', end="")
        save_vp_dbs(vp,timeseries_dict)
    print("Done.")

if __name__ == "__main__":
    """Enables this file to be run independently of simsearch as it's own CLU."""
    need_help = False

    # First, identify which flags were included
    for arg in sys.argv[1:]:
        if arg.lower() in ['-h','--help', 'help']: need_help = True

    while(True):
        if need_help:
            print (HELP_MESSAGE)
            break
        else:
            print("Starting...(May take a little while)")
            create_vpdbs(20,LIGHT_CURVES_DIR)
            break
