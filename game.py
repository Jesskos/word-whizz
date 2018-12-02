import random
import requests
from datetime import datetime

WORD_URL = "http://app.linkedin-reach.io/words"

class Game:
	''' A class to define and encapsulate the game rules and logic'''

	# a class attribute, which is a dictionary to store words at difficulty levels
	words = {}

	def __init__(self, difficulty_level="1"):
		''' initializes a game with instance attributes below '''

		self.word = Game._make_new_word(difficulty_level=difficulty_level)
		self.difficulty_level = difficulty_level
		self.word_set = set(self.word)
		self.correct_guessed_letters = set()
		self.incorrect_guessed_letters = set()
		self.incorrect_guesses = 0 
		self.max_incorrect_guesses = 6
		self.total_score = 0
		self.incorrect_words_guessed = set()

	def get_word(self):
		''' returns the word '''

		return self.word


	@staticmethod
	def _make_new_word(difficulty_level="1"):
		''' a method to get all the words from API at a specified difficulty level, and pick one at random '''
		
		# Checks if the difficulty level key is already in the dictionary
		if difficulty_level not in Game.words:
			print("Calling API to get words")
			payload = {"difficulty": difficulty_level}

			# Calls API to get words at a certain difficulty level
			r = requests.get(WORD_URL, params=payload)

			# Makes a list of words
			new_words = r.text.split("\n")

			# adds words to class variable dictionary, with difficulty_level as key and list of words as value
			Game.words[difficulty_level] = new_words

		# If diffiuclty level key is already in dictionary, a second API call can be avoid
		else:
			print("Not calling API because words is not empty.")

		# returns a random word from the list corresponding to the difficulty level key
		return random.choice(Game.words[difficulty_level])


	def get_word_length(self):
		''' gets the length of the word'''

		return len(self.word)


	def check_letter(self,letter):
		''' checks if the letter is in the word, and keeps track of letters guessed correctly, letters guessed incorrectly, and number of incorrect guesses '''

		if letter in self.word and (letter not in self.incorrect_guessed_letters or letter not in self.correct_guessed_letters):
			self.correct_guessed_letters.add(letter)
			return True
		else:
			self.incorrect_guessed_letters.add(letter)
			self.incorrect_guesses += 1 
			return False


	def is_already_guessed_letter(self,letter):
		''' checks whether or not the letter has been previously gussed by the user '''

		if letter in self.incorrect_guessed_letters or letter in self.correct_guessed_letters:
			return True 
		return False


	def guesses_left(self):
		''' returns the number remaining guesses''' 

		remaining_guesses = self.max_incorrect_guesses - self.incorrect_guesses
		return remaining_guesses


	def get_incorrectly_guessed_letters(self):
		''' gets the set of incorrectly guessed letters '''

		return self.incorrect_guessed_letters


	def get_correct_guessed_letters(self):
		''' gets the set of correctly guessed letters '''

		return self.correct_guessed_letters


	def get_incorrect_guessed_letters(self):
		''' gets the set of incorrectly guessed letters '''

		return self.incorrect_guessed_letters


	def get_incorrectly_guessed_words(self):
		''' returns the set of incorrectly guessed words'''

		return self.incorrect_words_guessed  


	def already_guessed_word(self, word):
		''' checks if word has already been gussed'''

		if word in self.incorrect_words_guessed:
			return True
		return False

		
	def lose(self):
		''' ends the game when the user exceeds allotted guesses'''

		if self.guesses_left() == 0:
			return True
		return False


	def get_indices_of_letter_in_word(self, letter):
		''' gets the index or indices of the a letter in a word ''' 

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


	def check_word(self, guessed_word):
		if guessed_word == self.word:
			self.correct_guessed_letters = set(list(self.word))
			return True
		else:
			self.incorrect_words_guessed.add(guessed_word)
			self.incorrect_guesses += 1


	def game_over(self):
		''' checks if the game is over '''

		if self.win() or self.lose():
			return True
		return False


	def get_score(self):
		''' gets the score at the end of the game'''

		base_score = 10
		point_gains = len(self.correct_guessed_letters) * 10
		point_losses = self.incorrect_guesses * 1 + len(self.incorrect_words_guessed)
		total_points = (base_score + point_gains - point_losses) * int(self.difficulty_level)

		if self.game_over():
			self.total_score = total_points

		return self.total_score




	
		 







