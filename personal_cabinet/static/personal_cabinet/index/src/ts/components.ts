import { TelegramBot } from 'telegram_bot_api/types';
import { TelegramBotCard as BaseTelegramBotCard } from 'telegram_bot_frontend/components';
import { TelegramBotCards } from './main';

declare const telegramBotCardFooterPersonalCabinetButtonText: string;

export class TelegramBotCard extends BaseTelegramBotCard {
	public constructor(telegramBot: TelegramBot) {
		super(TelegramBotCards.parentElement, telegramBot);

		const footer = document.createElement('div');
		footer.className = 'card-footer border-0 p-0';
		footer.innerHTML = `<a class="btn btn-light border border-top-0 rounded-top-0 w-100 px-3 py-2" href="/telegram-bot-menu/${this.telegramBot.id}/">${telegramBotCardFooterPersonalCabinetButtonText}</a>`;
		this.element.appendChild(footer);

		TelegramBotCards.object[this.telegramBot.id] = this;
	}

	public delete(): void {
		super.delete();

		delete TelegramBotCards.object[this.telegramBot.id];
	}
}