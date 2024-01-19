import React, { ReactElement, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Table from 'react-bootstrap/Table';

import Loading from 'components/Loading';
import Pagination from 'components/Pagination';

import CreateVariableModal from './components/CreateVariableModal';
import Variable from './components/Variable';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuVariablesLoaderData, UserVariablesPaginationData } from '../..';
import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { TelegramBotVariablesAPI } from 'services/api/telegram_bots/main';

function UserVariables(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;
	const { userVariablesPaginationData: initialPaginationData } = useRouteLoaderData('telegram-bot-menu-variables') as TelegramBotMenuVariablesLoaderData;

	const { createMessageToast } = useToast();

	const [paginationData, setPaginationData] = useState<UserVariablesPaginationData>(initialPaginationData);
	const [showCreateVariableModal, setShowCreateVariableModal] = useState<boolean>(false);
	const [loading, setLoading] = useState<boolean>(false);

	async function updateVariables(limit?: number, offset?: number): Promise<void> {
		setLoading(true);

		limit ??= paginationData.limit;
		offset ??= paginationData.offset;

		const response = await TelegramBotVariablesAPI.get(telegramBot.id, limit, offset);

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
			<CreateVariableModal
				show={showCreateVariableModal}
				onCreated={updateVariables}
				onHide={useCallback(() => setShowCreateVariableModal(false), [])}
			/>
			<Card className='border'>
				<Card.Header as='h5' className='border-bottom text-center'>
					{gettext('Пользовательские переменные')}
				</Card.Header>
				<Card.Body className='vstack gap-2'>
					<div className='d-flex flex-wrap justify-content-between gap-2'>
						<Button
							size='sm'
							variant='dark'
							onClick={() => setShowCreateVariableModal(true)}
						>
							<i
								className='bi bi-plus-lg me-1'
								style={{ WebkitTextStroke: '1px' }}
							/>
							{gettext('Добавить переменную')}
						</Button>
						<Pagination
							count={paginationData.count}
							limit={paginationData.limit}
							offset={paginationData.offset}
							size='sm'
							className='justify-content-center'
							onPageChange={offset => updateVariables(undefined, offset)}
						/>
					</div>
					{!loading ? (
						paginationData.count ? (
							<div className='border rounded'>
								<Table
									responsive
									striped
									borderless
									className='overflow-hidden align-middle rounded mb-0'
								>
									<tbody>
										{paginationData.results.map((variable, index) => (
											<Variable
												key={variable.id}
												index={index}
												variable={variable}
												onUpdated={updateVariables}
												onDeleted={updateVariables}
											/>
										))}
									</tbody>
								</Table>
							</div>
						) : (
							<div className='border rounded text-center px-3 py-2'>
								{gettext('Вы ещё не добавили переменные своему Telegram боту.')}
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

export default UserVariables;