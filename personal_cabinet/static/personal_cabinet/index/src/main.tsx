import './modals/add_telegram_bot_modal';

import Toast from 'global_modules/toast';
import { TelegramBotsApi } from 'telegram_bot_api/main';
import TelegramBotCard from 'telegram_bot_frontend/components/TelegramBotCard';
import { createRoot } from 'react-dom/client';
import React from 'react';

declare const telegramBotNotAddedYetText: string;
declare const telegramBotCardFooterPersonalCabinetButtonText: string;

export namespace TelegramBotCards {
	const root = createRoot(document.querySelector<HTMLDivElement>('#telegramBots')!);

	export async function update(): Promise<void> {
		const response = await TelegramBotsApi.get();

		if (response.ok) {
			root.render(response.json.length > 0 ? (
				response.json.map(telegramBot => (
					<TelegramBotCard key={telegramBot.id} telegramBotInitial={telegramBot}>
						<div className='card-footer border-0 p-0'>
							<a
								className='btn btn-light border border-top-0 rounded-top-0 w-100 px-3 py-2'
								href={`/telegram-bot-menu/${telegramBot.id}/`}
							>{telegramBotCardFooterPersonalCabinetButtonText}</a>
						</div>
					</TelegramBotCard>
				))
			) : (
				<div className='border rounded text-center p-3'>{telegramBotNotAddedYetText}</div>
			));
		} else {
			new Toast(response.json.message, response.json.level).show();
		}
	}
}

TelegramBotCards.update();