import unittest
from game import *
from server import app, db, connect_to_db

class ServerTestsLoggedIn(unittest.TestCase):
	''' Test the routes when the user is logged in'''

	def setUp(self):

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True
		self.client = app.test_client()
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()


		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1
				sess['difficulty_level'] = "3"


	def tearDown(self):
		db.session.remove()
		db.drop_all()


	def test_index_route_when_logged_in(self):
		''' integration test to make sure home page renders correct information '''

		result = self.client.get("/", follow_redirects=True)
		self.assertIn(b"Play Word Game", result.data)
		self.assertEqual(result.status_code, 200)


	def test_game_route_when_logged_in(self):
		''' Integratin test to make sure game route renders correct infomation '''

		result = self.client.get("/play")
		self.assertIn(b"Play Word Game", result.data)
		self.assertEqual(result.status_code, 200)


	def test_view_history_route_when_logged_in(self):
		''' Integratin test to make sure game route renders correct information '''

		result = self.client.get("/view_history")
		self.assertIn(b"Game History", result.data)
		self.assertEqual(result.status_code, 200)


	def test_view_leaderboard_route_when_logged_in(self):
		''' Integratin test to make sure game route renders correct information '''

		result = self.client.get("/view_leaderboard")
		self.assertIn(b"Leaderboard", result.data)
		self.assertEqual(result.status_code, 200)




class ServerTestsNotLoggedIn(unittest.TestCase):
	''' Test the routes when the user is not logged in '''

	def setUp(self):

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True
		self.client = app.test_client()
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()


	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_index_route(self):
		''' integration test to make sure home page renders correct information '''

	def test_index_route(self):
		''' integration test to make sure home page renders correct information '''
		result = self.client.get("/")
		self.assertIn(b"Sign Up/Log In Page", result.data)
		self.assertEqual(result.status_code, 200)


	def test_game_route(self):
		''' Integratin test to make sure game route renders correct infomation '''

		result = self.client.get("/play", follow_redirects=True)
		self.assertIn(b"Home Page", result.data)
		self.assertEqual(result.status_code, 200)


	def test_view_history_route(self):
		''' Integratin test to make sure game route renders correct information '''

		result = self.client.get("/view_history", follow_redirects=True)
		self.assertIn(b"Home Page", result.data)
		self.assertEqual(result.status_code, 200)


	def test_view_leaderboard_route(self):
		''' Integratin test to make sure game route renders correct information '''

		result = self.client.get("/view_leaderboard", follow_redirects=True)
		self.assertIn(b"Home Page", result.data)
		self.assertEqual(result.status_code, 200)


if __name__ == '__main__':  # pragma: no cover

    import unittest
    unittest.main()

