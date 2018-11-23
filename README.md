# Word Whiz
Word Whiz is a fun and educational word guessing game, similar to the "Hangman" game, whereby the computer challenges a player to guess a word. The player is given the length of the word, in which the location of the possible letter are denoted by underlines, and the player guesses a letter. The player must guess the word with less than 6 incorrect letter guesses to win the game. Points are awarded for guessing letters correctly, even if the player loses, in order to encourage the player to continue guessing and learn new words. Fewer points are deducted if the player gueses incorrectly. A bar at the bottom of the page shows the proportion of guesses remaining. The player can adjust the difficulty level on a scale of 1-10 to receive more or less challenging words.


## Contents
* [Technology Stack](#technology-stack)
* [Game Guidelines](#game-guidelines)
* [Features](#features)
* [Design Decisions](#design-decisions)
* [Setup](#setup)
* [Version 2.0](#version-2.0)
* [About the Developer](#about-the-developer)

### Technology Stack 
* Python3
* Flask
* Jinja2
* SQLAlchemy
* JavaScript (AJAX, JSON, jQuery)
* HTML/CSS
* Boostrap
* API: LinkedIn's Word API

### Game Guidelines 
* The player has 6 attempts to guess the word correctly. 
* The computer deducts one attempt each time a guessed letter is not in the word
* The player can adjust difficulty level on a scale from 1-10, with 10 providing the most difficult words.
* The computer sets difficulty level at 3 when the player logs in, but when the player adjusts difficulty level, it is maintained throughput the session.
* The computer awards points for each correctly guessed letter.
* The computer awards more points at higher word difficulty levels.
* The computer will still award points if the player loses the game, but does not award points if the player does not finish the game.

### SetUp

1. Clone the repository to a local directoy 
2. After acitivating the virtual environment:
	* `pip2 install requirements.txt`
3. Create the database:
   * `createdb scoresdb`
4. Run the server:
  * `python server.py`
 *`localhost:5000` in the browser window
5. Check testing coverage by running the following: 
	 *`coverage run --source ../ -m` 
	 * coverage report



### Version 2.0
Coming soon!!

* The computer shows the score dynamically while user is playing the game.
* The player can guess the entire word at once.
* The computer gives a hint to the player by proviging the word's dictinary definition.
* At the end of every game, the computer will display the word's definition to the player.
* The player can adjust minimum and maximum length of the word.
* The player can adjust the difficulty level in the profile. 
* The player will not be able to receive the same word more than once. 

### About the Developer
Jessica is a software engineer and former clinical dietitian based out of San Francisco.