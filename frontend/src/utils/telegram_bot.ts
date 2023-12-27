import { TelegramBot } from 'services/api/telegram_bots/types';

export function telegramBotIsStartingOrStopping(telegramBot: TelegramBot): boolean {
	return (
		telegramBot.is_running && telegramBot.is_stopped ||
		!telegramBot.is_running && !telegramBot.is_stopped
	);
}