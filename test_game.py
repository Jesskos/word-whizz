from game import Game
import unittest
from unittest.mock import patch


class GameTests(unittest.TestCase):
	''' unit tests for methods in Game class'''

	TEST_WORD = "chocolate"

	def setUp(self):
		''' sets the attributes in the init method to perform tests
		Attributes set up to test when a player who can neither win nor lose the game '''

		self.word_game=Game()
		self.word_game.word=GameTests.TEST_WORD
		self.word_game.word_set = set(WinningGameTests.TEST_WORD)
		self.word_game.correct_guessed_letters = set(['c', 'o'])
		self.word_game.incorrect_guessed_letters = set(['i', 's'])
		self.word_game.incorrect_guesses = 2 
		self.word_game.max_incorrect_guesses = 6
		self.letters = ['c', 'f', 'g']


	def test_get_word(self):
		''' tests method get_word method '''

		self.assertEqual(self.word_game.get_word(), GameTests.TEST_WORD)
	

	def test_get_word_length(self):
		'''tests method get_word_length '''

		self.assertEqual(self.word_game.get_word_length(), len(GameTests.TEST_WORD))


	def test_check_letter_in_word(self):
		''' tests method check_letter when guessed letter in word '''

		self.assertEqual(self.word_game.check_letter(self.letters[0]), True)
	

	def test_check_letter_not_in_word(self):
		'''tests method check_letter when guessed letter not in word'''

		self.assertEqual(self.word_game.check_letter(self.letters[1]), False)
		self.assertEqual(self.word_game.incorrect_guesses, 3)


	def test_is_already_guessed_letter_for_letter_not_guessed(self):
		''' tests method is_already_guessed_letter for a letter that has not been guessed'''

		self.assertEqual(self.word_game.is_already_guessed_letter(self.letters[2]), False)


	def test_is_already_guessed_letter_for_letter_already_guessed(self):
		''' tests method is_already_guessed_letter for a letter that has been guessed'''
		self.assertEqual(self.word_game.is_already_guessed_letter(self.letters[0]), True)


	def test_guesses_left(self):
		''' tests method guesses_left '''

		self.assertEqual(self.word_game.guesses_left(), 4)


	def test_get_indices_of_letter_in_word(self):
		''' tests method get_indices_of_letter_in_word '''

		self.assertEqual(self.word_game.get_indices_of_letter_in_word(self.letters[0]), [0, 3])


	def test_win_when_no_win_yet(self):
		''' tests method win() when the player has not yet won'''

		self.assertEqual(self.word_game.win(), False)


	def test_lose_when_no_loss_yet(self):
		''' tests method lose() when the player has not lost '''

		self.assertEqual(self.word_game.lose(), False)



	def test_game_over(self):
		''' tests method game_over() when the player has not lost '''

		self.assertEqual(self.word_game.game_over(), False)

class WinningGameTests(unittest.TestCase):
	''' unit tests for methods in Game class'''

	TEST_WORD = "chocolate"

	def setUp(self):
		''' sets the attributes in the init method to perform tests
		Attributes set up to test for a player who can win the game '''

		self.word_game=Game()
		self.word_game.word=WinningGameTests.TEST_WORD
		self.word_game.word_set = set(WinningGameTests.TEST_WORD)
		# set attribute correct_guessed_letters to include all letters in final word to test win() method
		self.word_game.correct_guessed_letters = set(['c', 'o', 'h', 'l', 'a', 't', 'e'])
		self.word_game.incorrect_guessed_letters = set(['i', 's'])
		self.word_game.incorrect_guesses = 2 
		self.word_game.max_incorrect_guesses = 6
		self.letters = ['c', 'f', 'g']


	def test_win_when_player_wins(self):
		''' tests route win() when a player should in the game'''

		self.assertEqual(self.word_game.win(), True)


	def test_lose_when_player_wins(self):
		''' tests method lose() when the player wins '''

		self.assertEqual(self.word_game.lose(), False)


	def test_game_over(self):
		''' tests method game_over() when the player wins, and game is over '''

		self.assertEqual(self.word_game.game_over(), True)


class LosingGameTests(unittest.TestCase):
	''' unit tests for methods in Game class'''


	TEST_WORD = "chocolate"

	def setUp(self):
		''' sets the attributes in the init method to perform tests
		Attributes set up to test for a player who can win the game '''

		self.word_game=Game()
		self.word_game.word=WinningGameTests.TEST_WORD
		self.word_game.word_set = set(WinningGameTests.TEST_WORD)
		self.word_game.correct_guessed_letters = set(['c', 'o'])
		self.word_game.incorrect_guessed_letters = set(['i', 's'])
		self.word_game.incorrect_guesses = 6 
		self.word_game.max_incorrect_guesses = 6
		self.letters = ['c', 'f', 'g']


	def test_win_when_player_loses(self):
		''' tests route win() when player loses '''

		self.assertEqual(self.word_game.win(), False)


	def test_lose_when_player_loses(self):
		''' tests method lose() when the player has lost '''

		self.assertEqual(self.word_game.lose(), True)


	def test_game_over_when_player_loses(self):
		''' tests method game_over() when the player has lost, and game is over'''

		self.assertEqual(self.word_game.game_over(), True)




















if __name__ == '__main__':  # pragma: no cover

    import unittest
    unittest.main()