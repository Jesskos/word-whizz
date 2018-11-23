import unittest
from game import *
from server import app, db, connect_to_db
from model import User, Score

#############################################################################################################################

class ServerTestsLoggedIn(unittest.TestCase):
	''' A series of tests that tests all routes when a user is logged in, and a session added '''

	def setUp(self):
		''' runs before each test '''

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True

		# gets the flask test client
		self.client = app.test_client()

		# connects to a test database
		connect_to_db(app, "postgresql:///testdb")

		# creates tables with sample data
		db.create_all()
		example_data()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1
				sess['difficulty_level'] = "3"
				sess['name'] = "name"


	def tearDown(self):
		''' runs after each test '''
		db.session.remove()
		db.drop_all()


	def test_index_route_when_logged_in(self):
		''' integration test to make sure home page renders correct information when user is logged in '''

		result = self.client.get("/", follow_redirects=True)
		self.assertIn(b"Play Word Game", result.data)
		self.assertEqual(result.status_code, 200)


	def test_game_route_when_logged_in(self):
		''' Integratin test to make sure play route renders correct infomation when user is logged in '''

		result = self.client.get("/play")
		self.assertIn(b"Play Word Game", result.data)
		self.assertEqual(result.status_code, 200)


	def test_view_history_route_when_logged_in(self):
		''' Integratin test to make sure history route renders correct information when user is logged in '''

		result = self.client.get("/view_history")
		self.assertIn(b"Game History", result.data)
		self.assertEqual(result.status_code, 200)


	def test_view_leaderboard_route_when_logged_in(self):
		''' Integratin test to make sure leaderboard route renders correct information when user is logged in '''

		result = self.client.get("/view_leaderboard")
		self.assertIn(b"Leaderboard", result.data)


	def test_log_out_when_logged_in(self):
		''' tests to make sure a logged in user is logged out ''' 
		result = self.client.get("/logout", follow_redirects=True)
		self.assertIn(b"Sign Up/Log In Page", result.data)
		self.assertEqual(result.status_code, 200)



class ServerTestsNotLoggedIn(unittest.TestCase):
	''' A series of tests to test same routes as above, except when user is not logged in, 
	and tests conditions when a user can be logged in or sign up '''

	def setUp(self):
		''' runs before each test '''

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True
		self.client = app.test_client()
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()
		example_data()


	def tearDown(self):
		''' runs after each test '''

		db.session.remove()
		db.drop_all()


	def test_index_route(self):
		''' integration test to make sure home page renders correct information when user is not logged in'''
		result = self.client.get("/")
		self.assertIn(b"Sign Up/Log In Page", result.data)
		self.assertEqual(result.status_code, 200)


	def test_game_route(self):
		''' Integration test to make sure the play route renders correct information when user is not logged in'''

		result = self.client.get("/play", follow_redirects=True)
		self.assertIn(b"Sign Up/Log In Page", result.data)
		self.assertEqual(result.status_code, 200)


	def test_view_history_route(self):
		''' Integratin test to make sure view_history route renders correct information when user is not logged in'''

		result = self.client.get("/view_history", follow_redirects=True)
		self.assertIn(b"Sign Up/Log In Page", result.data)
		self.assertEqual(result.status_code, 200)


	def test_view_leaderboard_route(self):
		''' Integratin test to make sure leadboard route renders correct information when user is not logged in'''

		result = self.client.get("/view_leaderboard", follow_redirects=True)
		self.assertIn(b"Sign Up/Log In Page", result.data)
		self.assertEqual(result.status_code, 200)


	def test_signing_up(self):
		''' Integration test to test that a user who is not logged in can signup with a new username and matching password and confirm password'''

		result = self.client.post("/signup", data={'SignUpInputEmail': 'CoolNewPlayer',
													'SignUpPassword': 'abc', 
													'ConfirmInputPassword': 'abc'}, 
													follow_redirects=True)
		self.assertIn(b"Play Word Game", result.data)
		self.assertEqual(result.status_code, 200)


	def test_signing_up_when_passwords_dont_match(self):
		''' Integration test to test that a user who is not logged in cannot signup when passwords do not match'''

		result = self.client.post("/signup", data={'SignUpInputEmail': 'CoolNewPlayer',
													'SignUpPassword': 'abc', 
													'ConfirmInputPassword': 'abd'}, 
													follow_redirects=True)
		self.assertIn(b"Passwords do not match", result.data)
		self.assertEqual(result.status_code, 200)


	def test_signing_up_when_username_taken(self):
		''' Integration test to test that a user who is not logged in cannot take a username that is already taken'''

		result = self.client.post("/signup", data={'SignUpInputEmail': "bestguesser",
													'SignUpPassword': 'abc', 
													'ConfirmInputPassword': 'abc'}, 
													follow_redirects=True)
		self.assertIn(b"User Already Exists.", result.data)
		self.assertEqual(result.status_code, 200)


	def test_logging_in_with_matching_password(self):
		''' Integration test to test that a user can log in with correct user_id and password'''

		result = self.client.post("/login", data={'InputUsername': "bestguesser",
													'InputPassword': '456def'}, 
													follow_redirects=True)
		self.assertIn(b"Play Word Game", result.data)
		self.assertEqual(result.status_code, 200)


	def test_logging_in_with_wrong_password(self):
		''' Integration test to test that a user cannot log in with incorrect password'''

		result = self.client.post("/login", data={'InputUsername': "bestguesser",
													'InputPassword': '456def'}, 
													follow_redirects=True)
		self.assertIn(b"Play Word Game", result.data)
		self.assertEqual(result.status_code, 200)


	def test_logging_in_with_non_existing_user_id(self):
		''' Integration test to test that a user cannot log in if username does not exist'''

		result = self.client.post("/login", data={'InputUsername': "coolguesser",
													'InputPassword': '456def'}, 
													follow_redirects=True)
		self.assertIn(b"Username does not exist.", result.data)
		self.assertEqual(result.status_code, 200)



class ServerTestsLeaderBoard(unittest.TestCase):
	''' A series of tests to test leaderboard and gamehistory routes and functionality '''

	






#############################################################################################################################

def example_data():
	''' creates some example data to test models'''

	player1 = User(username="awesomewordguesses", password="123abc")
	player2 = User(username="bestguesser", password="456def")
	player3 = User(username="alwayswrite", password="789ghi")
	player4 = User(username="notinterested", password="567")
	score1 = Score(user_id=player1, date=datetime.now(), score=200, word="arduous", won=True)
	score2 = Score(user_id=player1, date=datetime.now(), score=300, word="joyful", won=True)
	score3 = Score(user_id=player2, date=datetime.now(), score=10, word="tedious", won=False)
	score4 = Score(user_id=player2, date=datetime.now(), score=500, word="alacrity", won=True)
	score5 = Score(user_id=player3, date=datetime.now(), score=350, word="crystal", won=True)

	db.session.add_all([player1, player2, player3, player4])
	db.session.commit()


if __name__ == '__main__':  # pragma: no cover

    import unittest
    unittest.main()

