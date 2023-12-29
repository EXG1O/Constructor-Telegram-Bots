import React, { ReactNode, useCallback, useState } from 'react';
import { NodeProps, Handle, Position, useReactFlow } from 'reactflow';

import Stack from 'react-bootstrap/Stack';
import Button from 'react-bootstrap/Button';
import Image from 'react-bootstrap/Image';

import { NodeData } from './..';

import CommandOffcanvas, { Data } from './../../CommandOffcanvas';
import AskConfirmModal from 'components/AskConfirmModal';

import useTelegramBot from 'services/hooks/useTelegramBot';
import useToast from 'services/hooks/useToast';

import { TelegramBotCommandAPI } from 'services/api/telegram_bots/main';

interface CommandNodeProps extends Omit<NodeProps, 'data'>{
	data: NodeData;
}

function CommandNode({ id, data }: CommandNodeProps): ReactNode {
	const { createMessageToast } = useToast();
	const { telegramBot } = useTelegramBot();

	const { setNodes } = useReactFlow<NodeData>();

	const [showDeleteModal, setShowDeleteModal] = useState<boolean>(false);
	const [showCommandOffcanvas, setShowCommandOffcanvas] = useState<boolean>(false);

	const handleConfirmDeleteButtonClick = useCallback(async (): Promise<void> => {
		const response = await TelegramBotCommandAPI.delete_(telegramBot.id, data.id);

		if (response.ok) {
			setNodes(prevNodes => prevNodes.filter(node => node.id !== id));
			setShowDeleteModal(false);
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}, []);

	async function handleEditCommandButtonClick(commandData: Data): Promise<void> {
		const response = await TelegramBotCommandAPI.update(telegramBot.id, data.id, commandData);

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
				title={gettext('Редактирование команды')}
				onHide={useCallback(() => setShowCommandOffcanvas(false), [])}
			>
				{useCallback((commandData: Data) => (
					<Button
						variant='success'
						className='w-100'
						onClick={() => handleEditCommandButtonClick(commandData)}
					>
						{gettext('Сохранить команду')}
					</Button>
				), [])}
			</CommandOffcanvas>
			<Stack gap={2} style={{ width: '300px' }}>
				<div className='d-flex gap-1'>
					<Button
						size='sm'
						variant='danger'
						className='bi bi-trash px-1 py-0'
						style={{ fontSize: '16px' }}
						onClick={() => setShowDeleteModal(true)}
					/>
					<Button
						size='sm'
						variant='secondary'
						className='bi bi-pencil-square px-1 py-0'
						style={{ fontSize: '16px' }}
						onClick={() => setShowCommandOffcanvas(true)}
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
				{data.image && (
					<Image thumbnail className='p-0' src={data.image} />
				)}
				<div className='bg-light border rounded text-break px-3 py-2'>{data.message_text.text}</div>
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