import { Toast } from 'global_modules/toast';
import { TelegramBotApi } from 'telegram_bot_api/main';
import { TelegramBot } from 'telegram_bot_api/types';

declare const telegramBotCardHeaderIsRunningText: string;
declare const telegramBotCardHeaderIsNotRunningText: string;
declare const telegramBotCardBodyTableLineApiTokenText: string;
declare const telegramBotCardBodyTableLineIsPrivateText: string;
declare const telegramBotCardBodyTableLineDateAddedText: string;
declare const telegramBotCardBodyTableLineApiTokenInputPlaceholderText: string;

export class TelegramBotCard {
	protected telegramBot: TelegramBot;
	protected element: HTMLDivElement;
	protected headerElement: HTMLHeadingElement;
	protected usernameElement: HTMLAnchorElement;
	protected apiTokenElement: HTMLSpanElement;
	protected apiTokenEditButtonElement: HTMLButtonElement;
	protected apiTokenSaveButtonElement: HTMLButtonElement;
	protected apiTokenCancelButtonElement: HTMLButtonElement;
	protected isPrivateCheckboxElement: HTMLInputElement;

	public constructor(parentElement: HTMLElement, telegramBot: TelegramBot) {
		this.telegramBot = telegramBot;

		this.element = document.createElement('div');
		this.element.className = 'card border-0';
		this.element.innerHTML = `
			<h5 class="card-header border fw-semibold text-center"></h5>
			<div class="card-body border p-2">
				<table class="table table-sm table-borderless align-middle mb-0">
					<tbody>
						<tr>
							<th scope="row">@username:</th>
							<td class="text-break">
								<a class="link-dark link-underline-opacity-0 username" href="tg://resolve?domain=${this.telegramBot.username}">@${this.telegramBot.username}</a>
							</td>
						</tr>
						<tr>
							<th scope="row">${telegramBotCardBodyTableLineApiTokenText}:</td>
							<td class="text-break">
								<div class="d-flex gap-2">
									<span class="flex-fill api-token">${this.telegramBot.api_token}</span>
									<div class="d-flex justify-content-center align-items-center gap-1">
										<i class="bi bi-pencil-square text-secondary btn-edit-api-token" type="button" style="font-size: 20px; -webkit-text-stroke: 0.4px;"></i>
										<i class="bi bi-check-lg text-success btn-save-api-token d-none" type="button" style="font-size: 20px; -webkit-text-stroke: 1.4px;"></i>
										<i class="bi bi-x-lg text-danger btn-cancel-api-token d-none" type="button" style="font-size: 20px; -webkit-text-stroke: 1.8px;"></i>
									</div>
								</div>
							</td>
						</tr>
						<tr>
							<th scope="row">${telegramBotCardBodyTableLineIsPrivateText}:</th>
							<td>
								<div class="form-check form-switch mb-0">
									<input class="form-check-input is-private" type="checkbox"${(this.telegramBot.is_private) ? ' checked': ''}>
								</div>
							</td>
						</tr>
						<tr>
							<th scope="row">${telegramBotCardBodyTableLineDateAddedText}:</th>
							<td>${this.telegramBot.added_date}</td>
						</tr>
					</tbody>
				</table>
			</div>
		`;
		parentElement.appendChild(this.element);

		this.headerElement = this.element.querySelector('.card-header') as HTMLHeadingElement;
		this.usernameElement = this.element.querySelector('.username') as HTMLAnchorElement;
		this.apiTokenElement = this.element.querySelector('.api-token') as HTMLSpanElement;
		this.apiTokenEditButtonElement = this.element.querySelector('.btn-edit-api-token') as HTMLButtonElement;
		this.apiTokenSaveButtonElement = this.element.querySelector('.btn-save-api-token') as HTMLButtonElement;
		this.apiTokenCancelButtonElement = this.element.querySelector('.btn-cancel-api-token') as HTMLButtonElement;
		this.isPrivateCheckboxElement = this.element.querySelector('.is-private') as HTMLInputElement;

		this.updateHeaderElement();

		this.setupApiTokenElements();
		this.setupIsPrivateCheckboxElement();
	}

