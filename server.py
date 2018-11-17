from flask import Flask, request, render_template
from game import *

app = Flask(__name__)

@app.route('/')
def index():

	return render_template('index.html')

@app.route('/play')
def play_game():
	word = get_word()
	return render_template("game.html", word = word)

if __name__ == "__main__":
	app.run(debug=True)

