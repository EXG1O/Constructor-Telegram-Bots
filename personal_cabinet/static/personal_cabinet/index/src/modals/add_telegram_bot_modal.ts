import Toast from 'global_modules/toast';
import { TelegramBotApi } from 'telegram_bot_api/main';
import { TelegramBotCards } from '../main';
import { Modal } from 'bootstrap';

const modal = new Modal('#addTelegramBotModal');
const modalToggleButtonElement = document.querySelector<HTMLButtonElement>('#addTelegramBotModalButton')!;

const apiTokenInputElement = document.querySelector<HTMLInputElement>('#addTelegramBotModalApiTokenInput')!;
const isPrivateCheckBoxElement = document.querySelector<HTMLInputElement>('#addTelegramBotModalIsPrivateCheckBox')!;
const addButtonElement = document.querySelector<HTMLButtonElement>('#addTelegramBotModalAddTelegramBotButton')!;

addButtonElement.addEventListener('click', async () => {
	const response = await TelegramBotApi.create({
		api_token: apiTokenInputElement.value,
		is_private: isPrivateCheckBoxElement.checked,
	});

	if (response.ok) {
		TelegramBotCards.update();

		modal.hide();
	}

	new Toast(response.json.message, response.json.level).show();
});

modalToggleButtonElement.addEventListener('click', () => {
	apiTokenInputElement.value = '';
	isPrivateCheckBoxElement.checked = false;

	modal.toggle();
});