import React, { ReactElement, memo, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Button from 'react-bootstrap/Button';

import VariableModal, { VariableModalProps, Data as BaseVariableModalData } from './VariableModal';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import useToast from 'services/hooks/useToast';

import { TelegramBotVariableAPI } from 'services/api/telegram_bots/main';
import { TelegramBotVariable } from 'services/api/telegram_bots/types';

export interface UpdateVariableModalProps extends Pick<VariableModalProps, 'show' | 'onHide'> {
	variable: TelegramBotVariable;
	onUpdated: () => void;
}

function UpdateVariableModal({ variable, onUpdated, onHide, ...props }: UpdateVariableModalProps): ReactElement<UpdateVariableModalProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [loading, setLoading] = useState<boolean>(false);

	async function handleSaveButtonClick(data: BaseVariableModalData): Promise<void> {
		setLoading(true);

		const response = await TelegramBotVariableAPI.update(telegramBot.id, variable.id, data);

		if (response.ok) {
			onUpdated();
			onHide();
		}

		setLoading(false);
		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<VariableModal
			{...props}
			loading={loading}
			initialData={variable}
			title={gettext('Редактирование переменной')}
			onHide={onHide}
		>
			{data => (
				<Button
					variant='success'
					onClick={() => handleSaveButtonClick(data)}
				>
					{gettext('Сохранить')}
				</Button>
			)}
		</VariableModal>
	);
}

export default memo(UpdateVariableModal);