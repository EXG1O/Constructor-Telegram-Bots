import Toast from 'global_modules/toast';
import { TelegramBotUsersApi } from 'telegram_bot_api/main';
import UserListGroupItem from './components/UserListGroupItem';
import { createRoot } from 'react-dom/client';
import React from 'react';

declare const telegramBotId: number;
declare const telegramBotNotActivatedYetText: string;

export namespace UserListGroup {
	const root = createRoot(document.querySelector<HTMLDivElement>('#telegramBotUsers')!);

	const collapseButtonElement = document.querySelector<HTMLButtonElement>('#telegramBotUsersСollapseButton')!;
	const updateButtonElement = document.querySelector<HTMLButtonElement>('#telegramBotUsersUpdateButton')!;

	export async function update(): Promise<void> {
		const response = await TelegramBotUsersApi.get(telegramBotId);

		if (response.ok) {
			root.render(response.json.length > 0 ? (
				response.json.map(user => <UserListGroupItem key={user.id} userInitial={user}/>)
			) : (
				<div className='list-group-item text-center p-3'>{telegramBotNotActivatedYetText}</div>
			));
		} else {
			new Toast(response.json.message, response.json.level).show();
		}
	}

	collapseButtonElement.addEventListener('click', (): boolean => updateButtonElement.classList.toggle('disabled'));
	updateButtonElement.addEventListener('click', async (): Promise<void> => await update());
}

UserListGroup.update();