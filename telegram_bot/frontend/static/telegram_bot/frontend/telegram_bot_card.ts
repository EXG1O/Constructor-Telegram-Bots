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
	public telegramBot: TelegramBot;
	public parentDiv: HTMLDivElement;
	public div: HTMLDivElement;

	public constructor(parentDiv: HTMLDivElement, telegramBot: TelegramBot) {
		this.telegramBot = telegramBot;
		this.parentDiv = parentDiv;

		this.div = document.createElement('div');
		this.div.className = 'card border-0';
		this.div.innerHTML = `
			<h5 class="card-header border fw-semibold text-center"></h5>
			<div class="card-body border p-2">
				<table class="table table-borderless align-middle mb-0">
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
								<div class="d-flex gap-3">
									<div class="api-token flex-fill">${this.telegramBot.api_token}</div>
									<div class="d-flex justify-content-center align-items-center gap-2">
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

		this.create();
	}
	private updateHeader(): void {
		const header = this.div.querySelector('.card-header') as HTMLHeadingElement;

		const сolorsAntonyms: Record<string, string> = {
			success: 'danger',
			danger: 'success',
		}
		let headerColor: keyof typeof сolorsAntonyms;

		if (!this.telegramBot.is_running && this.telegramBot.is_stopped) {
			headerColor = 'danger';
			header.innerHTML = telegramBotCardHeaderIsNotRunningText;
		} else {
			headerColor = 'success';
			header.innerHTML = telegramBotCardHeaderIsRunningText;
		}

		if (!header.classList.replace(`text-bg-${сolorsAntonyms[headerColor]}`, `text-bg-${headerColor}`)) {
			header.classList.add(`text-bg-${headerColor}`);
		}
		if (!header.classList.replace(`border-${сolorsAntonyms[headerColor]}`, `border-${headerColor}`)) {
			header.classList.add(`border-${headerColor}`);
		}
	}
	private setupApiTokenElements(): void {
		const apiTokenDiv = this.div.querySelector('.api-token') as HTMLDivElement;
		const editButton = this.div.querySelector('.btn-edit-api-token') as HTMLButtonElement;
		const saveButton = this.div.querySelector('.btn-save-api-token') as HTMLButtonElement;
		const cancelButton = this.div.querySelector('.btn-cancel-api-token') as HTMLButtonElement;

		const toggle = (): void => {
			if (apiTokenDiv.querySelector('input')) {
				apiTokenDiv.innerHTML = this.telegramBot.api_token;
			} else {
				apiTokenDiv.innerHTML = `<input class="form-control" type="text" placeholder="${telegramBotCardBodyTableLineApiTokenInputPlaceholderText}" value="${this.telegramBot.api_token}">`;
			}

			editButton.classList.toggle('d-none');
			saveButton.classList.toggle('d-none');
			cancelButton.classList.toggle('d-none');
		}

		editButton.addEventListener('click', toggle);
		saveButton.addEventListener('click', async (): Promise<void> => {
			const newApiToken = (apiTokenDiv.querySelector('input') as HTMLInputElement).value;

			const response = await TelegramBotApi.update(this.telegramBot.id, {
				api_token: newApiToken,
				is_private: null,
			});

			if (response.ok) {
				this.telegramBot.api_token = newApiToken;
				apiTokenDiv.innerHTML = this.telegramBot.api_token;
			}

			new Toast(response.json.message, response.json.level).show();
		});
		cancelButton.addEventListener('click', toggle);
	}
	private setupIsPrivateElements(): void {
		const checkBox = this.div.querySelector('input.form-check-input.is-private') as HTMLInputElement;

		checkBox.addEventListener('change', async (): Promise<void> => {
			const response = await TelegramBotApi.update(this.telegramBot.id, {
				api_token: null,
				is_private: checkBox.checked,
			});

			if (response.ok) {
				this.telegramBot.is_private = checkBox.checked;
			}

			new Toast(response.json.message, response.json.level).show();
		});
	}
	protected setupUI(): void {
		this.setupApiTokenElements();
		this.setupIsPrivateElements();
	}
	protected create(): void {
		this.updateHeader();

		this.parentDiv.appendChild(this.div);

		this.setupUI();
	}
	public async update(): Promise<void> {
		const response = await TelegramBotApi.get(this.telegramBot.id);

		if (response.ok) {
			this.telegramBot = response.json;

			this.updateHeader();
		} else {
			new Toast(response.json.message, response.json.level).show();
		}
	}
	public delete(): void {
		this.div.remove();
	}
}