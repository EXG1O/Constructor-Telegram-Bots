import React, { ReactElement, memo, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import { ModalProps } from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

import BaseVariableModal, { Data as BaseVariableModalData } from './BaseVariableModal';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import useToast from 'services/hooks/useToast';
import useVariables from '../services/hooks/useVariables';

import { TelegramBotVariableAPI } from 'services/api/telegram_bots/main';
import { TelegramBotVariable } from 'services/api/telegram_bots/types';

export interface UpdateVariableModal extends ModalProps {
	index: number;
	variable: TelegramBotVariable;
}

function UpdateVariableModal({ index, variable, ...props }: UpdateVariableModal): ReactElement<UpdateVariableModal> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();
	const [variables, setVariables] = useVariables();

	const [loading, setLoading] = useState<boolean>(false);

	async function handleSaveButtonClick(data: BaseVariableModalData): Promise<void> {
		setLoading(true);

		const response = await TelegramBotVariableAPI.update(telegramBot.id, variable.id, data);

		if (response.ok) {
			const _variables = [...variables];
			_variables.splice(index, 1, response.json.telegram_bot_variable);
			setVariables(_variables);
			props.onHide?.();
		}

		setLoading(false);
		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<BaseVariableModal
			{...props}
			loading={loading}
			initialData={variable}
			title={gettext('Редактирование переменной')}
		>
			{data => (
				<Button
					variant='success'
					className='w-100'
					onClick={() => handleSaveButtonClick(data)}
				>
					{gettext('Сохранить')}
				</Button>
			)}
		</BaseVariableModal>
	);
}

export default memo(UpdateVariableModal);