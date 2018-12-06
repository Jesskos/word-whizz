from flask import Flask, request, render_template, redirect, jsonify, flash, session
from game import Game
import requests
from model import connect_to_db, db, User, Score
from datetime import datetime

# create an instance of the flask application.__name__ is unique file
app = Flask(__name__)

# creates a dictionary of users playing as the key value and the current word that user is trying to solve as the value
users_playing = {}

# secret key for encrypting sessions
app.secret_key="w()r|)gvu&&"

@app.route('/')
def index():
	# prevents a user who is logged in from viewing index route
	if "user_id" in session:
		return redirect("/play")

	# renders index page
	return render_template('index.html')

@app.route('/login', methods=['POST'])
def log_in():
	''' allows a user to login to play the game by checking login credentials '''

	# Receiving request from browser with form information
	# with more time, I would spend more time on form validation to prevent security threats
	# request.form returns an immutable MultiDict(). Used form.to_dict() to convert MultiDict() to dictionary
	request_info = request.form.to_dict()
	entered_username = request_info['InputUsername']
	entered_password = request_info['InputPassword']
	existing_user = User.query.filter(User.username==entered_username).first()

	# checks to make sure user exists in database
	if not existing_user:
		flash("Username does not exist. Please sign up or check your spelling")
		return redirect("/")

	# if user exists, checks password, to make sure it matches password found in database 
	# if so, logs user into the game. 
	else:
		if existing_user.password == entered_password:
			session["user_id"] = existing_user.user_id
			session["name"] = existing_user.username

			# creates a session with a default difficulty level of '1', and instantiates a new game
			# in the future, I would like the user to be able to choose a difficulty level when registering/signing up and change it in his/her profile
			# global word_game
			global users_playing
			session["difficulty_level"] = "1"
			users_playing[session["user_id"]] = Game(session["difficulty_level"])

			# when user logs in, flashes a message that they have successfully logged in (see html templating)
			flash("you have successfully logged in")
			return redirect("/play")

		# if passwords do not match, user is redirected home, and flashed a message to try again
		else:
			flash("Password Incorrect. Please try again")
			return redirect("/")


@app.route('/signup', methods=['POST'])
def sign_up():
	''' allows a user to signup and adds new users to the database'''

	# Receiving request from forms with username and password
	# With more time, I would spend more time on form validation to prevent security risks
	new_username = request.form["SignUpInputEmail"].lower()
	new_password = request.form["SignUpPassword"]
	confirm_password = request.form["ConfirmInputPassword"]

	# checks if user is already an existing user to prevent duplicate usernames before adding name to database
	existing_user = User.query.filter_by(username=new_username).first()

	# Checks if password matches confirmatory password
	# If password matches confirmatory password and user is not an existing user, the new user is saved to the db so that they can log in.
	# In the future, I plan to use password encryption, validation, and set password requirements to increase security
	if new_password == confirm_password and not existing_user:
		new_user = User(username = new_username, password=new_password)
		db.session.add(new_user)
		db.session.commit()

		# adds user information directly to session, and instantiates a new word game which is added to session. 
		session["user_id"] = new_user.user_id
		session["name"] = new_user.username

		# Creates a session with a default difficulty level of '1'
		# In the future, the user will be able to choose a difficulty level when registering/signing up and change it in their profile
		# A new game object is instantiated when sign up process is completed, and added to the dictionary users_playing
		global users_playing
		session["difficulty_level"] = "1"
		users_playing[session["user_id"]] = Game(session["difficulty_level"])


		# User is forwarded to play game
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
	''' logs a user out of the game, and ends session'''

	# Removes user_id, name, and difficulty level from the session to log out user, and redirects back to index
		# del users_playing[session["user_id"]]

	if session['user_id'] in users_playing:
		del users_playing[session["user_id"]]
	del session["user_id"]
	del session["name"]
	del session["difficulty_level"]
	flash("You have now logged out")
	return redirect("/")


