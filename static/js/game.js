"use strict";

// checking a letter, and adding a letter to JavaScript based on element ID and index of letter in word

function checkLetter(evt) {
	// gets a letter from the form, and sends a request to the server
	evt.preventDefault()
	const letterChoice = {
		'letter': $('#letter-input').val()
	};
	$.get('/check', letterChoice, getUpdate)};


function getUpdate(results) {

		// resets form so user does not have to delete letters
		document.getElementById("letter-guessing-form").reset();

		// checks if letter was a correct guess, and adds indices of letter to DOM
		if (results["message"].includes("Correct Guess!")) {
			addLetter(results["indices"], results['letter']);
			alert(results["message"]);

		// checks if letter was an incorrect guess, and adds incorrect choices to DOM
		} else if (results["message"].includes("Sorry, Incorrect Guess!")) {
			$("#incorrect-letters-guessed-list").append(results["letter"] + " ");
			growAntiProgessBar(results["remaining_guesses"]);
			alert(results["message"]);
		
		// checks if user lost the game, and show modal to play again
		} else if (results["message"].includes("lost the game")) {
			$("#incorrect-letters-guessed-list").append(results["letter" + " "]);
			$("div#word-to-guess").html(results["word"]);
			growAntiProgessBar(results["remaining_guesses"]);
			showModal(results["message"], results["score"]);


		// checks if user won the game, and show modal to play again	
		} else if (results["message"].includes("win")) {
			addLetter(results["indices"], results['letter']);
			showModal(results["message"], results["score"]); 

		// checks if user already guessed a letter
		} else if (results["message"].includes("You already guessed")) {
			alert(results["message"]);

		// checks if a user's game is already over
		} else if (results["message"].includes("The game is over")) {
			showModal(results["message"], results["score"]); 
		};

		// modified the guesses left
		$("#num-remaining-guesses").html(results["remaining_guesses"]);
		};


function addLetter(indices, letter) {
	// a helper functin to add letters to html by searching for element id

	let i;
	for (i=0; i<indices.length; i++){
		console.log(i)
		let itemId = indices[i];
		console.log(itemId)
		$(`#${itemId}`).html(letter);
	};
}


function showModal(notification, score) {
	// shows modal if the user wins or loses

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


function getNewWord(evt) {
	// dynamically gets a new word from the server when user chooses to play again

	// prevents default action of form
	evt.preventDefault()
	let progressBar = document.getElementById("myBar");
	progressBar.style.width = '0'
	// hides modal if displayed
	let modal = document.getElementById('play-modal');
		$("#word-to-guess").empty();
		$("#incorrect-letters-guessed-list").empty()
		modal.style.display="none";

	// gets data from server to load new word while on page, and replaces the html element with new word data
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
	//dynamically changes the difficulty of the word aby sending difficulty level to the server, returning a new work

	// prevents default action of form
	evt.preventDefault();

	// resets progress bar
	let progressBar = document.getElementById("myBar");
	progressBar.style.width = '0'

	// sends difficulty choice to the server
	console.log("in changeDifficulty")
	const difficultyChoice = {
		'difficulty-level': $("#difficulty-rating").val()
	};
	console.log(difficultyChoice);

	// clears out contents of inccorrect letters, word that was previously guessed, and difficulty level
	$("#word-to-guess").empty();
	$("#incorrect-letters-guessed-list").empty()
	$("#Difficulty").empty()

	// sends a request to get a new word from the browser, and adds to the DOM
	$.get('/play_again', difficultyChoice, (results) => {
		console.log(results);
		let letter_index;
 		for (letter_index=0; letter_index<results["word_length"]; letter_index++) {
 			$("#word-to-guess").append(`<span id=${letter_index}>___ </span>`)
 		};
 		$("#num-remaining-guesses").html(results["remaining_guesses"]);
 		$("#word-length").html(results["word_length"]);
 		$("#Difficulty").html(results["difficulty_level"])
	});
}

function makeNewGame(evt) {
	// dynamically changes the word when user selects 'new game', returning a new word at the same difficulty level

	// clears out old words and letters
	$("#word-to-guess").empty();
	$("#incorrect-letters-guessed-list").empty()

	// resets progress bar
	let progressBar = document.getElementById("myBar");
	progressBar.style.width = '0';

	// gets new word from the server, and adds to the DOM
	$.get('/play_again', function (data) {
  		let letter_index;
 		for (letter_index=0; letter_index<data.word_length; letter_index++) {
 			$("#word-to-guess").append(`<span id=${letter_index}>___ </span>`)
 		};
 		$("#num-remaining-guesses").html(data.remaining_guesses)
 		$("#word-length").html(data.word_length)
  		});
}

function growAntiProgessBar(remainingGuesses) {
	// grows an "antiprogress" bar when user with every incorrect guess
	// growth calculated by 100/6, as 6 is the max incorrect guesses
	
	let antiProgressBar = document.getElementById("myBar");
	antiProgressBar.style.width = '0'
	let newWidth = 100 - (remainingGuesses * 17);
	antiProgressBar.style.width = `${newWidth}%`;
}


$("#letter-guessing-form").on("submit", checkLetter);
$("#no-play-again").on("click", closeModal);
$("#play-again").on("click", getNewWord);
$("#change-difficulty").on("submit", changeDifficulty);
$("#reset-game-button").on("click", makeNewGame);




