# Word Whiz
Word Whiz is a fun and educational word guessing game, similar to the "Hangman" game, whereby the computer challenges a player to guess a word. The player is given the length of the word, denoted by underlines, and the player guesses a letter. The player must guess the word with less than 6 incorrect guesses in order to win the game. Points are awarded for guessing letters correctly, even if the player loses, in order to encourage the player to continue guessing and learn new words. Fewer points are deducted if the player gueses incorrectly. A bar at the bottom of the page shows the proportion of guesses remaining. The player can adjust the difficulty level on a scale of 1-10 to receive more or less challenging words.


## Contents
* [Game Guidelines](#game-guidelines)
* [Technology Stack](#technology-stack)
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
* JavaScript (Ajax, JSON, jQuery)
* HTML/CSS
* Boostrap
* API: LinkedIn's Word API

### Game Guidelines 
* Player has 6 tries to guess the word
* One try is deducted each time a word is guessed incorrectly
* Difficulty level can be adjusted from 1-10, with 10 being the most difficulty
* Difficulty level starts at 3 when logging in, but changes to difficulty level are maintained through user's playing session
* Points are awarded for each correctly guessed letter
* More points are awarded at higher word difficulty levels
* Points can be awarded if the player loses the game, but no points are awarded if the player does not finish the game

### Version 2.0
Coming soon!!

* shows score dynamically while user is playing came
* user can guess the entire word
* give a hint by proviging the word's dictinary definition
* provide the definition of the word at the end of every game
* adjust minimum and maximum length for word
* set difficulty level in profile
* user cannot receive the same word more than once

### About the Developer
Jessica is a software engineer and former clinical dietitian based out of San Francisco.