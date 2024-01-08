import { Dispatch, SetStateAction, createContext } from 'react';

import { TelegramBot } from 'services/api/telegram_bots/types';

export interface TelegramBotsContextProps {
	telegramBots: TelegramBot[];
	setTelegramBots: Dispatch<SetStateAction<TelegramBot[]>>;
}

const TelegramBotsContext = createContext<TelegramBotsContextProps | undefined>(undefined);

export default TelegramBotsContext;