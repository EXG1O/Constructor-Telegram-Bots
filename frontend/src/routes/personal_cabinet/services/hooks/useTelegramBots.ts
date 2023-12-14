import { useContext } from 'react';

import TelegramBotsContext, { TelegramBotsContextProps } from '../contexts/TelegramBotsContext';

function useTelegramBots(): TelegramBotsContextProps {
	const telegramBots = useContext<TelegramBotsContextProps | undefined>(TelegramBotsContext);

	if (telegramBots === undefined) {
		throw new Error('useTelegramBots must be used with a TelegramBotsContext!');
	}

	return telegramBots;
}

export default useTelegramBots;