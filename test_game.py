from game import Game
import unittest
from unittest.mock import patch
import requests


class GameTestProperties(unittest.TestCase):
	''' tests that game properties are instantiated correctly '''

	def test_create_game(self):
		''' tests difficulty level defaults to 1 if no arguments '''
		g = Game()
		self.assertEqual(g.difficulty_level, "1")

	def test_create_game_argument(self):
		''' tests difficulty level takes the diffiuclty level assigned in argument '''
		g = Game("3")
		self.assertEqual(g.difficulty_level, "3")


class GameTestsWhilePlaying(unittest.TestCase):
	''' unit tests for methods in Game class for a user who makes a guess that neither causes a win nor loss '''


	def setUp(self):
		''' sets the attributes in the init method to perform tests
		Attributes set up to test the condition of neither winning or losing the game'''

		self.word_game=Game(word="chocolate", correct_guessed_letters = set(['c', 'o']), incorrect_guessed_letters = set(['i', 's']),
		  incorrect_guesses = 2, incorrect_words_guessed = set(["berry"]))

		self.letters = ['c', 'f', 'g']


	def test_get_word(self):
		''' tests method get_word method '''

		self.assertEqual(self.word_game.get_word(), self.word_game.word)
	

	def test_get_word_length(self):
		'''tests method get_word_length '''

		self.assertEqual(self.word_game.get_word_length(), len(self.word_game.word))


	def test_check_letter_in_word(self):
		''' tests method check_letter when the guessed letter is in word '''

		self.assertEqual(self.word_game.check_letter(self.letters[0]), True)
	

	def test_check_letter_not_in_word(self):
		'''tests method check_letter when the guessed letter is not in word'''

		self.assertEqual(self.word_game.check_letter(self.letters[1]), False)
		self.assertEqual(self.word_game.incorrect_guesses, 3)

	def test_get_incorrectly_guessed_words(self):
		''' tests that incorrectly guessed words are stored'''

		self.assertEqual(self.word_game.get_incorrectly_guessed_words(), set(["berry"]))


	def test_is_already_guessed_letter_for_letter_not_guessed(self):
		''' tests method is_already_guessed_letter for a letter that has not been guessed'''

		self.assertEqual(self.word_game.is_already_guessed_letter(self.letters[2]), False)


	def test_is_already_guessed_letter_for_letter_already_guessed(self):
		''' tests method is_already_guessed_letter for a letter that has been guessed'''

		self.assertEqual(self.word_game.is_already_guessed_letter(self.letters[0]), True)


	def test_is_already_guessed_word_for_word_already_guessed(self):
		''' tests method already_guessed_word for a word which is already guessed '''

		self.assertEqual(self.word_game.already_guessed_word('berry'), True)


	def test_is_already_guessed_word_for_word_not_already_guessed(self):
		''' tests method already_guessed_word for a word which has not already guessed '''

		self.assertEqual(self.word_game.already_guessed_word('cherry'), False)


	def test_get_correct_guessed_letters(self):
		''' tests that the set of correctly guessed letters is returned '''

		self.assertEqual(self.word_game.get_correct_guessed_letters(), set(['c', 'o']))


	def test_get_incorrect_guessed_letters(self):
		''' tests that the set of incorrectly guessed letters is returned '''

		self.assertEqual(self.word_game.get_incorrectly_guessed_letters(), set(['i', 's']))


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


	def test_check_word_when_word_incorrect(self):
		''' checks a word when the word is not the correct word '''

		self.word_game.check_word("cherry")
		self.assertEqual(self.word_game.incorrect_guesses, 3)
		self.assertIn("cherry", self.word_game.incorrect_words_guessed)


class WinningGameTests(unittest.TestCase):
	''' unit tests for methods in Game class when a user has won'''


	def setUp(self):
		''' sets the attributes in the init method to perform tests
		Attributes set up to test the condition when a user wins the game'''

		self.word_game=Game(word="chocolate", correct_guessed_letters = set(['c', 'o', 'h', 'l', 'a', 't', 'e']), difficulty_level = '2',
			incorrect_guessed_letters = set(['i', 's']), incorrect_guesses=2, max_incorrect_guesses=6)
		# set attribute correct_guessed_letters to include all letters in final word to test win() method

		self.letters = ['c', 'f', 'g']


	def test_win_when_player_wins(self):
		''' tests method win() when a player wins the game'''

		self.assertEqual(self.word_game.win(), True)


	def test_lose_when_player_wins(self):
		''' tests method lose() when the player wins '''

		self.assertEqual(self.word_game.lose(), False)


	def test_game_over(self):
		''' tests method game_over() when the player wins, and game is over '''

		self.assertEqual(self.word_game.game_over(), True)


	def test_get_score(self):
		''' tests functionality of get_score method '''

		self.assertEqual(self.word_game.get_score(), 156)


	def test_check_word_when_word_correct(self):
		''' checks a word when the word is the correct word '''

		self.assertEqual(self.word_game.check_word("chocolate"), True)


class LosingGameTests(unittest.TestCase):
	''' unit tests for methods in Game class when a user has lost'''


	def setUp(self):
		''' sets the attributes in the init method to perform tests
		Attributes set up to test the condition when a user loses the game'''

		self.word_game=Game(word="chocolate", difficulty_level=2, correct_guessed_letters=set(['c', 'o']), incorrect_guessed_letters= set(['i', 's', 'd', 'f', 'g', 'z']),
		incorrect_guesses = 6, max_incorrect_guesses=6)
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


	def test_get_score(self):
		''' tests functionality of score method '''

		self.assertEqual(self.word_game.get_score(), 48)


class StringifyAttributes(unittest.TestCase):
	''' tests method stringify attributes '''

	def setUp(self):
		''' sets the attributes in the init method to perform tests
		Attributes set up to test the condition when a user loses the game'''

		self.word_game=Game(word="chocolate", difficulty_level=2, correct_guessed_letters=set(['c']), incorrect_guessed_letters= set(['i']),
		incorrect_guesses = 6, max_incorrect_guesses=6)

	def test_stringify_attributes(self):
		''' tests method stringify_attributes'''

		attributes_str = '{"word": "chocolate", "correct_guessed_letters": ["c"], "incorrect_guessed_letters": ["i"], "incorrect_guesses": 6, "max_incorrect_guesses": 6, "incorrect_words_guessed": []}'
		self.assertEqual(attributes_str, self.word_game.stringify_attributes())

class ApiGameTest(unittest.TestCase):
	''' test functionality of API, and finding words of appropriate difficulty_level'''


	def setUp(self):
		''' sets the attributes in the init method to perform tests
		Attributes set up to mock difficulty level '''


		words = {}
		self.word_game = Game()
		self.word_game.difficulty_level = "5"
		self.word_game.word = self.word_game._make_new_word(difficulty_level=self.word_game.difficulty_level)


	def test_API(self):
		''' test that the API returns a response '''

		result = requests.get("http://app.linkedin-reach.io/words")
		self.assertEqual(result.status_code, 200)


	def test_word_at_difficulty_level(self):
		''' test that the API is creating a new word at the specified difficulty_level '''

		payload = {"difficulty": self.word_game.difficulty_level}
		response = requests.get("http://app.linkedin-reach.io/words", params=payload)

		self.assertIn(self.word_game.word, response.text)







		


















if __name__ == '__main__':  # pragma: no cover

    import unittest
    unittest.main()