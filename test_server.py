import unittest
from game import *
from server import app, db, connect_to_db, session
import flask
from model import User, Score
from unittest.mock import patch
#############################################################################################################################

class ServerTestsLoggedIn(unittest.TestCase):
	''' A series of tests that tests all routes that require a user to be logged in '''

	def setUp(self):
		''' runs before each test '''

		# test_client simulates that the server is running
		# app defined inside server
		# tells flask that we are testing
		app.config['TESTING'] = True

		# gets the flask test client
		self.client = app.test_client()

		# connects to a test database
		connect_to_db(app, "postgresql:///testdb")

		# creates tables with sample data
		db.create_all()
		example_data()

		# a mock for session
		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1
				sess['difficulty_level'] = "1"
				sess['name'] = 'teddy'
				sess['game_id'] = 3


	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_index_route_when_logged_in(self):
		''' integration test to test home page renders correct information when user is logged in '''

		result = self.client.get("/", follow_redirects=True)
		self.assertIn(b"Play Word Game", result.data)
		self.assertEqual(result.status_code, 200)


	def test_game_route_when_logged_in(self):
		''' Integratin test to test play route renders correct infomation when user is logged in '''

		result = self.client.get("/play")
		self.assertIn(b"Play Word Game", result.data)
		self.assertEqual(result.status_code, 200)


	def test_view_history_route_when_logged_in(self):
		''' Integratin test to test that history route renders correct information when user is logged in, 
		and users scores and words are displayed on history '''

		result = self.client.get("/view_history")
		self.assertIn(b"Game History", result.data)
		self.assertIn(b"success", result.data)
		self.assertNotIn(b"resilience", result.data)
		self.assertNotIn(b"um", result.data)	
		self.assertIn(b"150", result.data)	


	def test_view_leaderboard_route_when_logged_in(self):
		''' Integratin test to test leaderboard route renders correct information when user is logged in, 
		and users from database (example data) are displayed on leaderboard if they have a score '''

		result = self.client.get("/view_leaderboard")
		self.assertIn(b"Leaderboard", result.data)
		self.assertEqual(result.status_code, 200)
		self.assertIn(b"200", result.data)
		self.assertIn(b"150", result.data)
		
	def test_log_out_when_logged_in(self):
		''' tests log out functionality ''' 
		
		result = self.client.get("/logout", follow_redirects=True)
		self.assertIn(b"Sign Up/Log In Page", result.data)
		self.assertIn(b"You have now logged out", result.data)

		self.assertEqual(result.status_code, 200)

	def test_rules(self):
		''' tests rules'''

		result = self.client.get("/game_rules")
		self.assertIn(b"Guidelines", result.data)


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
	

	def test_view_game_rules(self):
		''' Integratin test to make sure rules does not render unless user is logged in'''

		result = self.client.get("/game_rules", follow_redirects=True)
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



class ServerTestsPlay(unittest.TestCase):
	''' A series of tests to make sure that when page renders, letter locations on board are maintained '''

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
		# user = User.query.filter_by(username='awesomewordguesses').first()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 2
				sess['game_id'] = 4
				sess['difficulty_level'] = "3"
				sess['name'] = 'teddy'

	# def tearDown(self):
	# 	''' runs after each test '''

	# 	db.session.close()
	# 	db.drop_all()


	def test_route_play(self):
		''' tests_route_play to make sure html renders appropriately'''

		result = self.client.get("/play")
		self.assertIn(b"<span id=0>t</span>", result.data)
		self.assertIn(b"<span id=1>e</span>", result.data)
		self.assertIn(b"<span id=2>___</span>", result.data)