@app.route('/play')
def play():
	''' renders the game page using templating without changing the word '''

	# if user is not logged in, redirectsback to homepage
	if "user_id" not in session:
		return redirect("/")

	# gets global variable users_playing, and finds the user's word based on the session user_id
	# word_game = users_playing[session["user_id"]]
	try:
		word_game = users_playing[session["user_id"]]
	except:
		word_game = Game()
		users_playing[session["user_id"]] = word_game

	secret_word = word_game.get_word()
	
	# Gets the length of word, incorrect_guessed_letters, length_of_word, and remaining_guesses using class methods or attributes
	# When the page is refreshed, game will pick up where it left off
	incorrect_guessed_letters = word_game.get_incorrectly_guessed_letters()
	incorrectly_guessed_words = word_game.get_incorrectly_guessed_words()
	correctly_guessed_letters = word_game.get_correct_guessed_letters()
	length_word = word_game.get_word_length()
	remaining_guesses = word_game.guesses_left()

	# A dictionary to store correctly guessed letters and their indices
	correctly_guessed_dictionary = {}

	# Adds letter index as key, and the letter as value to correctly_guessed_dictionary. If page is refreshed, letter location is maintained. 
	# If the game is lost, will go into else condition to make a dictionary with all letter indices to reveal entire word to user
	if not word_game.lose():
		for letter in correctly_guessed_letters:
			indices = word_game.get_indices_of_letter_in_word(letter)
			for index in indices:
				correctly_guessed_dictionary[index] = letter

	else:
		for letter_idx in range(len(secret_word)):
			correctly_guessed_dictionary[letter_idx] = secret_word[letter_idx]

	print("word is {} and difficulty_level is {}".format(secret_word, word_game.difficulty_level))

	# Renders variables using Jinja2 templating
	return render_template("game.html", length=length_word, guesses=remaining_guesses, 
		incorrectly_guessed = incorrect_guessed_letters, words_incorrectly_guessed=incorrectly_guessed_words,
		correctly_guessed = correctly_guessed_dictionary, 
		difficulty_level=session["difficulty_level"], name=session["name"])


@app.route('/play_again')
def play_again():
	''' a route that responds to an AJAX call from the browser to refresh the word '''

	# Using the global users_playing dictionary, gets the current word
	global users_playing
	
	# Checks if user changed the difficulty level. Returns None if the user has not changed the difficutly level.
	new_difficulty_level = request.args.get('difficulty-level')

	# If the user changed the difficulty level, instantiates a new game with the new difficutly level as an argument.
	# finds the user in the dictionary using the key user_id from the session, and replaces it with the new word
	if new_difficulty_level:
		session['difficulty_level'] = new_difficulty_level
		word_game = Game(new_difficulty_level)
		users_playing[session["user_id"]] = word_game

	# If the user has not changed the difficulty level, instantiates a new game with the current difficulty level from session passed as an argument
	# finds the user in the dictionary using the key user_id from the session, and replaces it with the new word
	else:
		word_game = Game(session["difficulty_level"])
		users_playing[session["user_id"]] = word_game

	print("{} is the new difficulty_level and word is {} and difficulty is {}".format(new_difficulty_level, word_game.get_word(), session['difficulty_level']))

	# Gets the length of the word and remaining guesses to send to browser to modify DOM for new word
	length_word = word_game.get_word_length()
	remaining_guesses = word_game.guesses_left()

	return jsonify({"word_length": length_word, "remaining_guesses":remaining_guesses, "difficulty_level": session['difficulty_level']})


