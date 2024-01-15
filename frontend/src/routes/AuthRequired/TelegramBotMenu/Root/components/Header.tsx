import React, { ReactElement } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import './Header.css';

import { LinkContainer } from 'react-router-bootstrap';
import Nav from 'react-bootstrap/Nav';

import { LoaderData as TelegramBotMenuRootLoaderData } from '..';

function Header(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	return (
		<Nav variant='pills' className='nav-fill bg-light border rounded gap-2 p-2' id='telegramBotMenuHeader'>
			<LinkContainer to={`/telegram-bot-menu/${telegramBot.id}/`}>
				<Nav.Link className='link-dark'>{gettext('Telegram бот')}</Nav.Link>
			</LinkContainer>
			<LinkContainer to={`/telegram-bot-menu/${telegramBot.id}/variables/`}>
				<Nav.Link className='link-dark'>{gettext('Переменные')}</Nav.Link>
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