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
	# Receiving information from form to log user into the game. 
	#request.form returns an immutable MultiDict(). Used this method to convert.

	request_info = request.form.to_dict()
	entered_username = request_info['InputUsername']
	entered_password = request_info['InputPassword']
	existing_user = User.query.filter(User.username==entered_username).first()

	# checks to make sure user exists before logging in
	if not existing_user:
		flash("Username does not exist. Please sign up or check your spelling")
		return redirect("/")

	# if user exists, checks to make .ure entered password matches corresponding password in database
	# if so, logs user into the game. If they don't match, user is told to try again
	# A new game object is instantiated when user logs in
	else:
		if existing_user.password == entered_password:
			session["user_id"] = existing_user.user_id
			session["name"] = existing_user.username

			#creates a session with a default difficulty level
			# in the future, the user will be able to choose a default difficulty level when registering/signing up and change it in his/her profile
			global word_game
			session["difficulty_level"] = "3"
			word_game = Game(session["difficulty_level"])

			flash("you have successfully logged in")
			return redirect("/play")
		else:
			flash("Password Incorrect. Please try again")
			return redirect("/")


@app.route('/signup', methods=['POST'])
def sign_up():
	''' allows a user to signup '''

	# getting information from forms to sign up user to play game
	new_username = request.form["SignUpInputEmail"]
	new_password = request.form["SignUpPassword"]
	confirm_password = request.form["ConfirmInputPassword"]
	
	print("new password {} new_username {}".format(new_password, new_username))

	# checks if user is already existing user to prevent duplicate usernames
	existing_user = User.query.filter_by(username=new_username).first()

	# makes sure passwords are the same, and the selected username has not already been taken
	# In the future, I plan to use password encryption, validation, and set passwprd limits to increase security
	# A new game object is intantiated when user is confirmed and signs in
	if new_password == confirm_password and not existing_user:
		new_user = User(username = new_username, password=new_password)
		db.session.add(new_user)
		db.session.commit()

		# adds user information directly to session, and instantiates a new word game which is added to session. 
		session["user_id"] = new_user.user_id
		session["name"] = new_user.username

		#creates a session with a default difficulty level
		# in the future, the user will be able to choose a default difficulty level when registering/signing up and change it in his/her profile
		global word_game
		session["difficulty_level"] = "3"
		word_game = Game(session["difficulty_level"])

		word_game = Game()
		return redirect("/play")

	# checks to make sure passwords match
	elif new_password != confirm_password:
		flash("Passwords do not match")
		return redirect("/")

	# if user already exists, triggered to create a new account
	else:
		flash("User Already Exists. Please create a new username")
		return redirect("/")


@app.route('/logout')
def log_out():
	''' logs a user out of the portal'''

	# removes user_id from session, along with the word_game so it is not repeated for other users
	if "user_id" in session:
		del session["user_id"]
		del session["name"]
		del session["difficulty_level"]
		flash("You have now logged out")
		return redirect("/")


@app.route('/play')
def play():
	''' renders the initial page. Session maintains word. If page is refreshed, maintains the original word and game'''

	# if user is not logged in, redirectsback to homepage
	if "user_id" not in session:
		return redirect("/")

	#gets global variable wordgame
	global word_game
	word = word_game.get_word()
	
	# gets length of word, incorrect_guessed_letters, length_of_word, and remaining_guesses for templating
	# when page is refreshed, game will maintain where it left off
	incorrect_guessed_letters = word_game.incorrect_guessed_letters
	correctly_guessed_letters = word_game.correct_guessed_letters
	length_word = word_game.get_word_length()
	remaining_guesses = word_game.guesses_left()

	# makes a dictioary of the index as key, and the letter as values so that if the page is refreshed, letter location on board is maintained
	correctly_guessed_dictionary = {}
	for letter in correctly_guessed_letters:
		indices = word_game.get_indices_of_letter_in_word(letter)
		for index in indices:
			correctly_guessed_dictionary[index] = letter

	print("word is {} and difficulty_level is {}".format(word, word_game.difficulty_level))

	# sends over variables to be used for initial Jinja templating
	return render_template("game.html", length=length_word, guesses=remaining_guesses, 
		incorrectly_guessed = incorrect_guessed_letters, correctly_guessed = correctly_guessed_dictionary, 
		difficulty_level=session["difficulty_level"], name=session["name"])


@app.route('/play_again')
def play_again():
	''' a route that responds to an AJAX call from the browser to refresh the word '''

	# gets the global variable word_game 
	global word_game

	# checks if user changed the difficulty level
	new_difficulty_level = request.args.get('difficulty-level')

	# if the user changed the difficulty level, instantiates a new game with the new difficutly level as an argument
	if new_difficulty_level:
		session['difficulty_level'] = new_difficulty_level
		word_game = Game(new_difficulty_level)

	# if the user does not choose a new difficulty level, instantiates a new game with the current difficulty level from session as an argument
	else:
		word_game = Game(session["difficulty_level"])

	print("{} is the new difficulty_level and word is {} and difficulty is {}".format(new_difficulty_level, word_game.get_word(), session['difficulty_level']))

	# gets the length of the word and remaining guesses to send to browser to modify DOM for new word
	length_word = word_game.get_word_length()
	remaining_guesses = word_game.guesses_left()

	return jsonify({"word_length": length_word, "remaining_guesses":remaining_guesses, "difficulty_level": session['difficulty_level']})


@app.route('/check', methods=['GET'])
def check():
	''' carries out came logic based on instance of Game() class, and responds with appropriate message and information '''

	game_response = {}

	#checks to make sure the game has not already ended
	if word_game.game_over():
		game_response["message"] = "The game is over. Please choose to play again"
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
					game_response["score"] = word_game.get_score()
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
					game_response["score"] = word_game.get_score()
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

	#redirects to homepage if user not logged in
	if "user_id" not in session:
		return redirect("/")

	# queries the database for sum, user_Id, and username, performing a join on the users and scores table,
	# grouping by score sum by user_id
	sql = """SELECT SUM(score), scores.user_id, username 
			FROM scores JOIN users USING (user_id)
			GROUP BY scores.user_id, username 
			ORDER BY SUM(score) DESC
			"""
			

	cursor = db.session.execute(sql)
	game_leaders = cursor.fetchall()


	return render_template('leaderboard.html', name=session["name"], leaders=game_leaders)


@app.route('/view_history')
def view_game_history():

	if "user_id" not in session:
		return redirect("/")

	# queries the database for the word, score, and whether or not the user won in the 
	sql = """SELECT word, won, score, date
			FROM scores 
			WHERE user_id= :user_id
			ORDER BY date DESC
			"""

	user_id = session["user_id"]
	cursor = db.session.execute(sql, {"user_id": user_id})
	game_record = cursor.fetchall()

	scores = []
	for game in game_record:
		scores.append(game.score)
	sum_scores = sum(scores)


	return render_template('history.html', game_history=game_record, name=session["name"], scores_total=sum_scores)






if __name__ == "__main__":
	connect_to_db(app) 
	app.run(debug=True)

