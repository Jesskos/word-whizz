import unittest
from game import *
from server import app, db, connect_to_db, session
from model import User, Score
from unittest.mock import patch
#############################################################################################################################

class ServerTestsLoggedIn(unittest.TestCase):
	''' A series of tests that tests all routes that require a user to be logged in '''

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

		# adds a  user to the session from example_data to carry out routes that require log in
		user = User.query.filter_by(username='awesomewordguesses').first()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = user.user_id
				sess['difficulty_level'] = "3"
				sess['name'] = user.username


	def tearDown(self):
		''' runs after each test '''

		db.session.close()
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
		''' Integratin test to make sure history route renders correct information when user is logged in, 
		and users scores and words are displayed on history '''

		result = self.client.get("/view_history")
		self.assertIn(b"Game History", result.data)
		self.assertEqual(result.status_code, 200)
		self.assertIn(b"300", result.data)
		self.assertIn(b"joyful", result.data)
		self.assertNotIn(b"crystal", result.data)


	def test_view_leaderboard_route_when_logged_in(self):
		''' Integratin test to make sure leaderboard route renders correct information when user is logged in, 
		and users from database are displayed on leaderboard if they have a score '''

		result = self.client.get("/view_leaderboard")
		self.assertIn(b"Leaderboard", result.data)
		self.assertIn(b"awesomewordguesses", result.data)
		self.assertIn(b"500", result.data) 
		self.assertIn(b"alwayswrite", result.data)
		self.assertIn(b"500", result.data) 
		self.assertIn(b"20", result.data)
		self.assertNotIn(b"notinterested", result.data)


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

		db.session.close()
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
													'InputPassword': '456de'}, 
													follow_redirects=True)
		self.assertIn(b"Sign Up/Log In Page", result.data)
		self.assertEqual(result.status_code, 200)


	def test_logging_in_with_non_existing_user_id(self):
		''' Integration test to test that a user cannot log in if username does not exist'''

		result = self.client.post("/login", data={'InputUsername': "coolguesser",
													'InputPassword': '456def'}, 
													follow_redirects=True)
		self.assertIn(b"Username does not exist.", result.data)
		self.assertEqual(result.status_code, 200)



class ServerTestsPageRefresh(unittest.TestCase):
	''' A series of tests to make sure that when page refreshes, letter locations on board are maintained '''

	def setUp(self):
		''' runs before each test '''

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True
		self.client = app.test_client()
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()
		example_data()
		


		# adds a user to the session to carry out routes while logged in
		user = User.query.filter_by(username='awesomewordguesses').first()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = user.user_id
				sess['difficulty_level'] = "3"
				sess['name'] = user.username

	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_route_play(self):
		''' '''

		# mocking guessed letters
		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['r', 'e'])

		# makes sure guessed letters are  in html
		with patch('server.word_game',self.word_game):
			result = self.client.get("/play")
			self.assertIn(b"<span id=3>r</span>", result.data)
			self.assertIn(b"<span id=2>r</span>", result.data)
			self.assertIn(b"<span id=1>e</span>", result.data)
			self.assertIn(b"<span id=0>___</span>", result.data)
			self.assertNotIn(b"<span id=0>b</span>", result.data)



class ServerTestsDifficultyLevel(unittest.TestCase):
	''' A series of tests that tests that difficulty_level is changed '''

	def setUp(self):
		''' runs before each test '''

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True
		self.client = app.test_client()
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()
		example_data()
		

		# adds a user to the session to carry out routes while logged in
		user = User.query.filter_by(username='awesomewordguesses').first()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = user.user_id
				sess['difficulty_level'] = "3"
				sess['name'] = user.username

	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_new_difficulty_level(self):
		''' makes sure a thatt when the user selects a new difficulty level, the difficulty level updates '''

		# mocking guessed letters
		self.word_game = Game()
		self.word_game.word = "berry"

		with patch('server.word_game',self.word_game):
			result = self.client.get("/play_again", query_string={'difficulty-level': '8'})
			self.assertIn(b'"difficulty_level": "8"', result.data)
			self.assertNotIn(b"3", result.data)


	def test_no_change_difficulty_level(self):
		''' makes sure a thatt when the user selects no difficulty level, the difficulty level does not update '''

		result = self.client.get("/play_again", query_string={'difficulty-level': ''})
		self.assertIn(b'"difficulty_level": "3"', result.data)
		self.assertNotIn(b'"difficulty_level": "8"', result.data)



