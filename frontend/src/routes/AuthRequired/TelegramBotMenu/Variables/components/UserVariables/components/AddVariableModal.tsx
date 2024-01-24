import React, { ReactElement, memo, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Button from 'react-bootstrap/Button';

import VariableModal, { VariableModalProps, Data as BaseVariableModalData } from './VariableModal';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { TelegramBotVariableAPI } from 'services/api/telegram_bots/main';

export interface AddVariableModalProps extends Pick<VariableModalProps, 'show' | 'onHide'> {
	onCreated: () => void;
}

function AddVariableModal({ onCreated, onHide, ...props }: AddVariableModalProps): ReactElement<AddVariableModalProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [loading, setLoading] = useState<boolean>(false);

	async function handleCreateButtonClick(data: BaseVariableModalData): Promise<void> {
		setLoading(true);

		const response = await TelegramBotVariableAPI.create(telegramBot.id, data);

		if (response.ok) {
			onCreated();
			onHide();
		}

		setLoading(false);
		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<VariableModal
			{...props}
			loading={loading}
			title={gettext('Добавление переменной')}
			onHide={onHide}
		>
			{data => (
				<Button
					variant='success'
					className='w-100'
					onClick={() => handleCreateButtonClick(data)}
				>
					{gettext('Добавить')}
				</Button>
			)}
		</VariableModal>
	);
}

export default memo(AddVariableModal);