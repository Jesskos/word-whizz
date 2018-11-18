import unittest
from game import *
import server

class ServerTests(unittest.TestCase):

	def setUp(self):
		self.client = server.app.test_client()
		server.app.config['TESTING'] = True


	def test_index(self):
		result = self.client.get("/")
		self.assertIn(b"Home Page", result.data)
		self.assertEqual(result.status_code, 200)

	def test_game(self):
		result = self.client.get("/play")
		self.assertIn(b"Game", result.data)
		self.assertEqual(result.status_code, 200)
		



if __name__ == '__main__':  # pragma: no cover

    import unittest
    unittest.main()