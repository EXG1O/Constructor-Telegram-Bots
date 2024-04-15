import React, { ReactElement, memo, useCallback, useEffect, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Button from 'react-bootstrap/Button';

import CommandFormOffcanvas, { Data as CommandFormOffcanvasData } from './CommandFormOffcanvas';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { CommandAPI } from 'services/api/telegram_bots/main';

export interface CommandEditOffcanvasProps {
	show: boolean;
	commandID: number;
	onUpdated: () => void;
	onHide: () => void
}

function CommandEditOffcanvas({ show, commandID, onUpdated, onHide }: CommandEditOffcanvasProps): ReactElement<CommandEditOffcanvasProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [initialData, setInitialData] = useState<CommandFormOffcanvasData | undefined>(undefined);
	const [loading, setLoading] = useState<boolean>(true);

	useEffect(() => { show && updateInitialData() }, [show]);

	async function updateInitialData(): Promise<void> {
		setLoading(true);

		const response = await CommandAPI.get(telegramBot.id, commandID);

		if (response.ok) {
			const {
				id,
				name,
				settings,
				images,
				files,
				trigger,
				message,
				keyboard,
				api_request,
				database_record,
			} = response.json;

			setInitialData({
				name,
				settings: {
					isReplyToUserMessage: settings.is_reply_to_user_message,
					isDeleteUserMessage: settings.is_delete_user_message,
					isSendAsNewMessage: settings.is_send_as_new_message,
				},
				images: images.length ? images.map(image => ({ ...image, key: crypto.randomUUID() })) : undefined,
				files: files.length ? files.map(file => ({ ...file, key: crypto.randomUUID() })) : undefined,
				trigger: trigger ? {
					text: trigger.text,
					description: trigger.description ?? undefined,
				} : undefined,
				message,
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
			});
			setLoading(false);
		} else {
			createMessageToast({
				message: gettext('Не удалось получить данные команды!'),
				level: 'error',
			});
		}
	}

	async function handleSaveCommandButtonClick({
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

		const response = await CommandAPI.update(telegramBot.id, commandID, {
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
			images: images?.map(image => image.file ?? image.id!),
			files: files?.map(file => file.file ?? file.id!),
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

		if (response.ok) {
			onUpdated();
			onHide();
			createMessageToast({
				message: gettext('Вы успешно сохранили команду.'),
				level: 'success',
			});
		} else {
			createMessageToast({
				message: gettext('Не удалось сохранить команду!'),
				level: 'error',
			});
		}

		setLoading(false);
	}

	return (
		<CommandFormOffcanvas
			show={show}
			loading={loading}
			title={gettext('Редактирование команды')}
			initialData={initialData}
			onHide={onHide}
		>
			{useCallback((commandOffcanvasData: CommandFormOffcanvasData) => (
				<Button
					variant='success'
					onClick={() => handleSaveCommandButtonClick(commandOffcanvasData)}
				>
					{gettext('Сохранить команду')}
				</Button>
			), [])}
		</CommandFormOffcanvas>
	);
}

export default memo(CommandEditOffcanvas);