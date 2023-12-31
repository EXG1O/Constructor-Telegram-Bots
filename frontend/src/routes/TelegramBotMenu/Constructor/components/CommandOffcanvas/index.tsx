import React, { ReactElement, ReactNode, memo, useRef, useState } from 'react';

import Offcanvas, { OffcanvasProps } from 'react-bootstrap/Offcanvas';
import Button, { ButtonProps } from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';
import Collapse from 'react-bootstrap/Collapse';

import CommandName, { Data as CommandNameData } from './components/CommandName';
import Command, { Data as CommandData } from './components/Command';
import Image, { Data as ImageData } from './components/Image';
import MessageText, { Data as MessageTextData } from './components/MessageText';
import Keyboard, { Data as KeyboardData } from './components/Keyboard';

type AddonsName = 'command' | 'image' | 'keyboard';

interface AddonsButtonProps extends Omit<ButtonProps, 'key' | 'size' | 'variant' | 'onClick'> {
	name: AddonsName;
}

export interface Data {
	name: CommandNameData['text'];
	command?: CommandData | null;
	image?: ImageData['file'] | null;
	message_text: MessageTextData;
	keyboard?: KeyboardData | null;
}

export interface CommandOffcanvasProps extends Omit<OffcanvasProps, 'children'> {
	title: ReactNode;
	initialData?: Data;
	children?: (data: Data) => ReactNode;
}

const addonsButton: AddonsButtonProps[] = [
	{ name: 'command', children: gettext('Команда') },
	{ name: 'image', children: gettext('Изображение') },
	{ name: 'keyboard', children: gettext('Клавиатура') },
];

function CommandOffcanvas({ title, initialData, children, ...props }: CommandOffcanvasProps): ReactElement<CommandOffcanvasProps> {
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

	return (
		<Offcanvas {...props}>
			<Offcanvas.Header className='border-bottom' closeButton>
				<Offcanvas.Title as='h5'>{title}</Offcanvas.Title>
			</Offcanvas.Header>
			<Offcanvas.Body>
				<CommandName
					className='mb-3'
					initialData={{ text: initialData?.name ?? '' }}
					onChange={commandName => { data.current.name = commandName.text }}
				/>
				<Collapse in={addons.command} unmountOnExit>
					<div id='command-offcanvas-command-addon'>
						<Command
							className='mb-3'
							initialData={initialData?.command}
							onChange={command => { data.current.command = command }}
						/>
					</div>
				</Collapse>
				<Collapse in={addons.image} unmountOnExit>
					<div id='command-offcanvas-image-addon'>
						<Image
							className='mb-3'
							onChange={image => { data.current.image = image.file }}
						/>
					</div>
				</Collapse>
				<MessageText
					className='mb-3'
					initialData={initialData?.message_text}
					onChange={messageText => { data.current.message_text = messageText }}
				/>
				<Collapse in={addons.keyboard} unmountOnExit>
					<div id='command-offcanvas-keyboard-addon'>
						<Keyboard
							className='mb-3'
							initialData={initialData?.keyboard}
							onChange={keyboard => { data.current.keyboard = keyboard }}
						/>
					</div>
				</Collapse>
				<Stack className='bg-light border rounded p-1' gap={1}>
					{addonsButton.map(({ name, ...props }, index) => (
						<Button
							{...props}
							key={index}
							size='sm'
							variant={addons[name] ? 'secondary' : 'dark'}
							aria-controls={`command-offcanvas-${name}-addon`}
							aria-expanded={addons[name]}
							onClick={() => toggleAddon(name)}
						/>
					))}
				</Stack>
			</Offcanvas.Body>
			<Offcanvas.Header className='border-top'>
				{children?.(data.current)}
			</Offcanvas.Header>
		</Offcanvas>
	);
}

export default memo(CommandOffcanvas);