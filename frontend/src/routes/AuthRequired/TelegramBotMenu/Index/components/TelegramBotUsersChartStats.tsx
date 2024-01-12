import 'chart.js/auto';

import React, { ReactElement, useRef, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';
import { ChartJSOrUndefined } from 'react-chartjs-2/dist/types';

import { Line } from 'react-chartjs-2';
import Stack from 'react-bootstrap/Stack';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';
import ToggleButton, { ToggleButtonProps } from 'react-bootstrap/ToggleButton';
import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import Loading from 'components/Loading';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';
import { LoaderData as TelegramBotMenuIndexLoaderData } from '..';

import useToast from 'services/hooks/useToast';

import { TelegramBotUsersStatsAPI } from 'services/api/telegram_bots/main';

type StatsTypes = 'all' | 'unique' | 'regular';

interface StatsConfig {
	type: StatsTypes;
	daysInterval: number;
}

interface ChartData {
	x: string,
	y: number,
}

interface StatsTypeToggleButtonProps extends Omit<ToggleButtonProps, 'key' | 'id' | 'value' | 'size' | 'variant' | 'onChange'> {
	value: StatsTypes;
}

const statsTypeToggleButtons: StatsTypeToggleButtonProps[] = [
	{ value: 'all', children: gettext('Все') },
	{ value: 'regular', children: gettext('Постоянные') },
	{ value: 'unique', children: gettext('Уникальные') },
];

function TelegramBotUsersChartStats(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;
	const { telegramBotUsersStats } = useRouteLoaderData('telegram-bot-menu-index') as TelegramBotMenuIndexLoaderData;

	const { createMessageToast } = useToast();

	const statsConfig = useRef<StatsConfig>({
		type: telegramBotUsersStats.type,
		daysInterval: telegramBotUsersStats.daysInterval,
	});

	const chartRef = useRef<ChartJSOrUndefined<'line', ChartData[], undefined> | undefined>(undefined);
	const [chartData, setChartData] = useState<ChartData[][]>([
		telegramBotUsersStats.regular.map(data => ({ x: data.date, y: data.count })),
		telegramBotUsersStats.unique.map(data => ({ x: data.date, y: data.count })),
	]);

	const [daysIntervalInputValue, setDaysIntervalInputValue] = useState<string>(statsConfig.current.daysInterval.toString());
	const [loading, setLoading] = useState<boolean>(false);

	async function updateChartData(type?: StatsTypes, daysInterval?: number): Promise<void> {
		type ??= statsConfig.current.type;
		daysInterval ??= statsConfig.current.daysInterval;

		if (type !== statsConfig.current.type || daysInterval !== statsConfig.current.daysInterval) {
			setLoading(true);

			if (type === 'all') {
				const response = await TelegramBotUsersStatsAPI.get(telegramBot.id, 'regular', daysInterval);
				const _response = await TelegramBotUsersStatsAPI.get(telegramBot.id, 'unique', daysInterval);

				if (response.ok && _response.ok) {
					statsConfig.current = {
						type: 'all',
						daysInterval: response.json.days_interval,
					};
					setChartData([
						response.json.results.map(data => ({ x: data.date, y: data.count })),
						_response.json.results.map(data => ({ x: data.date, y: data.count })),
					]);
					setLoading(false);
				} else {
					createMessageToast({
						message: gettext('Не удалось получить статистику пользователей!'),
						level: 'danger',
					});
				}
			} else {
				const response = await TelegramBotUsersStatsAPI.get(telegramBot.id, type, daysInterval);

				if (response.ok) {
					statsConfig.current = {
						type: response.json.type,
						daysInterval: response.json.days_interval,
					};
					setChartData([response.json.results.map(data => ({ x: data.date, y: data.count }))]);
					setLoading(false);
				} else {
					createMessageToast({
						message: gettext('Не удалось получить статистику пользователей!'),
						level: 'danger',
					});
				}
			}
		}
	}

	return (
		<Stack gap={2} className='h-100'>
			<h3 className='text-center mb-0'>{gettext('Статистика пользователей')}</h3>
			<ToggleButtonGroup type='radio' name='telegram-bot-users-stats-types' defaultValue='all'>
				{statsTypeToggleButtons.map((props, index) => (
					<ToggleButton
						{...props}
						key={index}
						id={`btn-radio-telegram-bot-users-stats-type-${props.value}`}
						size='sm'
						variant='outline-dark'
						style={{ width: '33.33%' }}
						onClick={() => updateChartData(props.value)}
					/>
				))}
			</ToggleButtonGroup>
			<Stack direction='horizontal' gap={2}>
				<InputGroup size='sm'>
					<InputGroup.Text>{gettext('Интервал дней')}</InputGroup.Text>
					<Form.Control
						value={daysIntervalInputValue}
						type='number'
						min={1}
						max={30}
						onChange={e => setDaysIntervalInputValue(e.target.value)}
					/>
				</InputGroup>
				<Button
					size='sm'
					variant='dark'
					onClick={() => updateChartData(undefined, parseInt(daysIntervalInputValue))}
				>
					{gettext('Обновить')}
				</Button>
			</Stack>
			{loading ? (
				<div
					className='d-flex justify-content-center align-items-center'
					style={{
						width: chartRef.current?.width,
						height: chartRef.current?.height,
					}}
				>
					<Loading size='md' />
				</div>
			) : (
				<Line
					ref={chartRef}
					data={{
						datasets: chartData.map((data, index) => ({
							data,
							borderColor: index === 0 ? '#212529' : '#34383B',
							fill: true,
							tension: 0.1
						}))
					}}
					options={{
						plugins: {
							legend: { display: false },
							tooltip: {
								displayColors: false,
								bodyAlign: 'center',
							},
						},
						scales: {
							x: {
								ticks: { display: false },
								grid: { display: false },
							},
							y: {
								border: { display: false },
								ticks: { display: false },
								grid: { display: false },
							},
						},
					}}
				/>
			)}
		</Stack>
	);
}

export default TelegramBotUsersChartStats;