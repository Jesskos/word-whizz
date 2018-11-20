import unittest
from game import *
import server

class ServerTests(unittest.TestCase):

	def setUp(self):
		self.client = server.app.test_client()
		server.app.config['TESTING'] = True


	def test_index_route(self):
		''' integration test to make sure home page renders correct information '''

		result = self.client.get("/")
		self.assertIn(b"Home Page", result.data)
		self.assertEqual(result.status_code, 200)


	def test_game_route(self):
		''' Integratin test to make sure game route renders correct infomration '''

		result = self.client.get("/play")
		self.assertIn(b"Game", result.data)
		self.assertEqual(result.status_code, 200)


	def test_check_letter_not_present(self):
		''' Integratin test to make sure game route renders correct inofmration '''


	def test_check_letter_not_present(self):
		''' Integratin test to make sure game route renders correct inofmration '''


if __name__ == '__main__':  # pragma: no cover

    import unittest
    unittest.main()