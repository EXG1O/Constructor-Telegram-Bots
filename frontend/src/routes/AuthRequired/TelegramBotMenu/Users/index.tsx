import React, { ReactElement, useState } from 'react';
import { Params, useRouteLoaderData } from 'react-router-dom';

import Card from 'react-bootstrap/Card';

import Title from 'components/Title';

import Toolbar from './components/Toolbar';
import UserList from './components/UserList';

import useToast from 'services/hooks/useToast';

import UsersContext from './contexts/UsersContext';

import { LoaderData as TelegramBotMenuRootLoaderData } from '../Root';

import { UsersAPI } from 'services/api/telegram_bots/main';
import { APIResponse } from 'services/api/telegram_bots/types';

export interface PaginationData extends APIResponse.UsersAPI.Get.Pagination {
	limit: number;
	offset: number;
	search: string;
}

export interface LoaderData {
	paginationData: PaginationData;
}

export async function loader({ params }: { params: Params<'telegramBotID'> }): Promise<LoaderData | Response> {
	const telegramBotID: number = parseInt(params.telegramBotID!);
	const [limit, offset] = [20, 0];

	const response = await UsersAPI.get(telegramBotID, limit, offset);

	if (!response.ok) {
		throw Error('Failed to fetch data!');
	}

	return { paginationData: { ...response.json, limit, offset, search: '' } };
}

function Users(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;
	const { paginationData: initialPaginationData } = useRouteLoaderData('telegram-bot-menu-users') as LoaderData;

	const { createMessageToast } = useToast();

	const [paginationData, setPaginationData] = useState<PaginationData>(initialPaginationData);
	const [loading, setLoading] = useState<boolean>(false);

	async function updateUsers(
		limit: number = paginationData.limit,
		offset: number = paginationData.offset,
		search: string = paginationData.search,
	): Promise<void> {
		setLoading(true);

		const response = await UsersAPI.get(telegramBot.id, limit, offset, search);

		if (response.ok) {
			setPaginationData({ ...response.json, limit, offset, search });
		} else {
			createMessageToast({
				message: gettext('Не удалось получить список пользователей!'),
				level: 'error',
			});
		}

		setLoading(false);
	}

	return (
		<Title title={gettext('Пользователи')}>
			<Card>
				<Card.Header as='h5' className='text-center'>
					{gettext('Список пользователей')}
				</Card.Header>
				<Card.Body className='vstack gap-2'>
					<UsersContext.Provider value={{
						users: paginationData.results,
						filter: { search: paginationData.search },
						updateUsers,
					}}>
						<Toolbar paginationData={paginationData} />
						<UserList loading={loading} />
					</UsersContext.Provider>
				</Card.Body>
			</Card>
		</Title>
	);
}

export default Users;