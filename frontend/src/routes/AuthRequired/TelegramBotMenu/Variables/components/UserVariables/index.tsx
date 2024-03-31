import React, { ReactElement, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Card from 'react-bootstrap/Card';

import Loading from 'components/Loading';

import Toolbar from './components/Toolbar';
import VariableList from './components/VariableList';

import VariablesContext from './contexts/VariablesContext';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';
import { LoaderData as TelegramBotMenuVariablesLoaderData, UserVariablesPaginationData } from '../..';

import { VariablesAPI } from 'services/api/telegram_bots/main';

interface PaginationData extends UserVariablesPaginationData {
	search: string;
}

function UserVariables(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;
	const { userVariablesPaginationData: initialPaginationData } = useRouteLoaderData('telegram-bot-menu-variables') as TelegramBotMenuVariablesLoaderData;

	const { createMessageToast } = useToast();

	const [paginationData, setPaginationData] = useState<PaginationData>({ ...initialPaginationData, search: '' });
	const [loading, setLoading] = useState<boolean>(false);

	async function updateVariables(
		limit: number = paginationData.limit,
		offset: number = paginationData.offset,
		search: string = paginationData.search,
	): Promise<void> {
		setLoading(true);

		const response = await VariablesAPI.get(telegramBot.id, limit, offset, search);

		if (response.ok) {
			setPaginationData({ ...response.json, limit, offset, search });
		} else {
			createMessageToast({
				message: gettext('Не удалось получить список переменных!'),
				level: 'error',
			});
		}

		setLoading(false);
	}

	return (
		<Card>
			<Card.Header as='h5' className='text-center'>
				{gettext('Пользовательские переменные')}
			</Card.Header>
			<Card.Body className='vstack gap-2'>
				<VariablesContext.Provider value={{ variables: paginationData.results, updateVariables }}>
					<Toolbar paginationData={paginationData} />
					{!loading ? (
						<VariableList />
					) : (
						<div className='d-flex justify-content-center border rounded p-3'>
							<Loading size='md' />
						</div>
					)}
				</VariablesContext.Provider>
			</Card.Body>
		</Card>
	);
}

export default UserVariables;