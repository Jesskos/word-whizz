from flask import Flask, request, render_template
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


@app.route('/check')
def check():
	letter = request.args.get('letter-input') 
	print("{} is the letter".format(letter))
	if is_already_guessed_letter(letter):
		return "You already guessed this letter"
	else:
		checked_letter = check_letter(letter)
		guesses_remaining = guesses_left()
		if checked_letter:
			return "Great Work! Correct Guess!"
		else:
			return "Sorry, Incorrect Guess! You have {} chances remaining".format(guesses_remaining)





if __name__ == "__main__":
	app.run(debug=True)

