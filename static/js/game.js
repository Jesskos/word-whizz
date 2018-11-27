"use strict";

// checking a letter, and adding a letter to JavaScript based on element ID and index of letter in word

function checkLetter(evt) {
	// gets a letter from the form, and sends a request to the server

	// prevents default action of the form
	evt.preventDefault()
	const letterChoice = {
		'letter': $('#letter-input').val()
	};
	$.get('/check', letterChoice, getUpdateAfterCheckLetter)
};


function getUpdateAfterCheckLetter(results) {

		// resets form so user does not have to delete letters
		document.getElementById("letter-guessing-form").reset();
		
		// checks if letter was a correct guess, and adds indices of letter to DOM
		if (results["message"].includes("Correct Guess!")) {
			addLetter(results["indices"], results['letter']);
			alert(results["message"]);

		// checks if letter was an incorrect guess, and adds incorrect letters and remaining choices to DOM
		} else if (results["message"].includes("Sorry, Incorrect Guess!")) {
			$("#incorrect-letters-guessed-list").append(results["letter"] + " ");
			alert(results["message"]);
		
		// checks if user lost the game, shows the entire word, and displays modal with option to play again along with the player's score
		} else if (results["message"].includes("lost the game")) {
			$("#incorrect-letters-guessed-list").append(results["letter" + " "]);
			$("div#word-to-guess").html(results["secret_word"]);
			showModal(results["message"], results["score"]);

		// checks if user won the game, adds remaining letters, and show modal to play again	
		} else if (results["message"].includes("win")) {
			addLetter(results["indices"], results['letter']);
			showModal(results["message"], results["score"]); 

		// checks if user already guessed the letter, and alerts user
		} else if (results["message"].includes("You already guessed")) {
			alert(results["message"]);

		// checks if a user's game is already over
		} else if (results["message"].includes("The game is over")) {
			showModal(results["message"], results["score"]); 

		} else {
			alert(results["message"])
		};

		// for all outcomes, adjusts remmaining guesses and antiprogress bar
		growAntiProgessBar(results["remaining_guesses"]);
		$("#num-remaining-guesses").html(results["remaining_guesses"]);
};


function checkWord(evt) {
	// gets users word choice, makes a request to the server, and receives a response from the server
	evt.preventDefault();
	// gets users wordchoice from form
	const wordChoice = {
		'word': $("#word-input").val()
	};
	console.log(wordChoice);

	// makes a request and receives the response
	$.get('/check_word', wordChoice, getUpdateAfterCheckWord)
};


function getUpdateAfterCheckWord(results) {

	//empties word form
	document.getElementById("word-guessing-form").reset();

	//if the user wins, shows entire word and displays modal
	if (results["message"].includes("Win")) {
		$("#word-to-guess").html(results["secret_word"]);
		showModal(results["message"], results["score"]); 

	// if the user does not guess the word correctly, also lets them know without showing entire word
	} else if (results["message"].includes("guess was incorrect")) {
		alert(results["message"]);

	// if the user loses the game, lets them know and shows entire word
	} else if (results["message"].includes("lost the game")) {
		$("#word-to-guess").html(results['secret_word']);
		showModal(results["message"], results["score"]);

	// lets the user know if the game has already ended
	} else if (results["message"].includes("The game is over")) {
		showModal(results["message"], results["score"]);

	// all other messages incided below
	} else {
		alert(results["message"])
	};

	// for every response, the 'antiprogres bar' grows in proportion to the guesses remaining
	growAntiProgessBar(results["remaining_guesses"]);
	$("#num-remaining-guesses").html(results["remaining_guesses"]);

};


function addLetter(indices, letter) {
	// a helper functin to add letters to html by searching for element id

	let i;

	// counts up to the length of the list of indices
	// since each index corresponds to the <span> id with the same index, the ___ in the <span>
	// is replaced with the letter at that index
	for (i=0; i<indices.length; i++){
		console.log(i)
		let itemId = indices[i];
		console.log(itemId)
		$(`#${itemId}`).html(letter);
	};
}


function showModal(notification, score) {
	// shows modal if the user wins or loses with the game score and a message

	$('#notification').html(notification);
	$('#game-score').html(score);
	let modal = document.getElementById('play-modal');
	modal.style.display="block";
}


