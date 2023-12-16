import { Dispatch, SetStateAction, createContext } from 'react';

import { TelegramBot } from 'services/api/telegram_bots/types';

export interface TelegramBotContextProps {
	telegramBot: TelegramBot;
	setTelegramBot: Dispatch<SetStateAction<TelegramBot>>;
}

const TelegramBotContext = createContext<TelegramBotContextProps | undefined>(undefined);

export default TelegramBotContext;