class ServerTestsCheckGameLogic(unittest.TestCase):
	''' A series of tests that tests that test the game logic through the route check '''


	def setUp(self):
		''' runs before each test '''

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True
		self.client = app.test_client()
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()
		example_data()
		
		# adds a user to the session to carry out routes while logged in
		user = User.query.filter_by(username='awesomewordguesses').first()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = user.user_id
				sess['difficulty_level'] = "3"
				sess['name'] = user.username


	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_game_over(self):
		''' tests that the game is over '''

		# mocking guessed letters
		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['r', 'e', 'b', 'y'])
		self.word_game.word_set = set(list(self.word_game.word))

		# substitutes server word game with mock word game
		with patch('server.word_game',self.word_game):
			result = self.client.get("/check")
			self.assertIn(b"The game is over. Please choose to play again", result.data)
	

	def test_letter_already_guessed(self):
		''' tests if the letter is already guessed '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['r', 'e', 'b'])
		self.word_game.incorrect_guessed_letters = set(['y'])

		with patch('server.word_game',self.word_game):
			result = self.client.get("/check", query_string={'letter': 'Y'})
			self.assertIn(b"You already guessed the letter y", result.data)


	def test_for_win(self):
		''' tests if the user wins when entering a letter'''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['e', 'b', 'y'])
		self.word_game.word_set = set(list(self.word_game.word))

		with patch('server.word_game',self.word_game):
			result = self.client.get("/check", query_string={'letter': 'r'})
			self.assertIn(b"You win!", result.data)


	def test_for_correct_guess(self):
		''' tests for correct guess where player does not win '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['e', 'y'])
		self.word_game.word_set = set(list(self.word_game.word))

		with patch('server.word_game',self.word_game):
			result = self.client.get("/check", query_string={'letter': 'b'})
			self.assertIn(b"Great Work! Correct Guess!", result.data)


	def test_for_wrong_guess(self):
		''' tests for a wrong guess where player does not lose '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.incorrect_guesses = 2
		self.word_game.max_incorrect_guesses = 6

		with patch('server.word_game',self.word_game):
			result = self.client.get("/check", query_string={'letter': 't'})
			self.assertIn(b"Sorry, Incorrect Guess! t is not in the word.", result.data)

	def test_for_lose(self):
		''' tests if user loses after entering a letter '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.incorrect_guesses = 5
		self.word_game.max_incorrect_guesses = 6

		with patch('server.word_game',self.word_game):
			result = self.client.get("/check", query_string={'letter': 't'})
			self.assertIn(b"Sorry, you have lost the game.", result.data)


#############################################################################################################################

def example_data():
	''' creates some example data to test models'''

	player1 = User(username="awesomewordguesses", password="123abc")
	player2 = User(username="bestguesser", password="456def")
	player3 = User(username="alwayswrite", password="789ghi")
	player4 = User(username="notinterested", password="567")
	score1 = Score(user=player1, date=datetime.now(), score=200, word="arduous", won=True)
	score2 = Score(user=player1, date=datetime.now(), score=300, word="joyful", won=True)
	score3 = Score(user=player2, date=datetime.now(), score=10, word="tedious", won=False)
	score4 = Score(user=player2, date=datetime.now(), score=500, word="alacrity", won=True)
	score5 = Score(user=player3, date=datetime.now(), score=20, word="crystal", won=False)

	players = [player1, player2, player3, player4]
	scores = [score1, score2, score3, score4, score5]

	db.session.add_all(players[:])
	db.session.add_all(scores[:])
	db.session.commit()


if __name__ == '__main__':  # pragma: no cover

    import unittest
    unittest.main()

