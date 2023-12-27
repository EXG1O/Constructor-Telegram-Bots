import './Header.css';

import React, { ReactNode } from 'react';

import { LinkContainer } from 'react-router-bootstrap';
import Nav from 'react-bootstrap/Nav';

import useTelegramBot from 'services/hooks/useTelegramBot';

function Header(): ReactNode {
	const { telegramBot } = useTelegramBot();

	return (
		<Nav variant='pills' className='nav-fill bg-light border rounded gap-2 p-2' id='telegramBotMenuHeader'>
			<LinkContainer to={`/telegram-bot-menu/${telegramBot.id}/`}>
				<Nav.Link className='link-dark'>{gettext('Telegram бот')}</Nav.Link>
			</LinkContainer>
			<LinkContainer to={`/telegram-bot-menu/${telegramBot.id}/variables/`}>
				<Nav.Link className='link-dark'>{gettext('Список переменных')}</Nav.Link>
			</LinkContainer>
			<LinkContainer to={`/telegram-bot-menu/${telegramBot.id}/users/`}>
				<Nav.Link className='link-dark'>{gettext('Пользователи')}</Nav.Link>
			</LinkContainer>
			<LinkContainer to={`/telegram-bot-menu/${telegramBot.id}/constructor/`}>
				<Nav.Link className='link-dark'>{gettext('Конструктор')}</Nav.Link>
			</LinkContainer>
		</Nav>
	);
}

export default Header;