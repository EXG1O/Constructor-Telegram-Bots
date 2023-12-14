import React, { ReactNode } from 'react';

import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

import useTelegramBot from 'services/hooks/useTelegramBot';

function TelegramBotCardFooter(): ReactNode {
	const { telegramBot, setTelegramBot } = useTelegramBot();

	return (
		<Card.Footer className='d-flex flex-wrap border border-top-0 p-3 gap-3'>
			{!telegramBot.is_running && telegramBot.is_stopped ? (
				<Button
					variant='success'
					className='flex-fill'
				>
					{gettext('Включить Telegram бота')}
				</Button>
			) : (
				<Button
					variant='danger'
					className='flex-fill'
				>
					{gettext('Выключить Telegram бота')}
				</Button>
			)}
			<Button
				variant='danger'
				className='flex-fill'
			>
				{gettext('Удалить Telegram бота')}
			</Button>
		</Card.Footer>
	);
}

export default TelegramBotCardFooter;