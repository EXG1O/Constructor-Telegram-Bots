import React, { ReactElement, memo, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import AskConfirmModal from 'components/AskConfirmModal';

import EditVariableButton from './EditVariableButton';

import useToast from 'services/hooks/useToast';
import useVariables from '../hooks/useVariables';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { VariableAPI } from 'services/api/telegram_bots/main';
import { Variable } from 'services/api/telegram_bots/types';

export interface VariableDisplayProps {
	variable: Variable;
}

function VariableDisplay({ variable }: VariableDisplayProps): ReactElement<VariableDisplayProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();
	const { updateVariables } = useVariables();

	const [showDeletionModal, setShowDeletionModal] = useState<boolean>(false);
	const [loadingDeletionModal, setLoadingDeletionModal] = useState<boolean>(false);

	const handleConfirmDelete = useCallback(async () => {
		setLoadingDeletionModal(true);

		const response = await VariableAPI._delete(telegramBot.id, variable.id);

		if (response.ok) {
			updateVariables();
			setShowDeletionModal(false);
		}

		setLoadingDeletionModal(false);
		createMessageToast({
			message: response.json.message,
			level: response.json.level,
		});
	}, []);

	return(
		<>
			<AskConfirmModal
				show={showDeletionModal}
				loading={loadingDeletionModal}
				title={gettext('Удаление переменной')}
				onConfirm={handleConfirmDelete}
				onHide={useCallback(() => setShowDeletionModal(false), [])}
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
							<EditVariableButton variable={variable} className='my-auto' />
							<i
								className='d-flex text-danger bi bi-trash my-auto'
								style={{ fontSize: '18px', cursor: 'pointer' }}
								onClick={() => setShowDeletionModal(true)}
							/>
						</div>
					</div>
				</td>
			</tr>
		</>
	);
}

export default memo(VariableDisplay);