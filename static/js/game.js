"use strict";


function checkLetter(evt) {
	evt.preventDefault()
	const letterChoice = {
		'letter': $('#letter-input').val()
	};

	$.get('/check', letterChoice, (results) => {
		if (results.hasOwnProperty('indices')) {
			let indices = results['indices'];
			addLetter(indices, letterChoice['letter']);
		} else if (results["message"].includes("Sorry, Incorrect Guess!")) {
			$("#incorrect-letters-guessed").append(letterChoice["letter"] + " ");
		} else if (results.hasOwnProperty('word')) {
			$("#incorrect-letters-guessed").append(letterChoice["letter"])
			$("div#word-to-guess").html(results["word"])
		};
		$("#num-remaining-guesses").html(results["remaining_guesses"])
		alert(results["message"]);

	});
}

function addLetter(indices, letter) {
	console.log("inside add letters")
	let i;
	for (i=0; i<indices.length; i++){
		console.log(i)
		let itemId = indices[i];
		console.log(itemId)
		$(`#${itemId}`).html(letter);
	};
}

$("#letter-guessing-form").on('submit', checkLetter)