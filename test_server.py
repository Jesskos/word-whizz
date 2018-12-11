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
		self.assertEqual(result.status_code, 200)
		self.assertIn(b"300", result.data)
		self.assertIn(b"joyful", result.data)
		self.assertNotIn(b"crystal", result.data)


	def test_view_leaderboard_route_when_logged_in(self):
		''' Integratin test to test leaderboard route renders correct information when user is logged in, 
		and users from database (example data) are displayed on leaderboard if they have a score '''

		result = self.client.get("/view_leaderboard")
		self.assertIn(b"Leaderboard", result.data)
		self.assertIn(b"awesomewordguesses", result.data)
		self.assertIn(b"500", result.data) 
		self.assertIn(b"alwayswrite", result.data)
		self.assertIn(b"500", result.data) 
		self.assertIn(b"20", result.data)
		self.assertNotIn(b"notinterested", result.data)


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
				sess['user_id'] = 1
				sess['difficulty_level'] = "3"
				sess['name'] = 'teddy'

	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_route_play(self):
		''' tests_route_play to make sure html renders appropriately'''

		# mocking guessed letters
		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['r', 'e'])
		self.users_playing = {1:self.word_game}

		# makes sure guessed letters are  in html
		with patch('server.users_playing', self.users_playing):
			result = self.client.get("/play")
			self.assertIn(b"<span id=3>r</span>", result.data)
			self.assertIn(b"<span id=2>r</span>", result.data)
			self.assertIn(b"<span id=1>e</span>", result.data)
			self.assertIn(b"<span id=0>___</span>", result.data)
			self.assertNotIn(b"<span id=0>b</span>", result.data)


	def test_route_play_after_user_loses(self):
		''' tests_route_play after user loses '''

		# mocking guessed letters
		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['b', 'e'])
		self.word_game.max_incorrect_guesses = 6
		self.word_game.incorrect_guesses = 6
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing',self.users_playing):
			result = self.client.get("/play")
			self.assertEqual(self.word_game.guesses_left(), 0)
			outcome = self.word_game.lose()
			self.assertEqual(outcome, True)
			self.assertIn(b"<span id=0>b</span>", result.data)
			self.assertIn(b"<span id=1>e</span>", result.data)
			self.assertIn(b"<span id=2>r</span>", result.data)
			self.assertIn(b"<span id=3>r</span>", result.data)
			self.assertIn(b"<span id=4>y</span>", result.data)


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
				sess['user_id'] = 1
				sess['difficulty_level'] = "3"
				sess['name'] = 'teddy'

	def tearDown(self):
		''' runs after each test '''

		db.session.close()
		db.drop_all()


	def test_new_difficulty_level(self):
		''' makes sure a thatt when the user selects a new difficulty level, the difficulty level updates '''

		# mocking guessed letters
		self.word_game = Game()
		self.word_game.word = "berry"
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing',self.users_playing):
			result = self.client.get("/play_again", query_string={'difficulty-level': '8'})
			self.assertIn(b'"difficulty_level": "8"', result.data)
			self.assertNotIn(b"3", result.data)


	def test_no_change_difficulty_level(self):
		''' makes sure a that when the user selects no difficulty level, the difficulty level does not update '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.users_playing = {1:self.word_game}
		with patch('server.users_playing', self.users_playing):
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


	def test_invalid_letter_input(self):
		''' tests that when a letter input is invalid, the server reponds correctly'''
		
		self.word_game = Game()
		self.word_game.word = "berry"
		self.users_playing = {1:self.word_game}


		with patch('server.users_playing',self.users_playing):
			result = self.client.get("/check", query_string={'letter': 'a1'})
			self.assertIn(b"invalid input", result.data)


	def test_game_over(self):
		''' tests that the game is over when conditions for game over met'''

		# mocking guessed letters
		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['r', 'e', 'b', 'y'])
		self.word_game.word_set = set(list(self.word_game.word))
		self.users_playing = {1:self.word_game}

		# substitutes server word game with mock word game
		with patch('server.users_playing',self.users_playing):
			result = self.client.get("/check")
			self.assertIn(b"The game is over. Please choose to play again", result.data)
	

	def test_letter_already_guessed(self):
		''' tests for correct response with a letter already guessed'''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['r', 'e', 'b'])
		self.word_game.incorrect_guessed_letters = set(['y'])
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing',self.users_playing):
			result = self.client.get("/check", query_string={'letter': 'Y'})
			self.assertIn(b"You already guessed the letter y", result.data)


	def test_for_win(self):
		''' tests the user wins when entering a letter'''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['e', 'b', 'y'])
		self.word_game.word_set = set(list(self.word_game.word))
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing',self.users_playing):
			result = self.client.get("/check", query_string={'letter': 'r'})
			self.assertIn(b"You win!", result.data)


	def test_for_correct_guess(self):
		''' tests for correct guess where player does not win '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.correct_guessed_letters = set(['e', 'y'])
		self.word_game.word_set = set(list(self.word_game.word))
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing',self.users_playing):
			result = self.client.get("/check", query_string={'letter': 'b'})
			self.assertIn(b"Great Work! Correct Guess!", result.data)


	def test_for_wrong_guess(self):
		''' tests for a wrong guess where player does not lose '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.incorrect_guesses = 2
		self.word_game.max_incorrect_guesses = 6
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing',self.users_playing):
			result = self.client.get("/check", query_string={'letter': 't'})
			self.assertIn(b"Sorry, Incorrect Guess! t is not in the word.", result.data)

	def test_for_lose(self):
		''' tests if user loses after entering a letter '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.incorrect_guesses = 5
		self.word_game.max_incorrect_guesses = 6
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing',self.users_playing):
			result = self.client.get("/check", query_string={'letter': 't'})
			self.assertIn(b"Sorry, you have lost the game.", result.data)

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


	def test_for_game_over(self):
		''' tests for game over '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.incorrect_guesses = 6
		self.word_game.max_incorrect_guesses = 6
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing', self.users_playing):
			result = self.client.get("/check_word", query_string={'word': 'apple'})
			self.assertIn(b'The game is over.', result.data)


	def test_for_word_length(self):
		''' tests that server does not accept word guess that is not equal to secret word '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.incorrect_guesses = 6
		self.word_game.max_incorrect_guesses = 4
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing', self.users_playing):
			result = self.client.get("/check_word", query_string={'word': 'cherry'})
			self.assertIn(b"Invalid entry! make sure your guess is the same length as the secret word", result.data)


	def test_for_only_alpha_input(self):
		'''tests that server only accepts letters '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.incorrect_guesses = 6
		self.word_game.max_incorrect_guesses = 4
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing', self.users_playing):
			result = self.client.get("/check_word", query_string={'word': "b3rry"})
			self.assertIn(b"invalid input", result.data)


	def test_winning_game(self):
		''' tests for correct response when user wins by guessing right word '''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.incorrect_guesses = 6
		self.word_game.max_incorrect_guesses = 5
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing', self.users_playing):
			result = self.client.get("/check_word", query_string={'word': 'berry'})
			self.assertIn(b"You Win! You guessed the word correctly", result.data)
			self.assertIn(b"berry", result.data)

	def test_losing_game(self):
		''' tests for correct response when user loses by guessing wrong word'''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.incorrect_guesses = 5
		self.word_game.max_incorrect_guesses = 6
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing', self.users_playing):
			result = self.client.get("/check_word", query_string={'word': 'ferry'})
			self.assertIn(b"you have lost the game", result.data)
			self.assertIn(b"berry", result.data)


	def test_wrong_word(self):
		''' tests user guessed wrong word but has not lost'''

		self.word_game = Game()
		self.word_game.word = "berry"
		self.word_game.incorrect_guesses = 4
		self.word_game.max_incorrect_guesses = 6
		self.users_playing = {1:self.word_game}

		with patch('server.users_playing', self.users_playing):
			result = self.client.get("/check_word", query_string={'word': 'ferry'})
			self.assertIn(b"Sorry, your guess was incorrect", result.data)


##################################################################################
#############################################################################################################################

def example_data():
	''' creates some example data to test models'''

	player1 = User(username="awesomewordguesses", password="123abc")
	player2 = User(username="bestguesser", password="456def")
	player3 = User(username="alwayswrite", password="789ghi")
	player4 = User(username="notinterested", password="567")
	score1 = Score(user=player1, date=datetime.now(), score=200, word="arduous", won=True, completed=True, 
		game_information='{"word": "arduous", "correct_guessed_letters": ["a"], "incorrect_guessed_letters": ["i"], "incorrect_guesses": 1, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score2 = Score(user=player1, date=datetime.now(), score=300, word="joyful", won=True, completed=True, 
		game_information='{"word": "joyful", "correct_guessed_letters": ["j"], "incorrect_guessed_letters": ["z"], "incorrect_guesses": 1, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score3 = Score(user=player2, date=datetime.now(), score=10, word="tedious", won=False, completed=True, 
		game_information='{"word": "tedious", "correct_guessed_letters": ["t", "e"], "incorrect_guessed_letters": ["s", "a"], "incorrect_guesses": 2, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score4 = Score(user=player2, date=datetime.now(), score=500, word="alacrity", won=True, completed=True, 
		game_information='{"word": "alacrity", "correct_guessed_letters": ["a", "i"], "incorrect_guessed_letters": ["s", "e"], "incorrect_guesses": 2, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score5 = Score(user=player3, date=datetime.now(), score=20, word="crystal", won=False, completed=True, 
		game_information='{"word": "crystal", "correct_guessed_letters": ["c", "a", "l"], "incorrect_guessed_letters": ["i", "e", "o", "p", "w"], "incorrect_guesses": 5, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')
	score6 = Score(user=player3, date=datetime.now(), score=0, word="um", won=False, completed=True, 
		game_information='{"word": "um", "correct_guessed_letters": [], "incorrect_guessed_letters": ["i", "e", "o", "p", "w", "d"], "incorrect_guesses": 6, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}')

	players = [player1, player2, player3, player4]
	scores = [score1, score2, score3, score4, score5]

	db.session.add_all(players[:])
	db.session.add_all(scores[:])
	db.session.commit()


if __name__ == '__main__':  # pragma: no cover

    import unittest
    unittest.main()

