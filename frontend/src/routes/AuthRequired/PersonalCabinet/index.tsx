import React, { ReactElement, useState } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import { LinkContainer } from 'react-router-bootstrap';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

import TelegramBotCard from 'components/TelegramBotCard';

import Header from './components/Header';

import TelegramBotsContext from './services/contexts/TelegramBotsContext';

import { TelegramBotsAPI } from 'services/api/telegram_bots/main';
import { TelegramBot } from 'services/api/telegram_bots/types';

export interface LoaderData {
	telegramBots: TelegramBot[]
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
		<Container as='main' className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
			<TelegramBotsContext.Provider value={{ telegramBots, setTelegramBots }}>
				<Header />
				<Row xs={1} md={2} xl={3} className='g-3'>
					{telegramBots.length ? (
						telegramBots.map(telegramBot => (
							<TelegramBotCard key={telegramBot.id} telegramBot={telegramBot}>
								{() => (
									<Card.Footer className='border-0 p-0'>
										<LinkContainer to={`/telegram-bot-menu/${telegramBot.id}/`}>
											<Button
												as='a'
												variant='light'
												className=' border border-top-0 rounded-top-0 w-100 px-3 py-2'
											>
												{gettext('Меню Telegram бота')}
											</Button>
										</LinkContainer>
									</Card.Footer>
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
	);
}

export default PersonalCabinet;