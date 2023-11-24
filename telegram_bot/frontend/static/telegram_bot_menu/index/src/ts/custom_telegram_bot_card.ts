import { Toast } from 'global_modules/toast';
import { askConfirmModal } from 'global_modules/modals/ask_confirm_modal';
import { TelegramBotApi } from 'telegram_bot_api/main';
import { TelegramBotCard } from 'telegram_bot_frontend/telegram_bot_card';

declare const telegramBotCardFooterStartButtonText: string;
declare const telegramBotCardFooterStopButtonText: string;
declare const deleteTelegramBotAskConfirmModalTitle: string;
declare const deleteTelegramBotAskConfirmModalText: string;
declare const telegramBotCardFooterDeleteButtonText: string;

export class CustomTelegramBotCard extends TelegramBotCard {
	private updateStartOrStopButton(): void {
		const button = this.div.querySelector('#telegramBotCardFooterStartOrStopButton') as HTMLButtonElement;

		const colorsAntonyms: Record<string, string> = {
			success: 'danger',
			danger: 'success',
		}
		let buttonColor: keyof typeof colorsAntonyms;

		if (!this.telegramBot.is_running && this.telegramBot.is_stopped) {
			buttonColor = 'success';
			button.innerHTML = telegramBotCardFooterStartButtonText;
		} else {
			buttonColor = 'danger';
			button.innerHTML = telegramBotCardFooterStopButtonText;
		}

		if (!button.classList.replace(`btn-${colorsAntonyms[buttonColor]}`, `btn-${buttonColor}`)) {
			button.classList.add(`btn-${buttonColor}`);
		}
	}
	private setupFooterElements(): void {
		const startOrStopButton = this.div.querySelector('#telegramBotCardFooterStartOrStopButton') as HTMLButtonElement;
		const deleteButton = this.div.querySelector('#telegramBotCardFooterDeleteButton') as HTMLButtonElement;

		startOrStopButton.addEventListener('click', (): void => {
			if (!this.telegramBot.is_running && this.telegramBot.is_stopped) {
				TelegramBotApi.start(this.telegramBot.id);
			} else {
				TelegramBotApi.stop(this.telegramBot.id);
			}
		});
		deleteButton.addEventListener('click', (): void => {
			askConfirmModal(
				deleteTelegramBotAskConfirmModalTitle,
				deleteTelegramBotAskConfirmModalText,
				async (): Promise<void> => {
					const response = await TelegramBotApi.delete_(this.telegramBot.id);

					if (response.ok) {
						await this.delete();
					}

					new Toast(response.json.message, response.json.level).show();
				},
			)
		});
	}
	protected setupUI(): void {
		this.updateStartOrStopButton();

		super.setupUI();

		this.setupFooterElements();
	}
	protected create(): void {
		const footer = document.createElement('div');
		footer.className = 'card-footer d-flex flex-wrap border border-top-0 p-3 gap-3';
		footer.innerHTML = `
			<button class="btn flex-fill" id="telegramBotCardFooterStartOrStopButton" type="button"></button>
			<button class="btn btn-danger flex-fill" id="telegramBotCardFooterDeleteButton" type="button">${telegramBotCardFooterDeleteButtonText}</button>
		`;
		this.div.appendChild(footer);

		super.create();
	}
	public async delete(): Promise<void> {
		const response = await TelegramBotApi.delete_(this.telegramBot.id);

		if (response.ok) {
			super.delete();
		}

		new Toast(response.json.message, response.json.level).show();
	}
}