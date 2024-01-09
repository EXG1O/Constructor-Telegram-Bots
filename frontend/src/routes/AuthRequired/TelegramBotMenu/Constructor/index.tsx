import React, { ReactElement, useCallback, useRef, useState } from 'react';
import { useRouteLoaderData } from 'react-router';

import Button from 'react-bootstrap/Button';

import { LoaderData as TelegramBotMenuRootLoaderData } from '../Root';

import CommandOffcanvas, { Data as CommandOffcanvasData } from './components/CommandOffcanvas';
import Diagram from './components/Diagram';

import useToast from 'services/hooks/useToast';

import { TelegramBotCommandAPI } from 'services/api/telegram_bots/main';

export interface UpdateNodesRef {
	updateNodes?: () => void | Promise<void>;
}

function Constructor(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const diagramInnerRef = useRef<UpdateNodesRef>({});
	const [showCommandOffcanvas, setShowCommandOffcanvas] = useState<boolean>(false);

	async function handleAddCommandButtonClick(data: CommandOffcanvasData): Promise<void> {
		const { images, files, messageText, apiRequest, databaseRecord, ...data_ } = data;

		const response = await TelegramBotCommandAPI.create(telegramBot.id, {
			...data_,
			images: images?.map(image => image.file!),
			files: files?.map(file => file.file!),
			message_text: { text: messageText },
			api_request: apiRequest && {
				...apiRequest,
				headers: apiRequest.headers && apiRequest.headers.map(header => ({ [header.key]: header.value })),
				body: apiRequest.body && JSON.parse(apiRequest.body),
			},
			database_record: databaseRecord ? { data: JSON.parse(databaseRecord) } : undefined,
		});

		if (response.ok) {
			diagramInnerRef.current.updateNodes?.();
			setShowCommandOffcanvas(false);
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<>
			<CommandOffcanvas
				show={showCommandOffcanvas}
				title={gettext('Добавление команды')}
				onHide={useCallback(() => setShowCommandOffcanvas(false), [])}
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
			<Diagram
				innerRef={diagramInnerRef}
				onAddCommandClick={useCallback(() => setShowCommandOffcanvas(true), [])}
			/>
		</>
	)
}

export default Constructor;