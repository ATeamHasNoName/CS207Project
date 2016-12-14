# CS 207 Project Fall 2016

ATeamHasNoName group members:
- Leonard Loo
- Spandan Madan
- Tomas Arnar Gudmundsson
- Yihang Yan

[![Build Status](https://travis-ci.org/ATeamHasNoName/CS207Project.svg?branch=master)](https://travis-ci.org/ATeamHasNoName/CS207Project)

[![Coverage Status](https://coveralls.io/repos/github/ATeamHasNoName/CS207Project/badge.svg?branch=master&test=1)](https://coveralls.io/github/ATeamHasNoName/CS207Project?branch=master&test=1)

Instructions for installing on new EC2 instance:

1) Launch fresh Ubuntu instance on EC2

2) Clone our project repo: <code>cd ~ && git clone https://github.com/ATeamHasNoName/CS207Project.git</code>

3) Run the initial setup script (similar to lab 11): <code>cd ~/CS207Project && bash ./initialsetup.sh</code>

4) Setup PostgreSQL as such (similar to lab 11): 
- <code>sudo -u postgres psql</code>, and inside psql console:
- <code>alter user postgres password 'password';</code>
- <code>create user ubuntu createdb createuser password 'cs207password';</code>
- <code>create database ubuntu owner ubuntu;</code>

5) Go into our MS3 folder: <code>cd ~/CS207Project/CS207Project/MS3</code>

6) Run the server setup script: <code>bash bin/serversetup.sh</code>. Note that you might have to run this serversetup.sh file twice for portalocker to be successfully installed due to some unknown race condition in the script.

The server is now up and running and you can test the various functions. Note that everytime you run the <code>serversetup.sh</code> file you will clear all databases! Also you have to run the <code>serversetup.sh</code> file from the <code>MS3</code> directory.

Here's the Extra Credit we worked on:

1) Realized a fix in the serversetup.sh script where we have to run <code>sudo pkill -f python</code>, and Fuk promised extra credit.

2) Upon storing a new time series, we do multiple things: A) Insert the kernel distance between this time series and all vantage points into the respective Red Black Trees, B) When there are more than 50 time series inserted, the vantage points will be resampled and Red Black Trees rebuilt

3) FileStorageManager uses a smart cache in memory to prevent too many retrievals from disk. Specifically, it keeps track of the number of times a time series ID gets called, and stores the most frequently accessed time series in memory for fast retrieval.

4) Part 10's range queries such as mean_in, and std_in can be chained together.