class ServerTestsPlayWhenLose(unittest.TestCase):
	''' A series of tests to make sure that when page renders, letter locations on board are maintained '''

	
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
		# user = User.query.filter_by(username='awesomewordguesses').first()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 3
				sess['game_id'] = 7
				sess['difficulty_level'] = "3"
				sess['name'] = 'teddy'

	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_play_after_losing_game(self):
		result = self.client.get("/play")
		self.assertIn(b"<span id=0>u</span>", result.data)
		self.assertIn(b"<span id=1>m</span>", result.data)


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

		#'mocking' session id
		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 2
				sess['difficulty_level'] = "3"
				sess['name'] = 'teddy'
				sess['game_id'] = 3

	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_new_difficulty_level(self):
		''' makes sure a thatt when the user selects a new difficulty level, the difficulty level updates '''

		result = self.client.get("/play_again", query_string={'difficulty-level': '8'})
		self.assertIn(b'"difficulty_level": "8"', result.data)
		self.assertNotIn(b"3", result.data)


	def test_no_change_difficulty_level(self):
		''' makes sure a that when the user selects no difficulty level, the difficulty level does not update '''

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

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1
				sess["game_id"] = 1
				sess['difficulty_level'] = "3"
				sess['name'] ="teddy"


	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_invalid_letter_input(self):
		''' tests that when a letter input is invalid, the server reponds correctly'''
		
		result = self.client.get("/check", query_string={'letter': 'a1'})
		self.assertIn(b"invalid input", result.data)


	def test_letter_already_guessed(self):
		''' tests for correct response with a letter already guessed'''

		result = self.client.get("/check", query_string={'letter': 'I'})
		self.assertIn(b"You already guessed the letter i", result.data)


	def test_for_correct_guess(self):
		''' tests for correct guess where player does not win '''

		result = self.client.get("/check", query_string={'letter': 'u'})
		self.assertIn(b"Great Work! Correct Guess!", result.data)


	def test_for_wrong_guess(self):
		''' tests for a wrong guess where player does not lose '''

		result = self.client.get("/check", query_string={'letter': 'e'})
		self.assertIn(b"Sorry, Incorrect Guess! e is not in the word.", result.data)


class testWinningGame(unittest.TestCase):
	''' tests winning game when user guesses a correct letter or correct word '''

	def setUp(self):
		''' runs before each test '''

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True
		self.client = app.test_client()
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()
		example_data()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 5
				sess["game_id"] = 8
				sess['difficulty_level'] = "3"
				sess['name'] ="teddy"


	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_for_win_check_letter_letter(self):
		''' tests the user wins when entering a letter'''

		result = self.client.get("/check", query_string={'letter': 'i'})
		self.assertIn(b"You win!", result.data)


	def test_for_win_check_word(self):
		''' tests the user wins when entering a correct word'''

		result = self.client.get("/check_word", query_string={'word': 'GRIT'})
		self.assertIn(b"You Win!", result.data)


class testGameOver(unittest.TestCase):
	''' tests game over response when user has already won or lost in routes check[_letter] and check_word '''

	def setUp(self):
		''' runs before each test '''

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True
		self.client = app.test_client()
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()
		example_data()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 4
				sess["game_id"] = 7
				sess['difficulty_level'] = "3"
				sess['name'] ="teddy"


	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_for_game_over_in_check(self):
		''' tests for game over after a losing game '''

		result = self.client.get("/check", query_string={'letter': 'i'})
		self.assertIn(b"The game is over", result.data)


	def test_for_game_over_in_check_word(self):
		''' tests for game over after a losing game '''

		result = self.client.get("/check_word", query_string={'word': 'over'})
		self.assertIn(b"The game is over", result.data)


class testLosingGame(unittest.TestCase):
	''' tests losing game when user guesses a wrong letter or wrong word  '''

	def setUp(self):
		''' runs before each test '''

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True
		self.client = app.test_client()
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()
		example_data()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1
				sess["game_id"] = 2
				sess['difficulty_level'] = "3"
				sess['name'] ="teddy"


	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_for_loss_check_letter(self):
		''' tests the user loses when entering a wrong letter after 5 guesses '''

		result = self.client.get("/check", query_string={'letter': 'm'})
		self.assertIn(b"Sorry, you have lost the game.", result.data)


	def test_for_loss_check_word(self):
		''' tests the user loses when entering a wrong word after 5 guesses '''

		result = self.client.get("/check_word", query_string={'word': 'jellys'})
		self.assertIn(b"Sorry, you have lost the game", result.data)