@app.route('/check', methods=['GET'])
def check():
	''' carries out game logic, and responds with appropriate message and information to AJAX calls from the browser '''

	# An empty dictinary to be converted into JSON 
	game_response = {}

	# gets the current word the user is playing from the users_playing dictionary
	global users_playing
	word_game = users_playing[session["user_id"]]
	print("session id is {} for user {} and the word is {}".format(session["user_id"], session["name"], word_game.get_word()))

	# Checks to make sure the game has not already ended
	if word_game.game_over():
		game_response["message"] = "The game is over. Please choose to play again"
		game_response["score"] = word_game.get_score()

	# If the game has not already ended, carries out game logic
	else:

		# Receives the request with the letter from the browser
		letter = request.args.get('letter') 
		letter = letter.lower()

		# extra backend validation to make sure the letter is actually a letter, and is one character in length
		if len(letter) != 1 or not letter.isalpha():
			game_response["message"] = "invalid input"
			return jsonify(game_response)

		# Checks if the letter in the word has already been guessed.
		if word_game.is_already_guessed_letter(letter):
			game_response["message"] = "You already guessed the letter {}".format(letter)
			game_response["remaining_guesses"] = word_game.guesses_left()

		# If the letter has not been gussed yet, checks whether or not the letter is in the word
		else:
			letter_in_word = word_game.check_letter(letter)
			remaining_guesses = word_game.guesses_left()
			indices_of_letter_in_word = word_game.get_indices_of_letter_in_word(letter)

			# Adds the letter and remaining guesses to JSON response
			game_response['letter'] = letter
			game_response["remaining_guesses"]=remaining_guesses

			# Enters this condition if the checked_letter is in the word
			if letter_in_word:

				# If the checked letter is in the word, index/indices of the checked letter in the word are included in the response.
				game_response['indices'] = indices_of_letter_in_word

				# Checks if player has won the game after guessing a letter
				if word_game.win():

					# Adds a message and final score to the response
					game_response['message'] = "You win!"
					game_response["score"] = word_game.get_score()

					# Saves the game to the database along with the corresponding user_id, word score, and whether or not they won
					save_game = Score(date=datetime.now(), user_id=int(session['user_id']), word=word_game.get_word(), score=word_game.get_score(), 
						won=word_game.win())
					db.session.add(save_game)
					db.session.commit()
				
				# If the player has not won, they correctly guesses the letter. A message to inform them they guessed the correct letter is included in the response.
				else:
					game_response["message"] = "Great Work! Correct Guess!"

			# Enter this condition since the letter_in_word was False
			else:

				# Enter this condition if player runs out of remaining guesses, and loses
				if word_game.lose():

					# Adds a message, score, and entire word to response when player loses
					game_response["message"] = "Sorry, you have lost the game."
					game_response["secret_word"] = word_game.get_word()
					game_response["score"] = word_game.get_score()

					# saves the game to the database
					save_game = Score(date=datetime.now(), user_id=int(session['user_id']), word=word_game.get_word(), score=word_game.get_score(), 
						won=word_game.win())					
					db.session.add(save_game)
					db.session.commit()

				# Enter this condition if player still has remaining guesses, and can continue playing
				else: 
					game_response["message"] = "Sorry, Incorrect Guess! {} is not in the word. You have {} chances remaining".format(letter, remaining_guesses)

	# Sends a response to the browser
	return jsonify(game_response)


