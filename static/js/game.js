"use strict";

// checking a letter, and adding a letter to JavaScript based on element ID and index of letter in word

function checkLetter(evt) {
	evt.preventDefault()
	const letterChoice = {
		'letter': $('#letter-input').val()
	};

	console.log(letterChoice)

	$.get('/check', letterChoice, (results) => {

		// checks if letter was a correct guess, and adds indices of letter to DOM
		if (results["message"].includes("Correct Guess!")) {
			let indices = results["indices"];
			addLetter(indices, letterChoice['letter']);
			alert(results["message"]);

		// checks if letter was an incorrect guess, and adds incorrect choices to DOM
		} else if (results["message"].includes("Sorry, Incorrect Guess!")) {
			$("#incorrect-letters-guessed-list").append(letterChoice["letter"] + " ");
			alert(results["message"]);
		
		// checks if user lost the game, and show modal to play again
		} else if (results["message"].includes("lost the game")) {
			$("#incorrect-letters-guessed-list").append(letterChoice["letter" + " "]);
			$("div#word-to-guess").html(results["word"]);
			showModal(results["message"]);

		// checks if user won the game, and show modal to play again	
		} else if (results["message"].includes("win")) {
			showModal(results["message"]); 

		// checks if user already guessed a letter
		} else if (results["message"].includes("You already guessed")) {
			alert(results["message"]);

		// checks if a user's game is already over
		} else if (results["message"].includes("The game is over")) {
			showModal(results["message"]); 
		};

		// modified the guesses left
		$("#num-remaining-guesses").html(results["remaining_guesses"]);
		});
}


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


function showModal(notification) {
	// shows modal if the user wins or loses

	$('#notification').html(notification);
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

	evt.preventDefault()
	let modal = document.getElementById('play-modal');
		$("#word-to-guess").empty();
		$("#incorrect-letters-guessed-list").empty()
		modal.style.display="none";
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

	evt.preventDefault();
	console.log("in changeDifficulty")
	const difficultyChoice = {
		'difficulty-level': $("#difficulty-rating").val()
	};
	console.log(difficultyChoice);
	$("#word-to-guess").empty();
	$("#incorrect-letters-guessed-list").empty()
	$("#Difficulty").empty()
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
	// dynamically changes the word, returning a new word at the same difficulty level

	$("#word-to-guess").empty();
	$("#incorrect-letters-guessed-list").empty()
	$.get('/play_again', function (data) {
  		let letter_index;
 		for (letter_index=0; letter_index<data.word_length; letter_index++) {
 			$("#word-to-guess").append(`<span id=${letter_index}>___ </span>`)
 		};
 		$("#num-remaining-guesses").html(data.remaining_guesses)
 		$("#word-length").html(data.word_length)
  		});
}





$("#letter-guessing-form").on("submit", checkLetter);
$("#no-play-again").on("click", closeModal);
$("#play-again").on("click", getNewWord);
$("#change-difficulty").on("submit", changeDifficulty);
$("#reset-game-button").on("click", makeNewGame);




