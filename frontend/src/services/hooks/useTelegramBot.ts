import { useContext } from 'react';

import TelegramBotContext, { TelegramBotContextProps } from 'services/contexts/TelegramBotContext';

function useTelegramBot(): TelegramBotContextProps {
	const telegramBot = useContext<TelegramBotContextProps | undefined>(TelegramBotContext);

	if (telegramBot === undefined) {
		throw new Error('useTelegramBot must be used with a TelegramBotProvider!');
	}

	return telegramBot;
}

export default useTelegramBot;