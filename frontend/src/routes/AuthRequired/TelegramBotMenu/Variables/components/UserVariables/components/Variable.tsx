import React, { ReactElement, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import AskConfirmModal from 'components/AskConfirmModal';

import UpdateVariableModal from './UpdateVariableModal';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import useToast from 'services/hooks/useToast';
import useVariables from '../services/hooks/useVariables';

import { TelegramBotVariableAPI } from 'services/api/telegram_bots/main';
import { TelegramBotVariable } from 'services/api/telegram_bots/types';

export interface VariableProps {
	index: number;
	variable: TelegramBotVariable;
}

function Variable({ index, variable }: VariableProps): ReactElement<VariableProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();
	const [variables, setVariables] = useVariables();

	const [showUpdateVariableModal, setShowUpdateVariableModal] = useState<boolean>(false);
	const [showDeleteVariableModal, setShowDeleteVariableModal] = useState<boolean>(false);

	const handleDeleteButtonClick = useCallback(async () => {
		const response = await TelegramBotVariableAPI._delete(telegramBot.id, variable.id);

		if (response.ok) {
			const _variables = [...variables];
			_variables.splice(index, 1);
			setVariables(_variables);
			setShowDeleteVariableModal(false);
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}, [variables]);

	return(
		<>
			<UpdateVariableModal
				index={index}
				variable={variable}
				show={showUpdateVariableModal}
				onHide={useCallback(() => setShowUpdateVariableModal(false), [])}
			/>
			<AskConfirmModal
				show={showDeleteVariableModal}
				title={gettext('Удаление переменной')}
				onConfirmButtonClick={handleDeleteButtonClick}
				onHide={useCallback(() => setShowDeleteVariableModal(false), [])}
			>
				{gettext('Вы точно хотите удалить переменную Telegram бота?')}
			</AskConfirmModal>
			<tr>
				<td className='w-50'>
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
				<td>
					<div className='d-flex gap-2'>
						<span className='flex-fill text-nowrap'>
							{variable.description}
						</span>
						<i
							className='d-flex text-secondary bi bi-pencil-square my-auto'
							style={{ fontSize: '18px', cursor: 'pointer' }}
							onClick={() => setShowUpdateVariableModal(true)}
						/>
						<i
							className='d-flex text-danger bi bi-trash my-auto'
							style={{ fontSize: '19px', cursor: 'pointer' }}
							onClick={() => setShowDeleteVariableModal(true)}
						/>
					</div>
				</td>
			</tr>
		</>
	);
}

export default Variable;