function closeModal(evt) {
	// closes modal when player clicks 'no'

	console.log("in close")
	let modal = document.getElementById('play-modal');
	modal.style.display="none";
}


// functions getNewWord (lines 95-119) and makeNewGame (159-179) can be combined into one function

function getNewWord(evt) {
	// dynamically gets a new word from the server when user chooses to play again (in modal) by clicking the button "New Game"

	// prevents default action of form, and resets "anti-progress bar"
	evt.preventDefault()
	let progressBar = document.getElementById("myBar");
	progressBar.style.width = '0'

	// hides modal if displayed
	let modal = document.getElementById('play-modal');
		$("#word-to-guess").empty();
		$("#incorrect-letters-guessed-list").empty()
		modal.style.display="none";

	// makes an AJAX request to the server to receive a new word, and adds the new word to the DOM
	  $.get('/play_again', function (data) {
  		let letter_index;
 		for (letter_index=0; letter_index<data.word_length; letter_index++) {
 			$("#word-to-guess").append(`<span id=${letter_index}>___ </span>`)
 		};
 		$("#num-remaining-guesses").html(data.remaining_guesses)
 		$("#word-length").html(data.word_length)
  		});
}


function makeNewGame(evt) {
	// dynamically changes the word when user selects 'new game', returning a new word at the same difficulty level

	// clears out old words and letters to prepare for new word
	$("#word-to-guess").empty();
	$("#incorrect-letters-guessed-list").empty()

	// resets anti-progress bar to start new game
	let progressBar = document.getElementById("myBar");
	progressBar.style.width = '0';

	// makes an AJAX request the route in the server below to get a new word, and receives a response with the new word
	$.get('/play_again', function (data) {
  		let letter_index;
 		for (letter_index=0; letter_index<data.word_length; letter_index++) {
 			$("#word-to-guess").append(`<span id=${letter_index}>___ </span>`)
 		};
 		$("#num-remaining-guesses").html(data.remaining_guesses)
 		$("#word-length").html(data.word_length)
  		});
}


function changeDifficulty(evt) {
	//dynamically changes the difficulty of the word by sending a request to the server for a word at that new difficulty level

	// prevents default action of form
	evt.preventDefault();

	// resets ant--progress bar to start new game
	let progressBar = document.getElementById("myBar");
	progressBar.style.width = '0'

	// creates a variable to store difficulty level
	console.log("in changeDifficulty")
	const difficultyChoice = {
		'difficulty-level': $("#difficulty-rating").val()
	};
	console.log(difficultyChoice);

	// clears out DOM contents of inccorrect letters, current word, and difficulty level in preparation for a new word
	$("#word-to-guess").empty();
	$("#incorrect-letters-guessed-list").empty()
	$("#Difficulty").empty()

	// makes an AJAX request to the route in server below with the new diffiuclty level, and receives a response with a new word at that difficulty level
	$.get('/play_again', difficultyChoice, (results) => {
		console.log(results);
		let letter_index;
 		for (letter_index=0; letter_index<results["word_length"]; letter_index++) {
 			$("#word-to-guess").append(`<span id=${letter_index}>___ </span>`)
 		};

 		// adds the new word to teh DOM
 		$("#num-remaining-guesses").html(results["remaining_guesses"]);
 		$("#word-length").html(results["word_length"]);
 		$("#Difficulty").html(results["difficulty_level"])
	});
}


function growAntiProgessBar(remainingGuesses) {
	// grows an "antiprogress" bar with every incorrect guess
	// growth calculated by 100/6, as 6 is the maximum number of incorrect guesses
	
	let antiProgressBar = document.getElementById("myBar");
	antiProgressBar.style.width = '0'
	let newWidth = 100 - (remainingGuesses * 17);
	console.log(newWidth)
	antiProgressBar.style.width = `${newWidth}%`;
}


// loads JQuery after page loads
$(document).ready(function() {

// event listeneners
$("#letter-guessing-form").on("submit", checkLetter);
$("#no-play-again").on("click", closeModal);
$("#play-again").on("click", getNewWord);
$("#change-difficulty").on("submit", changeDifficulty);
$("#reset-game-button").on("click", makeNewGame);
$("#word-guessing-form").on("submit", checkWord)
});




