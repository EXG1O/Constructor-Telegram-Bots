import React, { ReactElement, memo, useCallback, useEffect, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Button from 'react-bootstrap/Button';

import CommandOffcanvas, { Data as CommandOffcanvasData } from './CommandOffcanvas';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { TelegramBotCommandAPI } from 'services/api/telegram_bots/main';

export interface AddCommandOffcanvasProps {
	show: boolean;
	commandID: number;
	onUpdated: () => void;
	onHide: () => void
}

function UpdateCommandOffcanvas({ show, commandID, onUpdated, onHide }: AddCommandOffcanvasProps): ReactElement<AddCommandOffcanvasProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [initialData, setInitialData] = useState<CommandOffcanvasData | undefined>(undefined);
	const [loading, setLoading] = useState<boolean>(true);

	useEffect(() => { show && updateInitialData() }, [show]);

	async function updateInitialData(): Promise<void> {
		setLoading(true);

		const response = await TelegramBotCommandAPI.get(telegramBot.id, commandID);

		if (response.ok) {
			const { id, name, settings, images, files, command, message_text, keyboard, api_request, database_record } = response.json;

			const newInitialData: CommandOffcanvasData = {
				name,
				settings: {
					isReplyToUserMessage: settings.is_reply_to_user_message,
					isDeleteUserMessage: settings.is_delete_user_message,
					isSendAsNewMessage: settings.is_send_as_new_message,
				},
				images: images.length ? images : undefined,
				files: files.length ? files : undefined,
				command: command ? {
					text: command.text,
					description: command.description ?? undefined,
				} : undefined,
				messageText: message_text.text,
				keyboard: keyboard ? {
					type: keyboard.type,
					buttons: keyboard.buttons.map(button => ({
						id: button.id,
						row: button.row ?? undefined,
						text: button.text,
						url: button.url ?? undefined,
					})),
				} : undefined,
				apiRequest: api_request ? {
					url: api_request.url,
					method: api_request.method,
					headers: api_request.headers ? Object.entries(api_request.headers).map(([key, value]) => ({ key, value })) : undefined,
					body: api_request.body ? JSON.stringify(api_request.body, undefined, 4) : undefined,
				} : undefined,
				databaseRecord: database_record ? JSON.stringify(database_record.data, undefined, 4) : undefined,
			}

			setInitialData(newInitialData);
			setLoading(false);
		} else {
			createMessageToast({
				message: gettext('Не удалось получить данные с сервера!'),
				level: 'error',
			});
		}
	}

	async function handleSaveCommandButtonClick(commandOffcanvasData: CommandOffcanvasData): Promise<void> {
		setLoading(true);

		const { name, settings, images, files, messageText, apiRequest, databaseRecord, ...data_ } = commandOffcanvasData;

		const response = await TelegramBotCommandAPI.update(telegramBot.id, commandID, {
			...data_,
			name: name ?? '',
			settings: {
				is_reply_to_user_message: settings?.isReplyToUserMessage ?? false,
				is_delete_user_message: settings?.isDeleteUserMessage ?? false,
				is_send_as_new_message: settings?.isSendAsNewMessage ?? false,
			},
			message_text: { text: messageText ?? '' },
			images: images?.map(image => image.file ?? image.id!),
			files: files?.map(file => file.file ?? file.id!),
			api_request: apiRequest && {
				...apiRequest,
				headers: apiRequest.headers && apiRequest.headers.map(header => ({ [header.key]: header.value })),
				body: apiRequest.body && JSON.parse(apiRequest.body),
			},
			database_record: databaseRecord ? { data: JSON.parse(databaseRecord) } : undefined,
		});

		if (response.ok) {
			onUpdated();
			onHide();
		}

		setLoading(false);
		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<CommandOffcanvas
			show={show}
			loading={loading}
			title={gettext('Редактирование команды')}
			initialData={initialData}
			onHide={onHide}
		>
			{useCallback((commandOffcanvasData: CommandOffcanvasData) => (
				<Button
					variant='success'
					className='w-100'
					onClick={() => handleSaveCommandButtonClick(commandOffcanvasData)}
				>
					{gettext('Сохранить команду')}
				</Button>
			), [])}
		</CommandOffcanvas>
	);
}

export default memo(UpdateCommandOffcanvas);