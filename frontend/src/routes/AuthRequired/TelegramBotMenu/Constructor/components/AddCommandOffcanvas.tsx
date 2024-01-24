import React, { ReactElement, memo, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Button from 'react-bootstrap/Button';

import CommandOffcanvas, { Data as CommandOffcanvasData } from './CommandOffcanvas';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { TelegramBotCommandAPI } from 'services/api/telegram_bots/main';

export interface AddCommandOffcanvasProps {
	show: boolean;
	onAdded: () => void;
	onHide: () => void
}

function AddCommandOffcanvas({ onAdded, onHide, ...props }: AddCommandOffcanvasProps): ReactElement<AddCommandOffcanvasProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [loading, setLoading] = useState<boolean>(false);

	async function handleAddCommandButtonClick(data: CommandOffcanvasData): Promise<void> {
		setLoading(true);

		const { name, settings, images, files, messageText, apiRequest, databaseRecord, ..._data } = data;

		const response = await TelegramBotCommandAPI.create(telegramBot.id, {
			..._data,
			name: name ?? '',
			settings: {
				is_reply_to_user_message: settings?.isReplyToUserMessage ?? false,
				is_delete_user_message: settings?.isDeleteUserMessage ?? false,
				is_send_as_new_message: settings?.isSendAsNewMessage ?? false,
			},
			images: images?.map(image => image.file!),
			files: files?.map(file => file.file!),
			message_text: { text: messageText ?? '' },
			api_request: apiRequest && {
				...apiRequest,
				headers: apiRequest.headers && apiRequest.headers.map(header => ({ [header.key]: header.value })),
				body: apiRequest.body && JSON.parse(apiRequest.body),
			},
			database_record: databaseRecord ? { data: JSON.parse(databaseRecord) } : undefined,
		});

		if (response.ok) {
			onAdded();
			onHide();
		}

		setLoading(false);
		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<CommandOffcanvas
			{...props}
			loading={loading}
			title={gettext('Добавление команды')}
			onHide={onHide}
		>
			{useCallback((data: CommandOffcanvasData) => (
				<Button
					variant='success'
					className='w-100'
					onClick={() => handleAddCommandButtonClick(data)}
				>
					{gettext('Добавить команду')}
				</Button>
			), [])}
		</CommandOffcanvas>
	);
}

export default memo(AddCommandOffcanvas);