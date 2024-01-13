import React, { ReactElement, memo, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Modal, { ModalProps } from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

import BaseVariableModal, { Data as BaseVariableModalData } from './BaseVariableModal';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import useToast from 'services/hooks/useToast';

import { TelegramBotVariableAPI } from 'services/api/telegram_bots/main';
import { TelegramBotVariable } from 'services/api/telegram_bots/types';

export interface CreateVariableModalProps extends ModalProps {
	onCreate: (variable: TelegramBotVariable) => void;
}

function CreateVariableModal({ onCreate , ...props }: CreateVariableModalProps): ReactElement<CreateVariableModalProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [loading, setLoading] = useState<boolean>(false);

	async function handleCreateButtonClick(data: BaseVariableModalData): Promise<void> {
		setLoading(true);

		const response = await TelegramBotVariableAPI.create(telegramBot.id, data);

		if (response.ok) {
			onCreate(response.json.telegram_bot_variable);
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
				<Modal.Footer>
					<Button
						variant='success'
						className='w-100'
						onClick={() => handleCreateButtonClick(data)}
					>
						{gettext('Создать')}
					</Button>
				</Modal.Footer>
			)}
		</BaseVariableModal>
	);
}

export default memo(CreateVariableModal);