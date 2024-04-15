import React, { ReactElement, memo, useState, useCallback } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import { useReactFlow } from 'reactflow';
import Button from 'react-bootstrap/Button';

import CommandFormOffcanvas, { Data as CommandFormOffcanvasData } from './CommandFormOffcanvas';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { parseNodes } from '../utils';

import { CommandsAPI, DiagramCommandAPI } from 'services/api/telegram_bots/main';

export interface AddCommandOffcanvasProps {
	show: boolean;
	onHide: () => void
}

function AddCommandOffcanvas({ onHide, ...props }: AddCommandOffcanvasProps): ReactElement<AddCommandOffcanvasProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { addNodes } = useReactFlow();
	const { createMessageToast } = useToast();

	const [loading, setLoading] = useState<boolean>(false);

	async function handleAddCommandButtonClick({
		name,
		settings,
		trigger,
		images,
		files,
		message,
		keyboard,
		apiRequest,
		databaseRecord,
	}: CommandFormOffcanvasData): Promise<void> {
		setLoading(true);

		const commandResponse = await CommandsAPI.create(telegramBot.id, {
			name: name ?? '',
			settings: {
				is_reply_to_user_message: settings?.isReplyToUserMessage ?? false,
				is_delete_user_message: settings?.isDeleteUserMessage ?? false,
				is_send_as_new_message: settings?.isSendAsNewMessage ?? false,
			},
			trigger: trigger ? {
				...trigger,
				description: trigger.description ?? null,
			} : null,
			images: images?.map(image => image.file!),
			files: files?.map(file => file.file!),
			message: message ?? { text: '' },
			keyboard: keyboard ? {
				...keyboard,
				buttons: keyboard.buttons.map(button => ({
					...button,
					row: button.row ?? null,
					url: button.url ?? null,
				})),
			} : null,
			api_request: apiRequest ? {
				...apiRequest,
				headers: apiRequest.headers ? apiRequest.headers.map(header => ({ [header.key]: header.value })) : null,
				body: apiRequest.body ? JSON.parse(apiRequest.body) : null,
			} : null,
			database_record: databaseRecord ? { data: JSON.parse(databaseRecord) } : null,
		});

		if (commandResponse.ok) {
			const diagramCommandResponse = await DiagramCommandAPI.get(telegramBot.id, commandResponse.json.id);

			if (diagramCommandResponse.ok) {
				addNodes(parseNodes([diagramCommandResponse.json]));
				onHide();
				createMessageToast({
					message: gettext('Вы успешно добавили команду.'),
					level: 'success',
				});
			} else {
				createMessageToast({
					message: gettext('Не удалось получить добавленную команду!'),
					level: 'error',
				});
			}
		} else {
			createMessageToast({
				message: gettext('Не удалось добавить команду!'),
				level: 'error',
			});
		}

		setLoading(false);
	}

	return (
		<CommandFormOffcanvas
			{...props}
			loading={loading}
			title={gettext('Добавление команды')}
			onHide={onHide}
		>
			{useCallback((data: CommandFormOffcanvasData) => (
				<Button
					variant='success'
					onClick={() => handleAddCommandButtonClick(data)}
				>
					{gettext('Добавить команду')}
				</Button>
			), [])}
		</CommandFormOffcanvas>
	);
}

export default memo(AddCommandOffcanvas);