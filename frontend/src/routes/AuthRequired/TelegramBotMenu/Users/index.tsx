import React, { ReactElement, useState } from 'react';
import { Params, useRouteLoaderData } from 'react-router-dom';

import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';

import Title from 'components/Title';
import Loading from 'components/Loading';

import Toolbar from './components/Toolbar';
import UserDisplay from './components/UserDisplay';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from '../Root';

import { UsersAPI } from 'services/api/telegram_bots/main';
import { APIResponse } from 'services/api/telegram_bots/types';
import UsersContext from './contexts/UsersContext';

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
					<UsersContext.Provider value={{ users: paginationData.results, updateUsers }}>
						<Toolbar paginationData={paginationData} />
						{!loading ? (
							paginationData.count ? (
								<div className='border rounded'>
									<Table
										responsive
										striped
										borderless
										className='overflow-hidden align-middle text-nowrap rounded mb-0'
									>
										<tbody>
											{paginationData.results.map(user => (
												<UserDisplay key={user.id} user={user} />
											))}
										</tbody>
									</Table>
								</div>
							) : (
								<div className='border rounded text-center px-3 py-2'>
									{gettext('Вашего Telegram бота ещё никто не активировал')}
								</div>
							)
						) : (
							<div className='d-flex justify-content-center border rounded p-3'>
								<Loading size='md' />
							</div>
						)}
					</UsersContext.Provider>
				</Card.Body>
			</Card>
		</Title>
	);
}

export default Users;