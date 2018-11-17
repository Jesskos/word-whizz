"use strict";

$("#letter-guessing-form").on('submit', checkLetter)

function checkLetter(evt) {
	evt.preventDefault()
	const letterChoice = {
		'letter': $('#letter-input').val()
	};
	console.log(letterChoice)
	$.get('/check', letterChoice, (results) => {
		alert(results)
	});
}
