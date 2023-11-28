import './modals/add_telegram_bot_modal';

import { Toast } from 'global_modules/toast';
import { TelegramBotsApi } from 'telegram_bot_api/main';
import { TelegramBot } from 'telegram_bot_api/types';
import { TelegramBotCard } from './components';

declare const telegramBotNotAddedYetText: string;

export namespace TelegramBotCards {
	export const parentElement = document.querySelector('#telegramBots') as HTMLDivElement;
	export const object: Record<TelegramBot['id'], TelegramBotCard> = {};

	export function checkCount() {
		const element = parentElement.querySelector('#telegramBotNotAddedYet');
		const objectLength = Object.keys(object).length;

		if (element && objectLength !== 0) {
			element.remove();
		} else if (!element && objectLength === 0) {
			const newElement = document.createElement('div');
			newElement.className = 'border rounded text-center p-3';
			newElement.id = 'telegramBotNotAddedYet';
			newElement.innerHTML = telegramBotNotAddedYetText;
			parentElement.appendChild(newElement);
		}
	}

	export async function update(): Promise<void> {
		const response = await TelegramBotsApi.get();

		if (response.ok) {
			response.json.forEach(telegramBot => {
				if (telegramBot.id in object) {
					object[telegramBot.id].update(telegramBot);
				} else {
					new TelegramBotCard(telegramBot);
				}
			});
			Object.keys(object).forEach(telegramBotId_ => {
				const telegramBotId = Number.parseInt(telegramBotId_);

				if (!(telegramBotId in object)) {
					object[telegramBotId].delete();
				}
			});

			checkCount();
		} else {
			new Toast(response.json.message, response.json.level).show();
		}
	}
}

TelegramBotCards.update();