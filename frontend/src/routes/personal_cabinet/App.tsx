import React, { ReactNode, useState } from 'react';
import { useLoaderData } from 'react-router-dom';

import { LinkContainer } from 'react-router-bootstrap';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

import Header from './components/Header';
import TelegramBotCard from 'components/TelegramBotCard';

import TelegramBotsContext from './services/contexts/TelegramBotsContext';

import AuthRequiredProvider from 'services/providers/AuthRequiredProvider';

import { TelegramBotsAPI } from 'services/api/telegram_bots/main';
import { TelegramBot } from 'services/api/telegram_bots/types';

export interface LoaderData {
	telegramBots: TelegramBot[];
}

export async function loader(): Promise<LoaderData> {
	const response = await TelegramBotsAPI.get();

	return { telegramBots: response.ok ? response.json : [] };
}

function App(): ReactNode {
	const { telegramBots: telegramBotsInit } = useLoaderData() as LoaderData;

	const [telegramBots, setTelegramBots] = useState<TelegramBot[]>(telegramBotsInit);

	return (
		<AuthRequiredProvider>
			<main className='mb-auto'>
				<Container className='d-flex flex-column gap-3 gap-lg-4 my-3 my-lg-4'>
					<TelegramBotsContext.Provider value={{telegramBots, setTelegramBots}}>
						<Header />
						<Row xs={1} md={2} xl={3} className='g-3'>
							{telegramBots.length ? (
								telegramBots.map(telegramBot => (
									<TelegramBotCard key={telegramBot.id} telegramBot={telegramBot}>
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
									</TelegramBotCard>
								))
							) : (
								<div className='border rounded text-center p-3'>
									{gettext('Вы ещё не добавили Telegram бота')}
								</div>
							)}
						</Row>
					</TelegramBotsContext.Provider>
				</Container>
			</main>
		</AuthRequiredProvider>
	);
}

export default App;