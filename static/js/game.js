"use strict";


function checkLetter(evt) {
	evt.preventDefault()
	const letterChoice = {
		'letter': $('#letter-input').val()
	};

	$.get('/check', letterChoice, (results) => {

		// checks for indices in the response, sent only when letter is correct, corresponding to element id
		if (results.hasOwnProperty("indices")) {
			let indices = results["indices"];
			addLetter(indices, letterChoice['letter']);

		// checks for "Incorrect Guess" in the response, sent only when incorrect guess made, to add to list of incorrect letters in html
		} else if (results["message"].includes("Sorry, Incorrect Guess!")) {
			$("#incorrect-letters-guessed").append(letterChoice["letter"] + " ");
		
		// checks for "word" in the response in case player has lost, and need to show resulting word
		} else if (results.hasOwnProperty("word")) {
			$("#incorrect-letters-guessed-list").append(letterChoice["letter" + " "])
			$("div#word-to-guess").html(results["word"])
		};

		// show how many guesses remain, and alert with message after each guess
		$("#num-remaining-guesses").html(results["remaining_guesses"])
		alert(results["message"]);

	});
}

function addLetter(indices, letter) {
	// a functin to add letters to html by searing for element id

	let i;
	for (i=0; i<indices.length; i++){
		console.log(i)
		let itemId = indices[i];
		console.log(itemId)
		$(`#${itemId}`).html(letter);
	};
}

// check letter every time form is submitted
$("#letter-guessing-form").on('submit', checkLetter)