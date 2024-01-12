import React, { ReactElement, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router';
import { NodeProps, Handle, Position, useReactFlow } from 'reactflow';
import _ from 'lodash';

import Stack from 'react-bootstrap/Stack';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/Image';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { NodeData } from './..';

import CommandOffcanvas, { Data as CommandOffcanvasData } from './../../CommandOffcanvas';
import AskConfirmModal from 'components/AskConfirmModal';

import useToast from 'services/hooks/useToast';

import { TelegramBotCommandAPI } from 'services/api/telegram_bots/main';

interface CommandNodeProps extends Omit<NodeProps, 'data'>{
	data: NodeData;
}

function CommandNode({ id, data }: CommandNodeProps): ReactElement<CommandNodeProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const { setNodes } = useReactFlow<NodeData>();

	const [showDeleteModal, setShowDeleteModal] = useState<boolean>(false);
	const [showCommandOffcanvas, setShowCommandOffcanvas] = useState<boolean>(false);
	const [loadingCommandOffcanvas, setLoadingCommandOffcanvas] = useState<boolean>(true);
	const [commandOffcanvasInitialData, setCommandOffcanvasInitialData] = useState<CommandOffcanvasData | undefined>(undefined);

	const handleConfirmDeleteButtonClick = useCallback(async (): Promise<void> => {
		const response = await TelegramBotCommandAPI._delete(telegramBot.id, data.id);

		if (response.ok) {
			setNodes(prevNodes => prevNodes.filter(node => node.id !== id));
			setShowDeleteModal(false);
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}, []);

	const handleEditCommandButtonClick = useCallback(async (): Promise<void> => {
		setLoadingCommandOffcanvas(true);
		setShowCommandOffcanvas(true);

		const response = await TelegramBotCommandAPI.get(telegramBot.id, data.id);

		if (response.ok) {
			const { id, name, settings, images, files, command, message_text, keyboard, api_request, database_record } = response.json;

			const initialData: CommandOffcanvasData = {
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
					headers: (
						api_request.headers &&
						Object.keys(api_request.headers).map(key => ({
							key,
							value: api_request.headers![key],
						}))
					) ?? undefined,
					body: (
						api_request.body &&
						JSON.stringify(api_request.body, undefined, 4)
					) ?? undefined,
				} : undefined,
				databaseRecord: (
					database_record &&
					JSON.stringify(database_record, undefined, 4)
				) ?? undefined,
			}

			if (!_.isEqual(initialData, commandOffcanvasInitialData)) {
				setCommandOffcanvasInitialData(initialData);
			}

			setLoadingCommandOffcanvas(false);
		} else {
			createMessageToast({
				message: interpolate(
					(
						gettext('Не удалось получить данные команды %(name)s!') +
						gettext('Попробуйте перезагрузить страницу.')
					),
					{ name: data.name },
					true,
				),
				level: 'danger',
			});
		}
	}, [commandOffcanvasInitialData]);

	async function handleSaveCommandButtonClick(commandOffcanvasData: CommandOffcanvasData): Promise<void> {
		const { name, settings, images, files, messageText, apiRequest, databaseRecord, ...data_ } = commandOffcanvasData;

		const response = await TelegramBotCommandAPI.update(telegramBot.id, data.id, {
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
			database_record: databaseRecord !== undefined ? { data: JSON.parse(databaseRecord) } : undefined,
		});

		if (response.ok) {
			data.updateNodes();
			setShowCommandOffcanvas(false);
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<>
			<AskConfirmModal
				show={showDeleteModal}
				title={gettext('Удаление команды')}
				onHide={useCallback(() => setShowDeleteModal(false), [])}
				onConfirmButtonClick={handleConfirmDeleteButtonClick}
			>
				{gettext('Вы точно хотите удалить команду Telegram бота?')}
			</AskConfirmModal>
			<CommandOffcanvas
				show={showCommandOffcanvas}
				loading={loadingCommandOffcanvas}
				title={gettext('Редактирование команды')}
				initialData={commandOffcanvasInitialData}
				onHide={useCallback(() => setShowCommandOffcanvas(false), [])}
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
			<Stack gap={2} style={{ width: '300px' }}>
				<div className='d-flex gap-1'>
					<Button
						as='i'
						size='sm'
						variant='danger'
						className='bi bi-trash d-flex justify-content-center align-items-center p-1'
						style={{ fontSize: '16px' }}
						onClick={() => setShowDeleteModal(true)}
					/>
					<Button
						as='i'
						size='sm'
						variant='secondary'
						className='bi bi-pencil-square d-flex justify-content-center align-items-center p-1'
						style={{ fontSize: '16px' }}
						onClick={handleEditCommandButtonClick}
					/>
				</div>
				<div className='bg-light border rounded text-break text-center px-3 py-2' style={{ position: 'relative' }}>
					<Handle
						id={`${data.id}:left:0`}
						type='target'
						position={Position.Left}
					/>
					{data.name}
					<Handle
						id={`${data.id}:right:0`}
						type='target'
						position={Position.Right}
					/>
				</div>
				<div
					className='bg-light border rounded text-break px-3 py-2'
					dangerouslySetInnerHTML={{ __html: data.message_text.text }}
				/>
				{data.keyboard?.buttons && (
					<Stack gap={1}>
						{data.keyboard.buttons.map(button => (
							<div
								key={button.id}
								className='text-bg-dark rounded text-break text-center px-3 py-2'
								style={{ position: 'relative' }}
							>
								<Handle
									id={`${data.id}:left:${button.id}`}
									type='source'
									position={Position.Left}
								/>
								{button.text}
								<Handle
									id={`${data.id}:right:${button.id}`}
									type='source'
									position={Position.Right}
								/>
							</div>
						))}
					</Stack>
				)}
			</Stack>
		</>
	);
}

export default CommandNode;