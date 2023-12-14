import React, { ReactNode, useEffect, useState } from 'react';
import { Params, useLocation, useNavigate, useParams } from 'react-router-dom';

import Spinner from 'react-bootstrap/Spinner';

import TelegramBotContext from 'services/contexts/TelegramBotContext';

import { TelegramBotAPI } from 'services/api/telegram_bots/main';
import { TelegramBot } from 'services/api/telegram_bots/types';

export interface TelegramBotProviderProps {
	children: ReactNode
}

function TelegramBotProvider({ children }: TelegramBotProviderProps): ReactNode {
	const { telegramBotID } = useParams<Params<'telegramBotID'>>();
	const navigate = useNavigate();

	if (telegramBotID !== undefined) {
		const location = useLocation();

		const [telegramBot, setTelegramBot] = useState<TelegramBot | undefined>(undefined);

		useEffect(() => {
			const getTelegramBot = async (): Promise<void> => {
				const response = await TelegramBotAPI.get(Number.parseInt(telegramBotID));

				if (response.ok) {
					setTelegramBot(response.json);
				} else {
					navigate('/personal-cabinet/');
				}
			}

			getTelegramBot();
		}, [location]);

		return telegramBot === undefined ? (
			<Spinner
				animation='border'
				className='m-auto'
				style={{
					width: '4rem',
					height: '4rem',
					borderWidth: '0.5rem',
				}}
			/>
		) : (
			<TelegramBotContext.Provider value={{ telegramBot, setTelegramBot }}>
				{children}
			</TelegramBotContext.Provider>
		);
	} else {
		navigate('/personal-cabinet/');
	}
}

export default TelegramBotProvider;