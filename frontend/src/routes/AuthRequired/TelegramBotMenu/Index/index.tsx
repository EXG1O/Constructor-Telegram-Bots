import React, { ReactElement } from 'react';
import { Params, json, useRouteLoaderData } from 'react-router-dom';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import TelegramBotCard from 'components/TelegramBotCard';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import TelegramBotCardFooter from './components/TelegramBotCardFooter';
import TelegramBotUsersChartStats from './components/TelegramBotUsersChartStats';

import { TelegramBotUsersStatsAPI } from 'services/api/telegram_bots/main';
import { TelegramBotUsersStats } from 'services/api/telegram_bots/types';

interface CustomTelegramBotUsersStats {
	type: 'all';
	daysInterval: TelegramBotUsersStats['days_interval'];
	regular: TelegramBotUsersStats['results'];
	unique: TelegramBotUsersStats['results'];
}

export interface LoaderData {
	telegramBotUsersStats: CustomTelegramBotUsersStats;
}

export async function loader({ params }: { params: Params<'telegramBotID'> }): Promise<LoaderData | Response> {
	const { telegramBotID } = params;

	const response = await TelegramBotUsersStatsAPI.get(parseInt(telegramBotID!), 'regular');
	const _response = await TelegramBotUsersStatsAPI.get(parseInt(telegramBotID!), 'unique');

	if (!response.ok || !_response.ok) {
		throw json(
			{
				message: gettext('Не удалось получить статистику пользователей!'),
				level: 'danger',
			},
			{ status: response.status },
		);
	}

	return {
		telegramBotUsersStats: {
			type: 'all',
			daysInterval: 1,
			regular: response.json.results,
			unique: response.json.results,
		},
	}
}

function Index(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	return (
		<Row className='g-3 g-lg-4'>
			<Col xs={12} lg={6}>
				<TelegramBotCard telegramBot={telegramBot}>
					{props => (
						<TelegramBotCardFooter {...props} />
					)}
				</TelegramBotCard>
			</Col>
			<Col xs={12} lg={6} />
			<Col xs={12} lg={6}>
				<TelegramBotUsersChartStats />
			</Col>
		</Row>
	);
}

export default Index;