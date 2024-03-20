import React, { ReactElement, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import AskConfirmModal from 'components/AskConfirmModal';

import VariableEditModal, { VariableEditModalProps } from './VariableEditModal';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import useToast from 'services/hooks/useToast';

import { VariableAPI } from 'services/api/telegram_bots/main';
import { Variable } from 'services/api/telegram_bots/types';

export interface VariableDisplayProps extends Pick<VariableEditModalProps, 'onUpdated'> {
	variable: Variable;
	onDeleted: () => void;
}

function VariableDisplay({ variable, onUpdated, onDeleted }: VariableDisplayProps): ReactElement<VariableDisplayProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [showVariableEditModal, setShowVariableEditModal] = useState<boolean>(false);
	const [showVariableDeletionModal, setShowVariableDeletionModal] = useState<boolean>(false);

	const handleConfirmDelete = useCallback(async () => {
		const response = await VariableAPI._delete(telegramBot.id, variable.id);

		if (response.ok) {
			onDeleted();
			setShowVariableDeletionModal(false);
		}

		createMessageToast({
			message: response.json.message,
			level: response.json.level,
		});
	}, []);

	return(
		<>
			<VariableEditModal
				variable={variable}
				show={showVariableEditModal}
				onUpdated={onUpdated}
				onHide={useCallback(() => setShowVariableEditModal(false), [])}
			/>
			<AskConfirmModal
				show={showVariableDeletionModal}
				title={gettext('Удаление переменной')}
				onConfirm={handleConfirmDelete}
				onHide={useCallback(() => setShowVariableDeletionModal(false), [])}
			>
				{gettext('Вы точно хотите удалить переменную?')}
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
						<div className='d-flex gap-1'>
							<i
								className='d-flex text-secondary bi bi-pencil-square my-auto'
								style={{ fontSize: '18px', cursor: 'pointer' }}
								onClick={() => setShowVariableEditModal(true)}
							/>
							<i
								className='d-flex text-danger bi bi-trash my-auto'
								style={{ fontSize: '18px', cursor: 'pointer' }}
								onClick={() => setShowVariableDeletionModal(true)}
							/>
						</div>
					</div>
				</td>
			</tr>
		</>
	);
}

export default VariableDisplay;