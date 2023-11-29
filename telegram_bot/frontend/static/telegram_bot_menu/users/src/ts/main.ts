import { Toast } from 'global_modules/toast';
import { TelegramBotUsersApi } from 'telegram_bot_api/main';
import * as Components from './components';

declare const telegramBotId: number;
declare const telegramBotNotActivatedYetText: string;

const usersParentElement = document.querySelector('#telegramBotUsers') as HTMLDivElement;
const usersComponent: Record<number, Components.User> = {};

function checkUsersComponentCount(): void {
	if (Object.keys(usersComponent).length <= 0) {
		const element = document.createElement('div');
		element.className = 'list-group-item text-center p-3';
		element.id = 'telegramBotNotActivated';
		element.innerHTML = telegramBotNotActivatedYetText;
		usersParentElement.append(element);
	} else {
		document.querySelector('#telegramBotNotActivated')?.remove();
	}
}

async function update(): Promise<void> {
	const response = await TelegramBotUsersApi.get(telegramBotId);

	if (response.ok) {
		Object.values(usersComponent).forEach(userComponent => userComponent.delete());
		response.json.forEach(user => {
			const component = new Components.User(user);

			usersComponent[user.id] = component;

			component.onDidDeleteFunc = (): void => {
				delete usersComponent[user.id];

				checkUsersComponentCount();
			}
		});

		checkUsersComponentCount();
	} else {
		new Toast(response.json.message, response.json.level).show();
	}
}

update();