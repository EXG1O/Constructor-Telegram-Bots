import React, { ReactElement, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Table from 'react-bootstrap/Table';

import Loading from 'components/Loading';
import AddButton from 'components/AddButton';
import Pagination from 'components/Pagination';

import VariableAdditionModal from './components/VariableAdditionModal';
import VariableDisplay from './components/VariableDisplay';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';
import { LoaderData as TelegramBotMenuVariablesLoaderData, UserVariablesPaginationData } from '../..';

import { VariablesAPI } from 'services/api/telegram_bots/main';

function UserVariables(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;
	const { userVariablesPaginationData: initialPaginationData } = useRouteLoaderData('telegram-bot-menu-variables') as TelegramBotMenuVariablesLoaderData;

	const { createMessageToast } = useToast();

	const [paginationData, setPaginationData] = useState<UserVariablesPaginationData>(initialPaginationData);
	const [showVariableAdditionModal, setShowVariableAdditionModal] = useState<boolean>(false);
	const [loading, setLoading] = useState<boolean>(false);

	async function updateVariables(
		limit: number = paginationData.limit,
		offset: number = paginationData.offset,
	): Promise<void> {
		setLoading(true);

		const response = await VariablesAPI.get(telegramBot.id, limit, offset);

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
			<VariableAdditionModal
				show={showVariableAdditionModal}
				onCreated={updateVariables}
				onHide={useCallback(() => setShowVariableAdditionModal(false), [])}
			/>
			<Card>
				<Card.Header as='h5' className='text-center'>
					{gettext('Пользовательские переменные')}
				</Card.Header>
				<Card.Body className='vstack gap-2'>
					<div className='d-flex flex-wrap justify-content-between gap-2'>
						<AddButton
							size='sm'
							variant='dark'
							onClick={useCallback(() => setShowVariableAdditionModal(true), [])}
						>
							{gettext('Добавить переменную')}
						</AddButton>
						<Pagination
							itemCount={paginationData.count}
							itemLimit={paginationData.limit}
							itemOffset={paginationData.offset}
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
										{paginationData.results.map(variable => (
											<VariableDisplay
												key={variable.id}
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
								{gettext('Вы ещё не добавили переменные')}
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