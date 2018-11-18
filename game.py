word = "chocolate"
word_set = set(word)
correct_guessed_letters = set()
incorrect_guessed_letters = set()
incorrect_guesses = 0 
max_incorrect_guesses = 6 

def get_word():
	''' returns a word to guess'''

	return word

def get_word_length():
	''' gets the length of the word'''

	return len(word)

def check_letter(letter):
	''' checks if the letter is in the word and adjusts the global lists and counters based on the response'''

	print("word is {} letter is {}".format(word, letter))
	global incorrect_guesses
	if letter in word and (letter not in incorrect_guessed_letters or letter not in correct_guessed_letters):
		correct_guessed_letters.add(letter)
		return True
	else:
		incorrect_guessed_letters.add(letter)
		incorrect_guesses += 1 
		return False

def is_already_guessed_letter(letter):
	''' checks whether or not the letter has been previously gussed by the user'''

	if letter in incorrect_guessed_letters or letter in correct_guessed_letters:
		return True 
	else:
		return False

def guesses_left():
	''' returns the remaining guesses''' 
	remaining_guesses = max_incorrect_guesses - incorrect_guesses
	return remaining_guesses

def game_over():
	''' ends the game when the user exceeds allotted guesses'''
	if guesses_left() == 0:
		return True
	if len(word_set - correct_guessed_letters) == 0:
		return True
	else:
		return False

def get_indices_of_letter_in_word(letter):
	indices_of_letter = []
	for idx, char in enumerate(word):
		if char == letter:
			indices_of_letter.append(idx)
	return indices_of_letter



