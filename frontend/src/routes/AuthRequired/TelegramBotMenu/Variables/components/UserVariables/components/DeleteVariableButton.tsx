import React, { ReactElement, HTMLAttributes, memo, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';
import classNames from 'classnames';

import AskConfirmModal from 'components/AskConfirmModal';

import useToast from 'services/hooks/useToast';
import useVariables from '../hooks/useVariables';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { VariableAPI } from 'services/api/telegram_bots/main';
import { Variable } from 'services/api/telegram_bots/types';

export interface DeleteVariableButtonProps extends Pick<HTMLAttributes<HTMLElement>, 'className'> {
	variable: Variable;
}

function DeleteVariableButton({ variable, className }: DeleteVariableButtonProps): ReactElement<DeleteVariableButtonProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();
	const { updateVariables } = useVariables();

	const [showModal, setShowModal] = useState<boolean>(false);
	const [loadingModal, setLoadingModal] = useState<boolean>(false);

	const handleConfirmDelete = useCallback(async () => {
		setLoadingModal(true);

		const response = await VariableAPI._delete(telegramBot.id, variable.id);

		if (response.ok) {
			updateVariables();
			setShowModal(false);
			createMessageToast({
				message: gettext('Вы успешно удалили переменную.'),
				level: 'success',
			});
		} else {
			createMessageToast({
				message: gettext('Не удалось удалить переменную!'),
				level: 'error',
			});
		}

		setLoadingModal(false);
	}, []);

	return (
		<>
			<AskConfirmModal
				show={showModal}
				loading={loadingModal}
				title={gettext('Удаление переменной')}
				onConfirm={handleConfirmDelete}
				onHide={useCallback(() => setShowModal(false), [])}
			>
				{gettext('Вы точно хотите удалить переменную?')}
			</AskConfirmModal>
			<i
				className={classNames('d-flex text-danger bi bi-trash', className)}
				style={{ fontSize: '18px', cursor: 'pointer' }}
				onClick={() => setShowModal(true)}
			/>
		</>
	);
}

export default memo(DeleteVariableButton);