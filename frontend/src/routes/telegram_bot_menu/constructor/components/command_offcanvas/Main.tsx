import React, { ReactNode, useState } from 'react';

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

export interface Data {
	name: CommandNameData['text'];
	command?: CommandData;
	image?: ImageData['image'];
	message_text: MessageTextData;
	keyboard?: KeyboardData;
}

type AddonsName = 'command' | 'image' | 'keyboard';

interface AddonsButtonProps extends Omit<ButtonProps, 'key' | 'size' | 'variant' | 'onClick'> {
	name: AddonsName;
}

const addonsButton: AddonsButtonProps[] = [
	{ name: 'command', children: gettext('Команда') },
	{ name: 'image', children: gettext('Изображение') },
	{ name: 'keyboard', children: gettext('Клавиатура') },
];

function Main(props: OffcanvasProps): ReactNode {
	const { createMessageToast } = useToast();
	const { telegramBot } = useTelegramBot();

	const [data, setData] = useState<Data>({ name: '', message_text: { text: '' } });
	const [addons, setAddons] = useState<Record<AddonsName, boolean>>({
		command: false,
		image: false,
		keyboard: false,
	});

	function toggleAddon(name: AddonsName): void {
		setAddons({ ...addons, [name]: !addons[name] });

		if (addons[name]) {
			setData({ ...data, [name]: undefined });
		}
	}

	async function handleAddCommandButtonClick() {
		const data_ = { ...data };
		delete data_.image;

		const response = await TelegramBotCommandAPI.create(telegramBot.id, { data: data_, image: data.image });

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<Offcanvas {...props} placement={'end'}>
			<Offcanvas.Header className='border-bottom' closeButton>
				<Offcanvas.Title as='h5'>{gettext('Добавление команды')}</Offcanvas.Title>
			</Offcanvas.Header>
			<Offcanvas.Body>
				<Stack gap={3}>
					<CommandName onChange={data_ => setData({ ...data, name: data_.text })} />
					{addons.command && (
						<Command onChange={data_ => setData({ ...data, command: data_ })} />
					)}
					{addons.image && (
						<Image onChange={data_ => setData({ ...data, image: data_.image })} />
					)}
					<MessageText onChange={data_ => setData({ ...data, message_text: data_ })} />
					{addons.keyboard && (
						<Keyboard onChange={data_ => setData({ ...data, keyboard: data_ })} />
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
				</Stack>
			</Offcanvas.Body>
			<Offcanvas.Header className='border-top'>
				<Button
					variant='success'
					className='flex-fill'
					onClick={handleAddCommandButtonClick}
				>
					{gettext('Добавить команду')}
				</Button>
			</Offcanvas.Header>
		</Offcanvas>
	);
}

export default Main;