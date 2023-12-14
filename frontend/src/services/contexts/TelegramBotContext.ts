import { Dispatch, SetStateAction, createContext } from 'react';

import { TelegramBot } from 'services/api/telegram_bots/types';

export interface TelegramBotContextProps {
	telegramBot: TelegramBot;
	setTelegramBot: Dispatch<SetStateAction<TelegramBot | undefined>>;
}

const TelegramBotContext = createContext<TelegramBotContextProps | undefined>(undefined);

export default TelegramBotContext;