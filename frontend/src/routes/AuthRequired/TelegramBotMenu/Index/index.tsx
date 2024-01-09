import 'chart.js/auto';

import React, { ReactElement } from 'react';
import { useRouteLoaderData } from 'react-router';

import { Line } from 'react-chartjs-2';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Stack from 'react-bootstrap/Stack';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';
import ToggleButton from 'react-bootstrap/ToggleButton';

import TelegramBotCard from 'components/TelegramBotCard';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import TelegramBotCardFooter from './components/TelegramBotCardFooter';

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
			<Col xs={12} lg={6}>
				<Stack gap={2}>
					<h3 className='text-center mb-0'>{gettext('Статистика пользователей')}</h3>
					<ToggleButtonGroup type='radio' name='types' defaultValue='all'>
						{[
							{
								value: 'all',
								text: gettext('Все'),
							},
							{
								value: 'unique',
								text: gettext('Уникальные'),
							},
							{
								value: 'regular',
								text: gettext('Постоянные'),
							},
						].map((data, index) => (
							<ToggleButton
								key={index}
								id={`btn-radio-type-${data.value}`}
								size='sm'
								variant={`outline-dark ${index === 1 ? 'w-50' : 'w-25'}`}
								value={data.value}
							>
								{data.text}
							</ToggleButton>
						))}
					</ToggleButtonGroup>
					<ToggleButtonGroup type='radio' name='options' defaultValue={0}>
						{[gettext('Сегодня'), gettext('Последние 7 дней'), gettext('Этот месяц'), gettext('Этот год')].map((value, index) => (
							<ToggleButton
								key={index}
								id={`tbg-radio-${index}`}
								size='sm'
								variant='outline-dark w-25'
								value={index}
							>
								{value}
							</ToggleButton>
						))}
					</ToggleButtonGroup>
					<Line
						data={{
							datasets: [{
								data: Array.from(Array(30).keys()).map(date => ({ x: `${date}.12.2023`, y: Math.floor(Math.random() * 100) })),
								borderColor: '#212529',
								fill: true,
								tension: 0.1,
							}],
						}}
						options={{
							plugins: {
								legend: {
									display: false,
								},
								tooltip: {
									displayColors: false,
									bodyAlign: 'center',
								},
							},
						}}
					/>
				</Stack>
			</Col>
		</Row>
	);
}

export default Index;