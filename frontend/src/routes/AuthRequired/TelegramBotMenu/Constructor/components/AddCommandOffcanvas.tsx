import React, { ReactElement, memo, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Button from 'react-bootstrap/Button';

import CommandOffcanvas, { Data as CommandOffcanvasData } from './CommandOffcanvas';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { CommandsAPI } from 'services/api/telegram_bots/main';

export interface AddCommandOffcanvasProps {
	show: boolean;
	onAdded: () => void;
	onHide: () => void
}

function AddCommandOffcanvas({ onAdded, onHide, ...props }: AddCommandOffcanvasProps): ReactElement<AddCommandOffcanvasProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [loading, setLoading] = useState<boolean>(false);

	async function handleAddCommandButtonClick({
		name,
		settings,
		images,
		files,
		message,
		apiRequest,
		databaseRecord,
		...data
	}: CommandOffcanvasData): Promise<void> {
		setLoading(true);

		const response = await CommandsAPI.create(telegramBot.id, {
			...data,
			name: name ?? '',
			settings: {
				is_reply_to_user_message: settings?.isReplyToUserMessage ?? false,
				is_delete_user_message: settings?.isDeleteUserMessage ?? false,
				is_send_as_new_message: settings?.isSendAsNewMessage ?? false,
			},
			images: images?.map(image => image.file!),
			files: files?.map(file => file.file!),
			message: message ?? { text: '' },
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
					onClick={() => handleAddCommandButtonClick(data)}
				>
					{gettext('Добавить команду')}
				</Button>
			), [])}
		</CommandOffcanvas>
	);
}

export default memo(AddCommandOffcanvas);