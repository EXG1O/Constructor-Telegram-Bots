import { Toast } from 'global_modules/toast';
import { askConfirmModal } from 'global_modules/modals/ask_confirm_modal';
import { TelegramBotUserApi, TelegramBotAllowedUserApi } from 'telegram_bot_api/main';
import { TelegramBotUser } from 'telegram_bot_api/types';

declare const telegramBotId: number;
declare const telegramBotIsPrivate: boolean;
declare const askConfirmModalDeleteTelegramBotUserTitle: string;
declare const askConfirmModalDeleteTelegramBotUserText: string;

const usersParentElement = document.querySelector('#telegramBotUsers') as HTMLDivElement;

export class User {
	public element: HTMLDivElement;
	public actionButtonGroupElement: HTMLDivElement;
	public user: TelegramBotUser;
	public onDidDeleteFunc?: () => void;

	public constructor(user: TelegramBotUser) {
		this.user = user;

		this.element = document.createElement('div');
		this.element.className = 'list-group-item p-3';
		this.element.innerHTML = `
			<div class="d-flex align-items-center gap-3">
				<p class="flex-fill m-0">[<span class="text-success-emphasis">${user.activated_date}</span>]: <span class="text-primary">${user.user_id}</span> - ${user.full_name}</p>
				<div class="d-flex btn-group btn-action-group" role="group"></div>
			</div>
		`;
		usersParentElement.appendChild(this.element);

		this.actionButtonGroupElement = this.element.querySelector('.btn-action-group') as HTMLDivElement;

		this.createActionButtons();
	}

	protected createActionButton(buttonColor: string, bootstrapIconName: string, buttonTextColor?: string, isShow: boolean = true): HTMLButtonElement {
		const button = document.createElement('button');
		button.className = `btn btn-${buttonColor}${buttonTextColor ? ` text-${buttonTextColor}` : ''} bi bi-${bootstrapIconName} px-2 py-0${!isShow ? ' d-none' : ''}`;
		button.type = 'button';
		button.style.fontSize = '20px';
		return button;
	}

	protected createActionButtons(): void {
		const setAllowedButton = this.createActionButton('warning', 'star', 'light', telegramBotIsPrivate && !this.user.is_allowed);
		const unsetAllowedButton = this.createActionButton('warning', 'star-fill', 'light', telegramBotIsPrivate && this.user.is_allowed);
		const deleteButton = this.createActionButton('danger', 'trash');

		unsetAllowedButton.classList.add('rounded-start');

		this.actionButtonGroupElement.append(setAllowedButton, unsetAllowedButton, deleteButton);

		setAllowedButton.addEventListener('click', async (): Promise<void> => {
			const response = await TelegramBotAllowedUserApi.set(telegramBotId, this.user.id);

			if (response.ok) {
				this.user.is_allowed = true;

				setAllowedButton.classList.add('d-none');
				unsetAllowedButton.classList.remove('d-none');
			}

			new Toast(response.json.message, response.json.level).show();
		});
		unsetAllowedButton.addEventListener('click', async (): Promise<void> => {
			const response = await TelegramBotAllowedUserApi.unset(telegramBotId, this.user.id);

			if (response.ok) {
				this.user.is_allowed = false;

				setAllowedButton.classList.remove('d-none');
				unsetAllowedButton.classList.add('d-none');
			}

			new Toast(response.json.message, response.json.level).show();
		});
		deleteButton.addEventListener('click', (): void => {
			askConfirmModal(
				askConfirmModalDeleteTelegramBotUserTitle,
				askConfirmModalDeleteTelegramBotUserText,
				async () => {
					const response = await TelegramBotUserApi.delete_(telegramBotId, this.user.id);

					if (response.ok) {
						if (this.onDidDeleteFunc) {
							this.onDidDeleteFunc();
						}

						this.delete();
					}

					new Toast(response.json.message, response.json.level).show();
				},
			);
		});
	}

	public delete(): void {
		this.element.remove();
	}
}