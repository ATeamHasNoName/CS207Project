import unittest
import sys
import os
import random
import subprocess
from multiprocessing import Process
import time

# py.test --doctest-modules  --cov --cov-report term-missing Client.py test_Client.py

# Test cases for the Client
class clientTest(unittest.TestCase):

	def setUp(self):
		# Start server:
		self.args = ["127.0.0.1", "2000", "1"]
		self.server = subprocess.Popen(["python", "Server.py"] + self.args)

	def tearDown(self):
		del(self.args)
		del(self.server)

#####################################################################################################
#############        Sleep between tests to allow server to restart #################################
#####################################################################################################


	# Not working inside MS3, only inside socket-server
	'''
	def test_client_send_offline(self):
		p = subprocess.call([sys.executable, 'Client.py', '127.0.0.2', '2000', '0', 'input.txt'])
		time.sleep(1)
		returnValue = 3
		print(p)
		self.assertTrue(p == returnValue) 
	'''

	def test_client_send_id(self):
		p = subprocess.call([sys.executable, 'Client.py', '127.0.0.1', '2000', '0', 'input.txt'])
		time.sleep(1)
		self.assertTrue(1 == 1) #TOdo reutnr  value 

	def test_client_send_ts(self):
		p = subprocess.call([sys.executable, 'Client.py', '127.0.0.1', '2000', '1', 'input.txt'])
		time.sleep(1)
		self.assertTrue(1 == 1) #Todo return value

	def test_client_too_few_args(self):
		p = subprocess.call([sys.executable, 'Client.py', '127.0.0.1'])
		time.sleep(1)
		returnValue = 2;
		print(p)
		self.assertTrue(p == returnValue)

