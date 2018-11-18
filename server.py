from flask import Flask, request, render_template, jsonify
from game import *

app = Flask(__name__)

@app.route('/')
def index():

	return render_template('index.html')

@app.route('/play')
def play_game():
	word = get_word()
	length_word = get_word_length()
	return render_template("game.html", length = length_word)


@app.route('/check', methods=['GET'])
def check():
	if game_over():
		return jsonify({"message": "Game Over!"})
	print(f"\n\nRequest: GET {request.url}\n\n")
	letter = request.args.get('letter') 
	print(letter)
	print("{} is the letter".format(letter))
	if is_already_guessed_letter(letter):
		return jsonify({"message": "You already guessed the letter {}".format(letter)})
	else:
		checked_letter = check_letter(letter)
		guesses_remaining = guesses_left()
		indices_of_letter_in_word = get_indices_of_letter_in_word(letter)
		if checked_letter:
			return jsonify({"message": "Great Work! Correct Guess!", 
				"indices": indices_of_letter_in_word})
		else:
			return jsonify({"message": "Sorry, Incorrect Guess! {} is not in the word. You have {} chances remaining".
				format(letter, guesses_remaining)})






if __name__ == "__main__":
	app.run(debug=True)

