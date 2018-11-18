from unittest import TestCase
from server import *
from game.py import *

class GameTests(TestCase):

	def setUp(self):
		client = server.app.test_client()
		server.app.config['TESTING'] = True
		_mock_check():
			return "chocolate"


	def test_index(self):
		client = server.app.test.client
		self.assertIn("Home Page", result.data)
		self.assertEqual(result.status_code, 200)

	def test_game(self):
		client = server.app.test.client
		self.assertIn("Game", result.data)
		self.assertEqual(result.status_code, 200)


