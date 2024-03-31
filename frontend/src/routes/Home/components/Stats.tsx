import React, { ReactElement } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import './Stats.scss';

import Stack from 'react-bootstrap/Stack';

import InfoArea from 'components/InfoArea';

import { LoaderData as HomeLoaderData } from '..';

function Stats(): ReactElement {
	const { stats } = useRouteLoaderData('home') as HomeLoaderData;

	return (
		<div className='stats'>
			<h3>{gettext('Информация о сайте')}</h3>
			<Stack gap={1}>
				<InfoArea value={stats.users.total}>
					{gettext('Пользователей')}
				</InfoArea>
				<InfoArea value={stats.telegramBots.telegram_bots.total}>
					{gettext('Добавленных Telegram ботов')}
				</InfoArea>
				<InfoArea value={stats.telegramBots.telegram_bots.enabled}>
					{gettext('Включенных Telegram ботов')}
				</InfoArea>
				<InfoArea value={stats.telegramBots.users.total}>
					{gettext('Пользователей Telegram ботов')}
				</InfoArea>
			</Stack>
		</div>
	);
}

export default Stats;