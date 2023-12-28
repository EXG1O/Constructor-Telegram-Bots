import React, { ReactNode, useRef, useState } from 'react';

import Offcanvas, { OffcanvasProps } from 'react-bootstrap/Offcanvas';
import Button, { ButtonProps } from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';

import CommandName, { Data as CommandNameData } from './components/CommandName';
import Command, { Data as CommandData } from './components/Command';
import Image, { Data as ImageData } from './components/Image';
import MessageText, { Data as MessageTextData } from './components/MessageText';
import Keyboard, { Data as KeyboardData } from './components/keyboard/Main';

import useToast from 'services/hooks/useToast';
import useTelegramBot from 'services/hooks/useTelegramBot';

import { TelegramBotCommandAPI } from 'services/api/telegram_bots/main';

type AddonsName = 'command' | 'image' | 'keyboard';

interface AddonsButtonProps extends Omit<ButtonProps, 'key' | 'size' | 'variant' | 'onClick'> {
	name: AddonsName;
}

export interface Data {
	name: CommandNameData['text'];
	command?: CommandData;
	image?: ImageData['file'];
	message_text: MessageTextData;
	keyboard?: KeyboardData;
}

export interface MainProps extends OffcanvasProps {
	commandID?: number;
	initialData?: Data;
	onUpdateNodes?: () => void;
}

const addonsButton: AddonsButtonProps[] = [
	{ name: 'command', children: gettext('Команда') },
	{ name: 'image', children: gettext('Изображение') },
	{ name: 'keyboard', children: gettext('Клавиатура') },
];

function Main({ commandID, initialData, onUpdateNodes, ...props }: MainProps): ReactNode {
	const { createMessageToast } = useToast();
	const { telegramBot } = useTelegramBot();

	const data = useRef<Data>(initialData ?? { name: '', message_text: { text: '' } });
	const [addons, setAddons] = useState<Record<AddonsName, boolean>>({
		command: Boolean(initialData?.command),
		image: Boolean(initialData?.image),
		keyboard: Boolean(initialData?.keyboard),
	});

	function toggleAddon(name: AddonsName): void {
		setAddons({ ...addons, [name]: !addons[name] });

		if (addons[name]) {
			data.current[name] = undefined;
		}
	}

	async function handleAddCommandButtonClick(): Promise<void> {
		const response = await TelegramBotCommandAPI.create(telegramBot.id, data.current);

		if (response.ok) {
			props.onHide();
			onUpdateNodes?.();
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	async function handleUpdateCommandButtonClick(): Promise<void> {
		const response = await TelegramBotCommandAPI.update(telegramBot.id, commandID!, data.current);

		if (response.ok) {
			props.onHide();
			onUpdateNodes?.();
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<Offcanvas {...props} placement={'end'}>
			<Offcanvas.Header className='border-bottom' closeButton>
				<Offcanvas.Title as='h5'>
					{commandID ? gettext('Редактирование команды') : gettext('Добавление команды')}
				</Offcanvas.Title>
			</Offcanvas.Header>
			<Offcanvas.Body className='vstack gap-3'>
				<CommandName
					initialData={{ text: initialData?.name ?? '' }}
					onChange={commandName => { data.current.name = commandName.text }}
				/>
				{addons.command && (
					<Command
						initialData={initialData?.command}
						onChange={command => { data.current.command = command }}
					/>
				)}
				{addons.image && (
					<Image onChange={image => { data.current.image = image.file }} />
				)}
				<MessageText
					initialData={initialData?.message_text}
					onChange={messageText => { data.current.message_text = messageText }}
				/>
				{addons.keyboard && (
					<Keyboard
						initialData={initialData?.keyboard}
						onChange={keyboard => { data.current.keyboard = keyboard }}
					/>
				)}
				<Stack className='bg-light border rounded p-1' gap={1}>
					{addonsButton.map(({ name, ...props }, index) => (
						<Button
							{...props}
							key={index}
							size='sm'
							variant={addons[name] ? 'secondary' : 'dark'}
							onClick={() => toggleAddon(name)}
						/>
					))}
				</Stack>
			</Offcanvas.Body>
			<Offcanvas.Header className='border-top'>
				<Button
					variant='success'
					className='flex-fill'
					{...commandID ? {
						onClick: handleUpdateCommandButtonClick,
						children: gettext('Редактировать команду'),
					} : {
						onClick: handleAddCommandButtonClick,
						children: gettext('Добавить команду'),
					}}
				/>
			</Offcanvas.Header>
		</Offcanvas>
	);
}

export default Main;