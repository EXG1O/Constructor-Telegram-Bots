import React, { ReactElement, useEffect, useState } from 'react';

import { LinkContainer } from 'react-router-bootstrap';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

import Loading from 'components/Loading';
import TelegramBotCard from 'components/TelegramBotCard';

import Header from './components/Header';

import TelegramBotsContext from './services/contexts/TelegramBotsContext';

import useToast from 'services/hooks/useToast';

import { TelegramBotsAPI } from 'services/api/telegram_bots/main';
import { TelegramBot } from 'services/api/telegram_bots/types';

function PersonalCabinet(): ReactElement {
	const { createMessageToast } = useToast();

	const [telegramBots, setTelegramBots] = useState<TelegramBot[]>([]);
	const [loading, setLoading] = useState<boolean>(true);

	useEffect(() => {
		const getTelegramBots = async (): Promise<void> => {
			const response = await TelegramBotsAPI.get();

			if (response.ok) {
				setLoading(false);
				setTelegramBots(response.json);
			} else {
				createMessageToast({
					message: gettext('Не удалось получить список добавленных Telegram ботов!'),
					level: 'danger',
				});
			}

		}

		getTelegramBots();
	}, []);

	return (
		<Container as='main' className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
			<TelegramBotsContext.Provider value={{ telegramBots, setTelegramBots }}>
				<Header />
				{loading ? (
					<Loading size='lg' className='m-auto' />
				) : (
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
							<div className='border rounded text-center px-3 py-2'>
								{gettext('Вы ещё не добавили Telegram бота')}
							</div>
						)}
					</Row>
				)}
			</TelegramBotsContext.Provider>
		</Container>
	);
}

export default PersonalCabinet;