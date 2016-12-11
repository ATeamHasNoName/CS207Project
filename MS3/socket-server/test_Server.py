import unittest
import sys
import os
import subprocess
from multiprocessing import Process

# py.test --doctest-modules  --cov --cov-report term-missing Server.py test_Server.py

# Test cases for the Server
class serverTest(unittest.TestCase):

	def setUp(self):
		# Start server:
		#sys.argv = ['127.0.0.1', '25000']
		#exec(open("Server.py").read())
		#p1 = subprocess.call([sys.executable, 'Server.py', '127.0.0.1', '25000', '1'])
		#p2 = subprocess.call([sys.executable, 'Client.py', '127.0.0.1', '25000', '1', 'input.txt'])
		b = 5

	# Note that these tests are run in sequential order

	def test_start_server_one_client(self):
		args = ["127.0.0.1", "2000", "2"]
		p = subprocess.Popen(["python", "Server.py"] + args)
		p1 = subprocess.call([sys.executable, 'Client.py', '127.0.0.1', '2000', '1', 'input.txt'])
		self.assertTrue(1 == 1) #Todo add value

	def test_start_too_few_args(self):
		args = ["127.0.0.2", "2000", "2"]
		p = subprocess.call([sys.executable, 'Server.py', '127.0.0.1'])
		p1 = subprocess.Popen(["python", "Server.py"] + args)
		returnValue = 2
		self.assertTrue(p == returnValue)
