import React, { ReactElement, useState } from 'react';
import { Params, json, useRouteLoaderData } from 'react-router-dom';

import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';

import Loading from 'components/Loading';
import Pagination from 'components/Pagination';

import TelegramBotUser from './components/TelegramBotUser';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from '../Root';

import { TelegramBotUsersAPI } from 'services/api/telegram_bots/main';
import { APIResponse } from 'services/api/telegram_bots/types';

export interface TelegramBotUsersPaginationData extends Omit<APIResponse.TelegramBotUsersAPI.Get.Pagination, 'next' | 'previous'> {
	limit: number;
	offset: number;
}

export interface LoaderData {
	telegramBotUsersPaginationData: TelegramBotUsersPaginationData;
}

export async function loader({ params }: { params: Params<'telegramBotID'> }): Promise<LoaderData | Response> {
	const telegramBotID: number = parseInt(params.telegramBotID!);
	const [limit, offset] = [20, 0];

	const response = await TelegramBotUsersAPI.get(telegramBotID, limit, offset);

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return {
		telegramBotUsersPaginationData: {
			count: response.json.count,
			limit,
			offset,
			results: response.json.results,
		},
	}
}

function Users(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;
	const { telegramBotUsersPaginationData: initialPaginationData } = useRouteLoaderData('telegram-bot-menu-users') as LoaderData;

	const { createMessageToast } = useToast();

	const [paginationData, setPaginationData] = useState<TelegramBotUsersPaginationData>(initialPaginationData);
	const [loading, setLoading] = useState<boolean>(false);

	async function updateTelegramBotUsers(limit?: number, offset?: number): Promise<void> {
		setLoading(true);

		limit ??= paginationData.limit;
		offset ??= paginationData.offset;

		const response = await TelegramBotUsersAPI.get(telegramBot.id, limit, offset);

		if (response.ok) {
			setPaginationData({
				count: response.json.count,
				limit,
				offset,
				results: response.json.results,
			});
			setLoading(false);
		} else {
			createMessageToast({ message: response.json.message, level: response.json.level });
		}
	}

	return (
		<>
			<Card className='border'>
				<Card.Header as='h5' className='border-bottom text-center'>
					{gettext('Список пользователей')}
				</Card.Header>
				<Card.Body className='vstack gap-2'>
					<Pagination
						itemCount={paginationData.count}
						itemLimit={paginationData.limit}
						itemOffset={paginationData.offset}
						size='sm'
						className='align-self-center'
						onPageChange={offset => updateTelegramBotUsers(undefined, offset)}
					/>
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
										{paginationData.results.map(telegramBotUser => (
											<TelegramBotUser
												key={telegramBotUser.id}
												telegramBotUser={telegramBotUser}
												onDeleted={updateTelegramBotUsers}
											/>
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
				</Card.Body>
			</Card>
		</>
	);
}

export default Users;