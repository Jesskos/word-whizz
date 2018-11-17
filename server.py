from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def index():
	return "hello world"

@app.route('/play')
def play_game():
	pass

if __name__ == "__main__":
	app.run(debug=True)

