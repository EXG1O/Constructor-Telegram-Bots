import Toast from 'global_modules/toast';
import { TelegramBotApi } from 'telegram_bot_api/main';
import TelegramBotCard from 'telegram_bot_frontend/components/TelegramBotCard';
import TelegramBotCardFooter from './components/TelegramBotCardFooter';
import { createRoot } from 'react-dom/client';
import React from 'react';

declare const telegramBotId: number;

const root = createRoot(document.querySelector<HTMLDivElement>('#telegramBotCard')!);

TelegramBotApi.get(telegramBotId).then(response => {
	if (response.ok) {
		root.render(
			<TelegramBotCard telegramBotInitial={response.json}>
				<TelegramBotCardFooter/>
			</TelegramBotCard>
		);
	} else {
		new Toast(response.json.message, response.json.level).show();
	}
});