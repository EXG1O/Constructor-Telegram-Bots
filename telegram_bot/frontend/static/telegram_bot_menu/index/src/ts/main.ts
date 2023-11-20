import 'default_entry/main';

import { Toast } from 'global_modules/toast';
import { TelegramBotApi } from 'telegram_bot_api/main';
import { CustomTelegramBotCard } from './custom_telegram_bot_card';

declare const telegramBotId: number;

const telegramBotCardParentDiv = document.querySelector('#telegramBotCard') as HTMLDivElement;

TelegramBotApi.get(telegramBotId).then(response => {
	if (response.ok) {
		new CustomTelegramBotCard(telegramBotCardParentDiv, response.json);
	} else {
		new Toast(response.json.message, response.json.level).show();
	}
});