	public async checkStatus(): Promise<void> {
		const response = await TelegramBotApi.get(this.telegramBot.id);

		if (response.ok) {
			if (this.telegramBot.is_running && !this.telegramBot.is_stopped) {

			} else if (!this.telegramBot.is_running && this.telegramBot.is_stopped) {

			} else {
				setTimeout(this.checkStatus, 3000);
			}
		} else {
			new Toast(response.json.message, response.json.level).show();
		}
	}

	private updateHeaderElement(): void {
		const colorMappings: Record<string, string> = {
			success: 'danger',
			danger: 'success',
		}
		let сolor: keyof typeof colorMappings;

		if (!this.telegramBot.is_running && this.telegramBot.is_stopped) {
			сolor = 'danger';

			this.headerElement.innerHTML = telegramBotCardHeaderIsNotRunningText;
		} else {
			сolor = 'success';

			this.headerElement.innerHTML = telegramBotCardHeaderIsRunningText;
		}

		['text-bg-', 'border-'].forEach(class_ => {
			if (!this.headerElement.classList.replace(class_ + colorMappings[сolor], class_ + сolor)) {
				this.headerElement.classList.add(class_ + сolor);
			}
		});
	}

	private setupApiTokenElements(): void {
		const toggle = (): void => {
			if (this.apiTokenElement.querySelector('input')) {
				this.apiTokenElement.innerHTML = this.telegramBot.api_token;
			} else {
				this.apiTokenElement.innerHTML = `<input class="form-control" type="text" placeholder="${telegramBotCardBodyTableLineApiTokenInputPlaceholderText}" value="${this.telegramBot.api_token}">`;
			}

			this.apiTokenEditButtonElement.classList.toggle('d-none');
			this.apiTokenSaveButtonElement.classList.toggle('d-none');
			this.apiTokenCancelButtonElement.classList.toggle('d-none');
		}

		this.apiTokenEditButtonElement.addEventListener('click', toggle);
		this.apiTokenSaveButtonElement.addEventListener('click', async (): Promise<void> => {
			const newApiToken = (this.apiTokenElement.querySelector('input') as HTMLInputElement).value;

			const response = await TelegramBotApi.update(this.telegramBot.id, {
				api_token: newApiToken,
				is_private: null,
			});

			if (response.ok) {
				this.update();
			}

			new Toast(response.json.message, response.json.level).show();
		});
		this.apiTokenCancelButtonElement.addEventListener('click', toggle);
	}

	private setupIsPrivateCheckboxElement(): void {
		this.isPrivateCheckboxElement.addEventListener('change', async (): Promise<void> => {
			const response = await TelegramBotApi.update(this.telegramBot.id, {
				api_token: null,
				is_private: this.isPrivateCheckboxElement.checked,
			});

			if (response.ok) {
				this.telegramBot.is_private = this.isPrivateCheckboxElement.checked;
			}

			this.isPrivateCheckboxElement.checked = this.telegramBot.is_private;

			new Toast(response.json.message, response.json.level).show();
		});
	}

	public reset(): void {
		this.updateHeaderElement();

		this.usernameElement.innerHTML = `@${this.telegramBot.username}`;
		this.usernameElement.href = `tg://resolve?domain=${this.telegramBot.username}`;
		this.apiTokenElement.innerHTML = this.telegramBot.api_token;
		this.apiTokenEditButtonElement.classList.remove('d-none');
		this.apiTokenSaveButtonElement.classList.add('d-none');
		this.apiTokenCancelButtonElement.classList.add('d-none');
		this.isPrivateCheckboxElement.checked = this.telegramBot.is_private;
	}

	public async update(telegramBot?: TelegramBot): Promise<void> {
		if (telegramBot) {
			this.telegramBot = telegramBot;
		} else {
			const response = await TelegramBotApi.get(this.telegramBot.id);

			if (response.ok) {
				this.telegramBot = response.json;
			} else {
				new Toast(response.json.message, response.json.level).show();
				return;
			}
		}

		this.reset();
	}

	public delete(): void {
		this.element.remove();
	}
}