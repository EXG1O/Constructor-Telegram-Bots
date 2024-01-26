import React, { ReactElement, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router';
import { NodeProps, Handle, Position, useReactFlow } from 'reactflow';
import _ from 'lodash';

import Stack from 'react-bootstrap/Stack';
import Button from 'react-bootstrap/Button';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { NodeData } from './..';

import AskConfirmModal from 'components/AskConfirmModal';

import useToast from 'services/hooks/useToast';

import { TelegramBotCommandAPI } from 'services/api/telegram_bots/main';
import UpdateCommandOffcanvas from './UpdateCommandOffcanvas';

interface CommandNodeProps extends Omit<NodeProps, 'data'>{
	data: NodeData;
}

function CommandNode({ id, data }: CommandNodeProps): ReactElement<CommandNodeProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const { setNodes } = useReactFlow<NodeData>();

	const [showDeleteModal, setShowDeleteModal] = useState<boolean>(false);
	const [showUpdateOffcanvas, setShowUpdateOffcanvas] = useState<boolean>(false);

	const handleConfirmDelete = useCallback(async (): Promise<void> => {
		const response = await TelegramBotCommandAPI._delete(telegramBot.id, data.id);

		if (response.ok) {
			setNodes(prevNodes => prevNodes.filter(node => node.id !== id));
			setShowDeleteModal(false);
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}, []);

	return (
		<>
			<AskConfirmModal
				show={showDeleteModal}
				title={gettext('Удаление команды')}
				onHide={useCallback(() => setShowDeleteModal(false), [])}
				onConfirm={handleConfirmDelete}
			>
				{gettext('Вы точно хотите удалить команду Telegram бота?')}
			</AskConfirmModal>
			<UpdateCommandOffcanvas
				show={showUpdateOffcanvas}
				commandID={data.id}
				onUpdated={data.updateNodes}
				onHide={() => setShowUpdateOffcanvas(false)}
			/>
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
						onClick={() => setShowUpdateOffcanvas(true)}
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
					className='message-text-block bg-light border rounded text-break px-3 py-2'
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