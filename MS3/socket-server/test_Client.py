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
		#p3 = subprocess.call([sys.executable, 'Client.py', '127.0.0.1', '2000', '1', 'input.txt'])

	def tearDown(self):
		del(self.args)
		del(self.server)

########################################################################

	def test_client_too_few_args(self):
		p = subprocess.call([sys.executable, 'Client.py', '127.0.0.1'])
		time.sleep(1)
		self.assertTrue(1 == 2)

	def test_connecting_to_offline_server(self):
		p = subprocess.call([sys.executable, 'Client.py', '127.0.0.80', '2000', '1', 'input.txt'])
		time.sleep(1)
		self.assertTrue(1 == 2)

	def test_client_send_id(self):
		p = subprocess.call([sys.executable, 'Client.py', '127.0.0.1', '2000', '0', 'input.txt'])
		time.sleep(1)
		self.assertTrue(1 == 2)

	def test_client_send_ts(self):
		p = subprocess.call([sys.executable, 'Client.py', '127.0.0.1', '2000', '1', 'input.txt'])
		time.sleep(1)
		self.assertTrue(1 == 2)
