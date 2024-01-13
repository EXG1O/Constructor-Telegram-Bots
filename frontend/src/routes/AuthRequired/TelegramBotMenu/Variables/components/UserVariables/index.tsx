import React, { ReactElement, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Table from 'react-bootstrap/Table';

import Loading from 'components/Loading';

import CreateVariableModal from './components/CreateVariableModal';

import { LoaderData as TelegramBotMenuVariablesLoaderData } from '../..';

import { TelegramBotVariable } from 'services/api/telegram_bots/types';

function UserVariables(): ReactElement {
	const { telegramBotVariables } = useRouteLoaderData('telegram-bot-menu-variables') as TelegramBotMenuVariablesLoaderData;

	const [variables, setVariables] = useState<TelegramBotVariable[]>(telegramBotVariables);
	const [showCreateVariableModal, setShowCreateVariableModal] = useState<boolean>(false);
	const [loading, setLoading] = useState<boolean>(false);

	const handleCreateVariable = useCallback((variable: TelegramBotVariable): void => {
		setShowCreateVariableModal(false);
		setVariables([...variables, variable]);
	}, [variables]);

	return (
		<>
			<CreateVariableModal
				show={showCreateVariableModal}
				onCreate={handleCreateVariable}
				onHide={useCallback(() => setShowCreateVariableModal(false), [])}
			/>
			<Card className='border'>
				<Card.Header as='h5' className='border-bottom text-center'>
					{gettext('Пользовательские переменные')}
				</Card.Header>
				<Card.Body className='vstack gap-2'>
					{loading ? (
						<Loading size='md' className='align-self-center' />
					) : (
						<>
							<div>
								<Button
									size='sm'
									variant='dark'
									onClick={() => setShowCreateVariableModal(true)}
								>
									<i className='bi bi-plus-lg me-1' style={{ WebkitTextStroke: '1px' }} />
									{gettext('Добавить переменную')}
								</Button>
							</div>
							{variables.length ? (
								<div className='border rounded'>
									<Table responsive borderless striped className='overflow-hidden rounded mb-0'>
										<tbody>
											{variables.map(variable => (
												<tr key={variable.id}>
													<td>
														<div className='d-flex gap-2'>
															<i
																className='btn-clipboard bi bi-clipboard'
																data-clipboard-text={`{{ ${variable.name} }}`}
																style={{ cursor: 'pointer' }}
															/>
															<span className='flex-fill text-info-emphasis'>
																{variable.name}
															</span>
														</div>
													</td>
													<td className='text-nowrap'>
														{variable.description}
													</td>
													<td>
														<div className='d-flex justify-content-end gap-2'>
															<i
																className='d-flex text-secondary bi bi-pencil-square'
																style={{ fontSize: '18px', cursor: 'pointer' }}
															/>
															<i
																className='d-flex text-danger bi bi-trash'
																style={{ fontSize: '19px', cursor: 'pointer' }}
															/>
														</div>
													</td>
												</tr>
											))}
										</tbody>
									</Table>
								</div>
							) : (
								<div className='border rounded text-center px-3 py-2'>
									{gettext('Вы ещё не добавили переменные своему Telegram боту.')}
								</div>
							)}
						</>
					)}
				</Card.Body>
			</Card>
		</>
	);
}

export default UserVariables;