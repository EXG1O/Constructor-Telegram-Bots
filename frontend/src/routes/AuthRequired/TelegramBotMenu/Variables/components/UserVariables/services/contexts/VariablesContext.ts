import { Dispatch, SetStateAction, createContext } from 'react';

import { TelegramBotVariable } from 'services/api/telegram_bots/types';

export type VariablesContextProps = [TelegramBotVariable[], Dispatch<SetStateAction<TelegramBotVariable[]>>];

const VariablesContext = createContext<VariablesContextProps | undefined>(undefined);

export default VariablesContext;