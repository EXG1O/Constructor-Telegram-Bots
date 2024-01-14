import React, { ReactElement, memo, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import { ModalProps } from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

import BaseVariableModal, { Data as BaseVariableModalData } from './BaseVariableModal';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import useToast from 'services/hooks/useToast';
import useVariables from '../services/hooks/useVariables';

import { TelegramBotVariableAPI } from 'services/api/telegram_bots/main';

function CreateVariableModal(props: ModalProps): ReactElement<ModalProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();
	const [variables, setVariables] = useVariables();

	const [loading, setLoading] = useState<boolean>(false);

	async function handleCreateButtonClick(data: BaseVariableModalData): Promise<void> {
		setLoading(true);

		const response = await TelegramBotVariableAPI.create(telegramBot.id, data);

		if (response.ok) {
			setVariables([...variables, response.json.telegram_bot_variable]);
			props.onHide?.();
		}

		setLoading(false);
		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<BaseVariableModal
			{...props}
			loading={loading}
			title={gettext('Создание переменной')}
		>
			{data => (
				<Button
					variant='success'
					className='w-100'
					onClick={() => handleCreateButtonClick(data)}
				>
					{gettext('Создать')}
				</Button>
			)}
		</BaseVariableModal>
	);
}

export default memo(CreateVariableModal);