@app.route('/check_word')
def check_word():
	''' checks if user guessed the word '''

	# gets the word that the user is currently playing based on the session_id
	global users_playing
	word_game = users_playing[session["user_id"]]

	# an empty dictionary to be sent to the server as a JSON object
	game_response = {}

	# receives the guessed word from a request, and makes it lowecase
	guessed_word = request.args.get('word').lower()

	# Checks to make sure the game has not already ended before carrying out logic
	if word_game.game_over():
		game_response["message"] = "The game is over. Please choose to play again"
		game_response["score"] = word_game.get_score()
		return jsonify(game_response)

	# checks to make sure entered word is the same length as secret word
	elif word_game.get_word_length() != len(guessed_word):
		game_response["message"] = "Invalid entry! make sure your guess is the same length as the secret word"
		game_response["remaining_guesses"] = word_game.guesses_left()
		return jsonify(game_response)

	# extra step to verify that input is all letters (also done in html)
	elif not guessed_word.isalpha():
		game_response["message"] = "invalid input"
		return jsonify(game_response)

	elif word_game.already_guessed_word(guessed_word):
		game_response["message"] = "word already guessed"
		return jsonify(game_response)

	# number of remaining guesses left
	guessed_correctly = word_game.check_word(guessed_word)

	# Gets remainig guesses, which is to be sent in response to all conditions below
	game_response["remaining_guesses"] = word_game.guesses_left()

	# checks if the user guessed the correct word. If so, sends a message and the full word
	if guessed_correctly:
		game_response["message"] = "You Win! You guessed the word correctly"
		game_response["secret_word"] = word_game.get_word()

	else:
		# adds guessed_word to the response to be sent
		game_response["guessed_word"] = guessed_word

		# checks if user lost the game
		if word_game.lose():
			game_response["message"] = "{} is not the word. Sorry, you have lost the game".format(guessed_word)
			game_response["secret_word"] = word_game.get_word()
		
		# if the user has not lost the game, lets them know they guessed incorrectly
		else:
			game_response["message"] = "Sorry, your guess was incorrect. {} is not the word".format(guessed_word)
			
	# saves word game 
	if word_game.win() or word_game.lose():
		save_game = Score(date=datetime.now(), user_id=int(session['user_id']), word=word_game.get_word(), score=word_game.get_score(), won=word_game.win())					
		db.session.add(save_game)
		db.session.commit()
		game_response["score"] = word_game.get_score()

	return jsonify(game_response)


@app.route('/view_leaderboard')
def view_leaderboard():
	''' renders the template for the leaderboard'''

	# Redirects to homepage if user not logged in
	if "user_id" not in session:
		return redirect("/")

	# Queries the database for a sum of users' scores, user_id, and username by joining the users and scores table on user_id
	# grouping by scores and user_ID, and ordering by sum in descending

	sql = """SELECT SUM(score), scores.user_id, username 
			FROM scores JOIN users USING (user_id)
			GROUP BY scores.user_id, username 
			ORDER BY SUM(score) DESC
			"""
			
	# executing the query, and fetching all records
	cursor = db.session.execute(sql)

	# gets a list of the game_leader objects
	game_leaders = cursor.fetchall()

	# Uses Jinja2 variarbles with a list of game_leader objects (game_leaders) and length of this list to use in Jinha2 variables for relative ranking
	return render_template('leaderboard.html', name=session["name"], leaders=game_leaders, length=len(game_leaders))


@app.route('/view_history')
def view_game_history():
	''' a route that allows a user to view all records of game history'''

	# Redirects user to home if not logged in
	if "user_id" not in session:
		return redirect("/")

	# Queries the database for the word, score, and whether or not the user has won the game baed on user_id, 
	# sorting results by date in descending order
	sql = """SELECT word, won, score, date
			FROM scores 
			WHERE user_id= :user_id
			ORDER BY date DESC
			"""

	# gets the user_id from the session
	user_id = session["user_id"]

	# adds user_id to :user_id varbale insql statement, and executes query
	cursor = db.session.execute(sql, {"user_id": user_id})

	# gets a list of the game_record objects
	game_record = cursor.fetchall()

	# getting the sum of the users scores
	scores = []
	for game in game_record:
		scores.append(game.score)
	sum_scores = sum(scores)

	# Uses Jinja2 variables to render game_record information on template
	return render_template('history.html', game_history=game_record, name=session["name"], scores_total=sum_scores)


@app.route('/game_rules')
def get_rules():
	''' gets game rules '''

	if "user_id" not in session:
		return redirect("/")

	return render_template('rules.html', name=session["name"])

# if you run the file directly, will run code below
if __name__ == "__main__": # pragma: no cover
	connect_to_db(app)  # pragma: no cover
	app.run() # pragma: no cover

