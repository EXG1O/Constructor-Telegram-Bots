import { Toast } from 'global_modules/toast';
import { TelegramBotApi } from 'telegram_bot_api/main';
import { TelegramBotCards } from '../main';
import { Modal } from 'bootstrap';

const modal = new Modal('#addTelegramBotModal');
const modalToggleButton = document.querySelector('#addTelegramBotModalButton') as HTMLButtonElement;

const apiTokenInput = document.querySelector('#addTelegramBotModalApiTokenInput') as HTMLInputElement;
const isPrivateCheckBox = document.querySelector('#addTelegramBotModalIsPrivateCheckBox') as HTMLInputElement;
const addButton = document.querySelector('#addTelegramBotModalAddTelegramBotButton') as HTMLButtonElement;

addButton.addEventListener('click', async () => {
	const response = await TelegramBotApi.create({
		api_token: apiTokenInput.value,
		is_private: isPrivateCheckBox.checked,
	});

	if (response.ok) {
		TelegramBotCards.update();

		modal.hide();
	}

	new Toast(response.json.message, response.json.level).show();
});

modalToggleButton.addEventListener('click', () => {
	apiTokenInput.value = '';
	isPrivateCheckBox.checked = false;

	modal.toggle();
});