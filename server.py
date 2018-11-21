from flask import Flask, request, render_template, redirect, jsonify, flash, session
from game import Game
import requests
from model import connect_to_db, db, User, Score
from datetime import datetime
from sqlalchemy.sql import label
from sqlalchemy import func, desc


app = Flask(__name__)
word_game = Game()
app.secret_key="w()r|)gvu&&"

@app.route('/')
def index():
	if "user_id" in session:
		return redirect("/play")

	return render_template('index.html')

@app.route('/login', methods=['POST'])
def log_in():
	''' allows a user to login '''

	print(request.form)
	request_info = request.form.to_dict()
	entered_username = request_info['InputUsername']
	entered_password = request_info['InputPassword']
	existing_user = User.query.filter(User.username==entered_username).first()
	if not existing_user:
		flash("Username does not exist. Please sign up or check your spelling")
		return redirect("/")
	else:
		if existing_user.password == entered_password:
			session["user_id"] = existing_user.user_id
			session["name"] = existing_user.username
			flash("you have successfully logged in")
			return redirect("/play")
		else:
			flash("Password Incorrect. Please try again")
			return redirect("/")




@app.route('/signup', methods=['POST'])
def sign_up():
	''' allows a user to signup '''

	new_username = request.form["SignUpInputEmail"]
	new_password = request.form["SignUpPassword"]
	confirm_password = request.form["ConfirmInputPassword"]
	
	print("new password {} new_username {}".format(new_password, new_username))

	existing_user = User.query.filter_by(username=new_username).first()

	if new_password == confirm_password and not existing_user:
		new_user = User(username = new_username, password=new_password, total_score=0)
		db.session.add(new_user)
		db.session.commit()
		session["user_id"] = new_user.user_id
		return redirect("/play")

	elif new_password != confirm_password:
		flash("Passwords do not match")
		return redirect("/")

	else:
		flash("User Already Exists. Please create a new username")
		return redirect("/")


@app.route('/logout')
def log_out():
	''' logs a user out of the portal'''

	if "user_id" in session:
		del session["user_id"]
		flash("You have now logged out")
		return redirect("/")


@app.route('/play')
def play():
	''' renders the initial page. If page is refreshed, maintains the original word and game'''

	if "user_id" not in session:
		return redirect("/")

	# temporarily keeping difficulty level in this route to initialize until login is set up
	session["difficulty_level"] = "3"
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

	print("word is {} and difficulty_level is {})".format(word, word_game.difficulty_level))

	return render_template("game.html", length=length_word, guesses=remaining_guesses, 
		incorrectly_guessed = incorrect_guessed_letters, correctly_guessed = correctly_guessed_dictionary, 
		difficulty_level=session["difficulty_level"], name=session["name"])


@app.route('/play_again')
def play_again():

	global word_game
	new_difficulty_level = request.args.get('difficulty-level')
	if new_difficulty_level:
		word_game = Game(new_difficulty_level)
		session['difficulty_level'] = new_difficulty_level
	else:
		word_game = Game(session["difficulty_level"])
	print("{} is the new difficulty_level and word is {} and difficulty is {}".format(new_difficulty_level, word_game.get_word(), session['difficulty_level']))
	length_word = word_game.get_word_length()
	remaining_guesses = word_game.guesses_left()
	return jsonify({"word_length": length_word, "remaining_guesses":remaining_guesses, "difficulty_level": session['difficulty_level']})


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
					save_game = Score(date=datetime.now(), user_id=int(session['user_id']), word=word_game.get_word(), score=word_game.get_score(), 
						won=word_game.win())
					db.session.add(save_game)
					db.session.commit()
				
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
					save_game = Score(date=datetime.now(), user_id=int(session['user_id']), word=word_game.get_word(), score=word_game.get_score(), 
						won=word_game.win())					
					db.session.add(save_game)
					db.session.commit()

				# the player guessed an incorrect letter, but still has more tries
				else: 
					game_response["message"] = "Sorry, Incorrect Guess! {} is not in the word. You have {} chances remaining".format(letter, remaining_guesses)

	return jsonify(game_response)


@app.route('/view_leaderboard')
def view_leaderboard():
	''' renders the template for the leaderboard'''

	if "user_id" not in session:
		return redirect("/")

	results = db.session.query(Score.user_id,label('total_score', func.sum(Score.score))).group_by(Score.user_id).order_by(desc('total_score')).all()
	for result in results:
		username = User.query.filter(User.user_id==result[0]).first().username
		result.append(username)

	return render_template('leaderboard.html', name=session["name"])


@app.route('/view_history')
def view_game_history():

	if "user_id" not in session:
		return redirect("/")

	games_history_for_user = Score.query.filter(Score.user_id==session["user_id"]).all()

	for i in games_history_for_user:
		print(i)

	return render_template('history.html', game_history=games_history_for_user, name=session["name"])






if __name__ == "__main__":
	connect_to_db(app) 
	app.run(debug=True)

