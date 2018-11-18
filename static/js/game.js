"use strict";

$("#letter-guessing-form").on('submit', checkLetter)

function checkLetter(evt) {
	evt.preventDefault()
	const letterChoice = {
		'letter': $('#letter-input').val()
	};

	$.get('/check', letterChoice, (results) => {
		alert(results["message"]);
		if (results.hasOwnProperty('indices')) {
			let indices = results['indices'];
			addLetter(indices, letterChoice['letter']);
		} else if (results["message"].includes("Sorry, Incorrect Guess!")) {
			$("#incorrect-letters-guessed").append(letterChoice["letter"] + " ")
		}

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