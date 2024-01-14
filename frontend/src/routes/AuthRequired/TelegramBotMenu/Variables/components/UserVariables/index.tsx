import React, { ReactElement, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Table from 'react-bootstrap/Table';

import CreateVariableModal from './components/CreateVariableModal';
import Variable from './components/Variable';

import VariablesContext from './services/contexts/VariablesContext';

import { LoaderData as TelegramBotMenuVariablesLoaderData } from '../..';

import { TelegramBotVariable } from 'services/api/telegram_bots/types';

function UserVariables(): ReactElement {
	const { telegramBotVariables } = useRouteLoaderData('telegram-bot-menu-variables') as TelegramBotMenuVariablesLoaderData;

	const [variables, setVariables] = useState<TelegramBotVariable[]>(telegramBotVariables);
	const [showCreateVariableModal, setShowCreateVariableModal] = useState<boolean>(false);

	return (
		<VariablesContext.Provider value={[variables, setVariables]}>
			<CreateVariableModal
				show={showCreateVariableModal}
				onHide={useCallback(() => setShowCreateVariableModal(false), [])}
			/>
			<Card className='border'>
				<Card.Header as='h5' className='border-bottom text-center'>
					{gettext('Пользовательские переменные')}
				</Card.Header>
				<Card.Body className='vstack gap-2'>
					<div>
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
					</div>
					{variables.length ? (
						<div className='border rounded'>
							<Table
								responsive
								striped
								borderless
								className='overflow-hidden align-middle rounded mb-0'
							>
								<tbody>
									{variables.map((variable, index) => (
										<Variable
											key={variable.id}
											index={index}
											variable={variable}
										/>
									))}
								</tbody>
							</Table>
						</div>
					) : (
						<div className='border rounded text-center px-3 py-2'>
							{gettext('Вы ещё не добавили переменные своему Telegram боту.')}
						</div>
					)}
				</Card.Body>
			</Card>
		</VariablesContext.Provider>
	);
}

export default UserVariables;