from flask import Flask, request, render_template, redirect, jsonify, flash, session
from game import *
import requests

app = Flask(__name__)
word_game = Game()
app.secret_key="Apple"

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/play')
def play_game():
	global word_game
	word_game = Game()
	length_word = word_game.get_word_length()
	remaining_guesses = word_game.guesses_left()
	return render_template("game.html", length=length_word, guesses=remaining_guesses)


@app.route('/check', methods=['GET'])
def check():
	''' carries out came logic based on instance of Game() class '''

	if word_game.game_over():
		return jsonify({"message":"The Game is over. Please choose to play again"})
	letter = request.args.get('letter') 
	if word_game.is_already_guessed_letter(letter):
		return jsonify({"message": "You already guessed the letter {}".format(letter)})
	else:
		checked_letter = word_game.check_letter(letter)
		remaining_guesses = word_game.guesses_left()
		indices_of_letter_in_word = word_game.get_indices_of_letter_in_word(letter)
		if checked_letter:
			if word_game.win():
				return jsonify({"message": "You win!", 
					"indices": indices_of_letter_in_word})
			return jsonify({"message": "Great Work! Correct Guess!", 
				"indices": indices_of_letter_in_word})
		else:
			if word_game.lose():
				return jsonify({"message":"Sorry, you have lost the game.", 
					"remaining_guesses": remaining_guesses, 
					"word": word_game.get_word()})

			return jsonify({"message": "Sorry, Incorrect Guess! {} is not in the word. You have {} chances remaining".
				format(letter, remaining_guesses), 
				"remaining_guesses": remaining_guesses})






if __name__ == "__main__":
	app.run(debug=True)

