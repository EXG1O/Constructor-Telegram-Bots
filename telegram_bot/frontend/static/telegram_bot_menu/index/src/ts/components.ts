import { Toast } from 'global_modules/toast';
import { askConfirmModal } from 'global_modules/modals/ask_confirm_modal';
import { TelegramBotApi } from 'telegram_bot_api/main';
import { TelegramBot } from 'telegram_bot_api/types';
import { TelegramBotCard as BaseTelegramBotCard } from 'telegram_bot_frontend/components';

declare const personalCabinetUrl: string;
declare const telegramBotCardFooterStartButtonText: string;
declare const telegramBotCardFooterStopButtonText: string;
declare const askConfirmModalDeleteTelegramBotTitle: string;
declare const askConfirmModalDeleteTelegramBotText: string;
declare const telegramBotCardFooterDeleteButtonText: string;

export class TelegramBotCard extends BaseTelegramBotCard {
	public constructor(parentElement: HTMLElement, telegramBot: TelegramBot) {
		super(parentElement, telegramBot);

		const footer = document.createElement('div');
		footer.className = 'card-footer d-flex flex-wrap border border-top-0 p-3 gap-3';
		footer.innerHTML = `
			<button class="btn flex-fill" id="telegramBotCardFooterStartOrStopButton" type="button"></button>
			<button class="btn btn-danger flex-fill" id="telegramBotCardFooterDeleteButton" type="button">${telegramBotCardFooterDeleteButtonText}</button>
		`;
		this.element.appendChild(footer);

		this.updateStartOrStopButton();

		this.setupFooterElements();
	}

	private updateStartOrStopButton(): void {
		const button = this.element.querySelector('#telegramBotCardFooterStartOrStopButton') as HTMLButtonElement;

		const colorMappings: Record<string, string> = {
			success: 'danger',
			danger: 'success',
		}
		let color: keyof typeof colorMappings;

		if (!this.telegramBot.is_running && this.telegramBot.is_stopped) {
			color = 'success';

			button.innerHTML = telegramBotCardFooterStartButtonText;
		} else {
			color = 'danger';

			button.innerHTML = telegramBotCardFooterStopButtonText;
		}

		if (!button.classList.replace(`btn-${colorMappings[color]}`, `btn-${color}`)) {
			button.classList.add(`btn-${color}`);
		}
	}

	private setupFooterElements(): void {
		const startOrStopButton = this.element.querySelector('#telegramBotCardFooterStartOrStopButton') as HTMLButtonElement;
		const deleteButton = this.element.querySelector('#telegramBotCardFooterDeleteButton') as HTMLButtonElement;

		startOrStopButton.addEventListener('click', (): void => {
			if (!this.telegramBot.is_running && this.telegramBot.is_stopped) {
				TelegramBotApi.start(this.telegramBot.id);
			} else if (this.telegramBot.is_running && !this.telegramBot.is_stopped) {
				TelegramBotApi.stop(this.telegramBot.id);
			}
		});
		deleteButton.addEventListener('click', (): void => {
			askConfirmModal(
				askConfirmModalDeleteTelegramBotTitle,
				askConfirmModalDeleteTelegramBotText,
				async (): Promise<void> => {
					const response = await TelegramBotApi.delete_(this.telegramBot.id);

					if (response.ok) {
						setTimeout(() => window.location.href = personalCabinetUrl, 3000);
					}

					new Toast(response.json.message, response.json.level).show();
				},
			);
		});
	}
}