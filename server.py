from flask import Flask, request, render_template, redirect, jsonify, flash, session
from game import *
import requests
import model

app = Flask(__name__)
word_game = Game()
app.secret_key="Apple"

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/play')
def play():
	''' renders the initial page. If page is refreshed, maintains the original word and game'''

	global word_game
	word = word_game.get_word()
	print(word)
	length_word = word_game.get_word_length()
	remaining_guesses = word_game.guesses_left()

	# if page is refreshed, also need to keep track of incorrect guessed letters and incides of correctly guessed letters
	incorrect_guessed_letters = word_game.incorrect_guessed_letters
	correctly_guessed_letters = word_game.correct_guessed_letters

	# makes a dictioary of the index as key, and the letter as value
	correctly_guessed_dictionary = {}
	for letter in correctly_guessed_letters:
		indices = word_game.get_indices_of_letter_in_word(letter)
		for index in indices:
			correctly_guessed_dictionary[index] = letter


	return render_template("game.html", length=length_word, guesses=remaining_guesses, 
		incorrectly_guessed = incorrect_guessed_letters, correctly_guessed = correctly_guessed_dictionary)


@app.route('/play_again')
def play_again():
	global word_game
	difficulty_level = request.args.get('difficulty-level')
	if difficulty_level:
		word_game = Game(difficulty_level)
	else:
		word_game = Game()
	print("{} is the difficulty_level and word is {}".format(difficulty_level, word_game.get_word()))
	length_word = word_game.get_word_length()
	remaining_guesses = word_game.guesses_left()
	return jsonify({"word_length": length_word, "remaining_guesses":remaining_guesses})


@app.route('/check', methods=['GET'])
def check():
	''' carries out came logic based on instance of Game() class, and responds with appropriate message and information '''

	game_response = {}

	#checks to make sure the game has not already ended
	if word_game.game_over():
		game_response["message"] = "The Game is over. Please choose to play again"
	# if not game over, carries out game logic
	else:
		# receives the chosen letter 
		letter = request.args.get('letter') 
		letter = letter.lower()

		# checks if the letter in the word has already been guessed.
		if word_game.is_already_guessed_letter(letter):
			game_response["message"] = "You already guessed the letter {}".format(letter)

		# if the letter has not been gussed yet, checks whether or not the letter is in the word
		else:
			checked_letter = word_game.check_letter(letter)
			remaining_guesses = word_game.guesses_left()
			indices_of_letter_in_word = word_game.get_indices_of_letter_in_word(letter)

			# if the checked letter is in the word, will include the indices of the checked letter in the word in the response.
			# will also check if the player has completed the word and won when they make the guess
			if checked_letter:
				game_response['indices'] = indices_of_letter_in_word

				#player has won the game after guessing letter
				if word_game.win():
					game_response['message'] = "You win!"
				
				#player correctly guessed letter, but has not yet won
				else:
					game_response["message"] = "Great Work! Correct Guess!"

			# if the checked letter is not in the word, will include the number of remaing guesses in the response
			# will also check if the player has lost the game with the wrong guess, and if so, include the whole word in the response
			else:
				game_response["remaining_guesses"]=remaining_guesses

				# the player guessed an incorrect letter, and lost the game after exceeding incorrect guesses
				if word_game.lose():
					game_response["message"] = "Sorry, you have lost the game."
					game_response["word"] = word_game.get_word()

				# the player guessed an incorrect letter, but still has more tries
				else: 
					game_response["message"] = "Sorry, Incorrect Guess! {} is not in the word. You have {} chances remaining".format(letter, remaining_guesses)

	return jsonify(game_response)






if __name__ == "__main__":
	app.run(debug=True)