class testCheckWord(unittest.TestCase):
	''' tests functionality of check_word '''

	def setUp(self):
		''' runs before each test '''

		# test_client simulates that the server is running
		# app defined inside server
		app.config['TESTING'] = True
		self.client = app.test_client()
		connect_to_db(app, "postgresql:///testdb")
		db.create_all()
		example_data()

		with self.client as c:
			with c.session_transaction() as sess:
				sess['user_id'] = 1
				sess['game_id'] = 1
				sess['difficulty_level'] = "3"
				sess['name'] = "teddy"


	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_for_only_alpha_input(self):
		'''tests that server only accepts letters '''


		result = self.client.get("/check_word", query_string={'word': "b3rries"})
		self.assertIn(b"invalid input", result.data)


	def test_wrong_word(self):
		''' tests user guessed wrong word but has not lost'''

		result = self.client.get("/check_word", query_string={'word': 'arduino'})
		self.assertIn(b"Sorry, your guess was incorrect", result.data)


	def test_wrong_length(self):
		''' tests length was incorrect '''

		result = self.client.get("/check_word", query_string={'word': 'ardent'})
		self.assertIn(b"make sure your guess is the same length as the secret word", result.data)


	def test_word_already_guessed(self):
		''' tests length was incorrect '''

		result = self.client.get("/check_word", query_string={'word': 'ambient'})
		self.assertIn(b"word already guessed", result.data)

##################################################################################
#############################################################################################################################

def example_data():
	''' creates some example data to test models'''

	# sample game players
	player1 = User(username="awesomewordguesses", password="123abc")
	player2 = User(username="bestguesser", password="456def")
	player3 = User(username="alwayswrite", password="789ghi")
	player4 = User(username="notinterested", password="567")
	player5 = User(username="notgivingup", password="words")

	# sample games 
	score1 = Score(user=player1, date=datetime.now(), score=0, word="arduous", won=True, completed=False, 
		game_information='{"word": "arduous", "correct_guessed_letters": ["a"], "incorrect_guessed_letters": ["i"], "incorrect_guesses": 1, "max_incorrect_guesses": 6, "incorrect_words_guessed": ["ambient"]}')
	score2 = Score(user=player1, date=datetime.now(), score=0, word="joyful", won=False, completed=False, 
		game_information='{"word": "joyful", "correct_guessed_letters": ["j"], "incorrect_guessed_letters": ["z", "e", "i", "p", "s"], "incorrect_guesses": 5, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score3 = Score(user=player1, date=datetime.now(), score=150, word="success", won=True, completed=True, 
		game_information='{"word": "success", "correct_guessed_letters": ["s", "u", "c", "e"], "incorrect_guessed_letters": ["a"], "incorrect_guesses": 1, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score4 = Score(user=player2, date=datetime.now(), score=0, word="tedious", won=False, completed=False, 
		game_information='{"word": "tedious", "correct_guessed_letters": ["t", "e"], "incorrect_guessed_letters": ["s", "a"], "incorrect_guesses": 2, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score5 = Score(user=player2, date=datetime.now(), score=0, word="alacrity", won=False, completed=False, 
		game_information='{"word": "alacrity", "correct_guessed_letters": ["a", "i"], "incorrect_guessed_letters": ["s", "e"], "incorrect_guesses": 2, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score6 = Score(user=player3, date=datetime.now(), score=0, word="crystal", won=False, completed=False, 
		game_information='{"word": "crystal", "correct_guessed_letters": ["c", "a", "l"], "incorrect_guessed_letters": ["i", "e", "o", "p", "w"], "incorrect_guesses": 5, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score7 = Score(user=player3, date=datetime.now(), score=0, word="um", won=False, completed=True, 
		game_information='{"word": "um", "correct_guessed_letters": [], "incorrect_guessed_letters": ["i", "e", "o", "p", "w", "d"], "incorrect_guesses": 6, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score8 = Score(user=player5, date=datetime.now(), score=0, word="grit", won=False, completed=False, 
		game_information='{"word": "grit", "correct_guessed_letters": ["g", "r", "t"], "incorrect_guessed_letters": ["e"], "incorrect_guesses": 1, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score9 = Score(user=player5, date=datetime.now(), score=200, word="", won=True, completed=True, 
		game_information='{"word": "resilience", "correct_guessed_letters": ["r", "e", "s", "i", "l", "n", "c"], "incorrect_guessed_letters": ["w", "z", "y", "m"], "incorrect_guesses": 4, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	

	players = [player1, player2, player3, player4, player5]
	scores = [score1, score2, score3, score4, score5, score6, score7, score8, score9]

	db.session.add_all(players)
	db.session.add_all(scores)
	db.session.commit()


if __name__ == '__main__':  # pragma: no cover

    import unittest
    unittest.main()

