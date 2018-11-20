import random
import requests

WORD_URL = "http://app.linkedin-reach.io/words"

class Game:
	''' A class to define the game rules and logic'''

	words = []

	def __init__(self):

		self.word = Game.make_new_word()
		self.word_set = set(self.word)
		self.correct_guessed_letters = set()
		self.incorrect_guessed_letters = set()
		self.incorrect_guesses = 0 
		self.max_incorrect_guesses = 6

	def get_word(self):
		''' returns a word to guess'''

		return self.word

	@staticmethod
	def make_new_word():
		''' a temporary method to get all the words from API at a certain difficulty level, and pick one at random'''
		if not Game.words:
			print("Calling API to get words")
			payload = {"difficulty": "5"}
			r = requests.get(WORD_URL, params=payload)
			new_words = r.text.split("\n")
			Game.words = new_words
		else:
			print("Not calling API because words is not empty.")
		return random.choice(Game.words)


	def get_word_length(self):
		''' gets the length of the word'''

		return len(self.word)

	def check_letter(self,letter):
		''' checks if the letter is in the word and adjusts the global lists and counters based on the response'''

		print("word is {} letter is {}".format(self.word, letter))
		if letter in self.word and (letter not in self.incorrect_guessed_letters or letter not in self.correct_guessed_letters):
			self.correct_guessed_letters.add(letter)
			return True
		else:
			self.incorrect_guessed_letters.add(letter)
			self.incorrect_guesses += 1 
			return False

	def is_already_guessed_letter(self,letter):
		''' checks whether or not the letter has been previously gussed by the user'''

		if letter in self.incorrect_guessed_letters or letter in self.correct_guessed_letters:
			return True 
		return False

	def guesses_left(self):
		''' returns the remaining guesses''' 

		remaining_guesses = self.max_incorrect_guesses - self.incorrect_guesses
		return remaining_guesses

	def lose(self):
		''' ends the game when the user exceeds allotted guesses'''
		if self.guesses_left() == 0:
			return True
		return False

	def get_indices_of_letter_in_word(self, letter):
		''' gets the indices of the chosen letter in a word ''' 
		indices_of_letter = []
		for idx, char in enumerate(self.word):
			if char == letter:
				indices_of_letter.append(idx)
		return indices_of_letter


	def win(self):
		''' checks if player has won the game '''
		if len(self.word_set - self.correct_guessed_letters) == 0:
			return True
		return False

	def game_over(self):
		''' checks to make sure the game is over so that the user does not play again with the same word'''
		if self.win() or self.lose():
			return True
		return False







