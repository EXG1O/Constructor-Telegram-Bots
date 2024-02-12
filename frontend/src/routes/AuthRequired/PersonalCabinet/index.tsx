import React, { ReactElement, useState } from 'react';
import { Link, json, useRouteLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import TelegramBotCard from 'components/TelegramBotCard';

import Header from './components/Header';

import TelegramBotsContext from './services/contexts/TelegramBotsContext';

import { TelegramBotsAPI } from 'services/api/telegram_bots/main';
import { TelegramBot, APIResponse } from 'services/api/telegram_bots/types';
import Title from 'components/Title';

export interface LoaderData {
	telegramBots: APIResponse.TelegramBotsAPI.Get;
}

export async function loader(): Promise<LoaderData> {
	const response = await TelegramBotsAPI.get();

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return { telegramBots: response.json };
}

function PersonalCabinet(): ReactElement {
	const { telegramBots: initialTelegramBots } = useRouteLoaderData('personal-cabinet') as LoaderData;

	const [telegramBots, setTelegramBots] = useState<TelegramBot[]>(initialTelegramBots);

	return (
		<Title title={gettext('Личный кабинет')}>
			<Container as='main' className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
				<TelegramBotsContext.Provider value={[telegramBots, setTelegramBots]}>
					<Header />
					<Row xs={1} md={2} xl={3} className='g-3'>
						{telegramBots.length ? (
							telegramBots.map(telegramBot => (
								<TelegramBotCard key={telegramBot.id} telegramBot={telegramBot}>
									{() => (
										<Link
											to={`/telegram-bot-menu/${telegramBot.id}/`}
											className='card-footer btn btn-light border border-top-0'
										>
											{gettext('Меню Telegram бота')}
										</Link>
									)}
								</TelegramBotCard>
							))
						) : (
							<div className='border rounded text-center px-3 py-2'>
								{gettext('Вы ещё не добавили Telegram бота')}
							</div>
						)}
					</Row>
				</TelegramBotsContext.Provider>
			</Container>
		</Title>
	);
}

export default PersonalCabinet;