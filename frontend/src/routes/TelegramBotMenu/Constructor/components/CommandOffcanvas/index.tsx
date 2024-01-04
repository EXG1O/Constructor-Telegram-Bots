import React, { ReactElement, ReactNode, memo, useCallback, useMemo, useRef, useState } from 'react';

import Offcanvas, { OffcanvasProps } from 'react-bootstrap/Offcanvas';
import Button, { ButtonProps } from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';
import Collapse from 'react-bootstrap/Collapse';

import CommandName from './components/CommandName';
import Command, { Data as CommandData } from './components/Command';
import Images, { Data as ImagesData } from './components/Images';
import MessageText from './components/MessageText';
import Keyboard, { Data as KeyboardData } from './components/Keyboard';
import Files, { Data as FilesData } from './components/Files';
import APIRequest, { Data as APIRequestData } from './components/APIRequest';
import DatabaseRecord from './components/DatabaseRecord';

export interface Data {
	name: string;
	command?: CommandData | null;
	images?: ImagesData['files'];
	files?: FilesData['files'],
	message_text: string;
	keyboard?: KeyboardData | null;
	api_request?: APIRequestData | null;
	database_record?: string | null;
}

export interface CommandOffcanvasProps extends Omit<OffcanvasProps, 'children'> {
	title: ReactNode;
	initialData?: Data;
	children?: (data: Data) => ReactNode;
}

type AddonNames = 'command' | 'images' | 'files' | 'keyboard' | 'api_request' | 'database_record';

interface AddonButtonsProps extends Omit<ButtonProps, 'key' | 'size' | 'variant' | 'onClick'> {
	name: AddonNames;
}

const addonButtons: AddonButtonsProps[] = [
	{ name: 'command', children: gettext('Команда') },
	{ name: 'images', children: gettext('Изображения') },
	{ name: 'files', children: gettext('Файлы') },
	{ name: 'keyboard', children: gettext('Клавиатура') },
	{ name: 'api_request', children: gettext('API-запрос') },
	{ name: 'database_record', children: gettext('Запись в базу данных') },
];

function CommandOffcanvas({ title, initialData, children, ...props }: CommandOffcanvasProps): ReactElement<CommandOffcanvasProps> {
	const data = useRef<Data>(initialData ?? { name: '', message_text: '' });

	const [showAddons, setShowAddons] = useState<Record<AddonNames, boolean>>({
		command: Boolean(initialData?.command),
		images: Boolean(initialData?.images),
		files: Boolean(initialData?.files),
		keyboard: Boolean(initialData?.keyboard),
		api_request: Boolean(initialData?.api_request),
		database_record: Boolean(initialData?.database_record),
	});
	const [showAddonButtons, setShowAddonButtons] = useState<boolean>(true);

	function toggleAddon(name: AddonNames): void {
		setShowAddons({ ...showAddons, [name]: !showAddons[name] });

		if (showAddons[name]) {
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
					initialValue={initialData?.name}
					onChange={useCallback(commandName => { data.current.name = commandName }, [])}
				/>
				<Collapse in={showAddons.command} unmountOnExit>
					<div id='command-offcanvas-command-addon'>
						<Command
							className='mb-3'
							initialData={initialData?.command}
							onChange={useCallback(command => { data.current.command = command }, [])}
						/>
					</div>
				</Collapse>
				<Collapse in={showAddons.images} unmountOnExit>
					<div id='command-offcanvas-image-addon'>
						<Images
							className='mb-3'
							initialData={useMemo(() => ({ files: data.current.images }), [])}
							onChange={useCallback(images => { data.current.images = images.files }, [])}
						/>
					</div>
				</Collapse>
				<Collapse in={showAddons.files} unmountOnExit>
					<div id='command-offcanvas-files-addon'>
						<Files
							className='mb-3'
							initialData={useMemo(() => ({ files: data.current.files }), [])}
							onChange={useCallback(files => { data.current.files = files.files }, [])}
						/>
					</div>
				</Collapse>
				<MessageText
					className='mb-3'
					initialValue={initialData?.message_text}
					onChange={useCallback(messageText => { data.current.message_text = messageText }, [])}
				/>
				<Collapse in={showAddons.keyboard} unmountOnExit>
					<div id='command-offcanvas-keyboard-addon'>
						<Keyboard
							className='mb-3'
							initialData={initialData?.keyboard}
							onChange={useCallback(keyboard => { data.current.keyboard = keyboard }, [])}
						/>
					</div>
				</Collapse>
				<Collapse in={showAddons.api_request} unmountOnExit>
					<div id='command-offcanvas-api_request-addon'>
						<APIRequest
							className='mb-3'
							initialData={initialData?.api_request}
							onChange={useCallback(apiRequest => { data.current.api_request = apiRequest }, [])}
						/>
					</div>
				</Collapse>
				<Collapse in={showAddons.database_record} unmountOnExit>
					<div id='command-offcanvas-database_record-addon'>
						<DatabaseRecord
							className='mb-3'
							initialValue={initialData?.database_record}
							onChange={useCallback(databaseRecord => { data.current.database_record = databaseRecord }, [])}
						/>
					</div>
				</Collapse>
				<Button
					size='sm'
					{...(
						showAddonButtons ? {
							variant: 'secondary',
							className: 'w-100 border-bottom-0 rounded-bottom-0',
							children: gettext('Скрыть дополнения'),
						} : {
							variant: 'dark',
							className: 'w-100',
							children: gettext('Показать дополнения'),
						}
					)}
					onClick={() => setShowAddonButtons(!showAddonButtons)}
				></Button>
				<Collapse in={showAddonButtons} unmountOnExit>
					<div id='command-offcanvas-addons'>
						<Stack className='border border-top-0 rounded rounded-top-0 p-1' gap={1}>
							{addonButtons.map(({ name, ...props }, index) => (
								<Button
									{...props}
									key={index}
									size='sm'
									variant={showAddons[name] ? 'secondary' : 'dark'}
									aria-controls={`command-offcanvas-${name}-addon`}
									aria-expanded={showAddons[name]}
									onClick={() => toggleAddon(name)}
								/>
							))}
						</Stack>
					</div>
				</Collapse>
			</Offcanvas.Body>
			<Offcanvas.Header className='border-top'>
				{children?.(data.current)}
			</Offcanvas.Header>
		</Offcanvas>
	);
}

export default memo(CommandOffcanvas);