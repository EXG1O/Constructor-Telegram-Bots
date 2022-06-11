function hideOrShowButtonClick() {
	var inputPasswordElement = document.getElementById('inputBotToken');

	if (inputPasswordElement.getAttribute('type') == 'password') {
		inputPasswordElement.setAttribute('type', 'text');

		var buttonElement = document.getElementById('hideBotToken');
		buttonElement.setAttribute('id', 'showBotToken');
	} else {
		inputPasswordElement.setAttribute('type', 'password');

		var buttonElement = document.getElementById('showBotToken');
		buttonElement.setAttribute('id', 'hideBotToken');
	}
}

function startBotButtonClick() {
	var request = new XMLHttpRequest();
	request.open('POST', 'start_bot/', true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = function() {
		if (request.status == 200) {
			showSuccessMessage(request.responseText);

			var startBotButtonElement = document.getElementsByClassName('start-bot-button-control')[0];
			startBotButtonElement.setAttribute('class', 'stop-bot-button-control');
			startBotButtonElement.setAttribute('onclick', 'stopBotButtonClick()');
			startBotButtonElement.innerHTML = 'Остоновить бота';
		} else {
			showErrorMessage(request.responseText);
		}
	}
	request.send();
}

function stopBotButtonClick() {
	var request = new XMLHttpRequest();
	request.open('POST', 'stop_bot/', true);
	request.setRequestHeader('Content-Type', 'application/json');
	request.onreadystatechange = function() {
		if (request.status == 200) {
			showSuccessMessage(request.responseText);

			var stopBotButtonElement = document.getElementsByClassName('stop-bot-button-control')[0];
			stopBotButtonElement.setAttribute('class', 'start-bot-button-control');
			stopBotButtonElement.setAttribute('onclick', 'startBotButtonClick()');
			stopBotButtonElement.innerHTML = 'Запустить бота';
		} else {
			showErrorMessage(request.responseText);
		}
	}
	request.send();
}