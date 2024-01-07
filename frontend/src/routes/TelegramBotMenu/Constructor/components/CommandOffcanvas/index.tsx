import React, { ReactElement, ReactNode, MutableRefObject, memo, useCallback, useRef, useState } from 'react';

import Offcanvas, { OffcanvasProps } from 'react-bootstrap/Offcanvas';
import Button, { ButtonProps } from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';
import Collapse from 'react-bootstrap/Collapse';

import Loading from 'components/Loading';

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
	command?: CommandData;
	images?: ImagesData;
	files?: FilesData,
	messageText: string;
	keyboard?: KeyboardData;
	apiRequest?: APIRequestData;
	databaseRecord?: string;
}

export interface CommandOffcanvasProps extends Omit<OffcanvasProps, 'children'> {
	title: ReactNode;
	loading?: boolean;
	initialData?: Data;
	children?: (data: Data) => ReactNode;
}

interface InnerRefValue {
	data: Data;
}

interface CommandOffcanvasLoadedBodyProps extends Pick<CommandOffcanvasProps, 'initialData'> {
	innerRef: MutableRefObject<InnerRefValue>;
}

type AddonNames = 'command' | 'images' | 'files' | 'keyboard' | 'apiRequest' | 'databaseRecord';

interface AddonButtonsProps extends Omit<ButtonProps, 'key' | 'size' | 'variant' | 'onClick'> {
	name: AddonNames;
}

const addonButtons: AddonButtonsProps[] = [
	{ name: 'command', children: gettext('Команда') },
	{ name: 'images', children: gettext('Изображения') },
	{ name: 'files', children: gettext('Файлы') },
	{ name: 'keyboard', children: gettext('Клавиатура') },
	{ name: 'apiRequest', children: gettext('API-запрос') },
	{ name: 'databaseRecord', children: gettext('Запись в базу данных') },
];

function CommandOffcanvasLoadingBody(): ReactElement {
	return (
		<Offcanvas.Body className='d-flex'>
			<Loading size='md' className='m-auto' />
		</Offcanvas.Body>
	);
}

function CommandOffcanvasLoadedBody({ innerRef, initialData }: CommandOffcanvasLoadedBodyProps): ReactElement<CommandOffcanvasLoadedBodyProps> {
	const [showAddons, setShowAddons] = useState<Record<AddonNames, boolean>>({
		command: Boolean(initialData?.command),
		images: Boolean(initialData?.images),
		files: Boolean(initialData?.files),
		keyboard: Boolean(initialData?.keyboard),
		apiRequest: Boolean(initialData?.apiRequest),
		databaseRecord: Boolean(initialData?.databaseRecord),
	});
	const [showAddonButtons, setShowAddonButtons] = useState<boolean>(true);

	function toggleAddon(name: AddonNames): void {
		setShowAddons({ ...showAddons, [name]: !showAddons[name] });

		if (showAddons[name]) {
			innerRef.current.data[name] = undefined;
		}
	}

	return (
		<Offcanvas.Body>
			<CommandName
				className='mb-3'
				initialValue={initialData?.name}
				onChange={useCallback(commandName => { innerRef.current.data.name = commandName }, [])}
			/>
			<Collapse in={showAddons.command} unmountOnExit>
				<div id='command-offcanvas-command-addon'>
					<Command
						className='mb-3'
						initialData={initialData?.command}
						onChange={useCallback(command => { innerRef.current.data.command = command }, [])}
					/>
				</div>
			</Collapse>
			<Collapse in={showAddons.images} unmountOnExit>
				<div id='command-offcanvas-image-addon'>
					<Images
						className='mb-3'
						initialData={initialData?.images}
						onChange={useCallback(images => { innerRef.current.data.images = images }, [])}
					/>
				</div>
			</Collapse>
			<Collapse in={showAddons.files} unmountOnExit>
				<div id='command-offcanvas-files-addon'>
					<Files
						className='mb-3'
						initialData={initialData?.files}
						onChange={useCallback(files => { innerRef.current.data.files = files }, [])}
					/>
				</div>
			</Collapse>
			<MessageText
				className='mb-3'
				initialValue={initialData?.messageText}
				onChange={useCallback(messageText => { innerRef.current.data.messageText = messageText }, [])}
			/>
			<Collapse in={showAddons.keyboard} unmountOnExit>
				<div id='command-offcanvas-keyboard-addon'>
					<Keyboard
						className='mb-3'
						initialData={initialData?.keyboard}
						onChange={useCallback(keyboard => { innerRef.current.data.keyboard = keyboard }, [])}
					/>
				</div>
			</Collapse>
			<Collapse in={showAddons.apiRequest} unmountOnExit>
				<div id='command-offcanvas-apiRequest-addon'>
					<APIRequest
						className='mb-3'
						initialData={initialData?.apiRequest}
						onChange={useCallback(apiRequest => { innerRef.current.data.apiRequest = apiRequest }, [])}
					/>
				</div>
			</Collapse>
			<Collapse in={showAddons.databaseRecord} unmountOnExit>
				<div id='command-offcanvas-databaseRecord-addon'>
					<DatabaseRecord
						className='mb-3'
						initialValue={initialData?.databaseRecord}
						onChange={useCallback(databaseRecord => { innerRef.current.data.databaseRecord = databaseRecord }, [])}
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
	);
}

function CommandOffcanvas({ title, loading, initialData, children, ...props }: CommandOffcanvasProps): ReactElement<CommandOffcanvasProps> {
	const innerRef = useRef<InnerRefValue>({ data: { name: '', messageText: '' } });

	return (
		<Offcanvas {...props}>
			<Offcanvas.Header className='border-bottom' closeButton>
				<Offcanvas.Title as='h5'>{title}</Offcanvas.Title>
			</Offcanvas.Header>
			{loading ? (
				<CommandOffcanvasLoadingBody />
			) : (
				<CommandOffcanvasLoadedBody
					innerRef={innerRef}
					initialData={initialData}
				/>
			)}
			<Offcanvas.Header className='border-top'>
				{loading ? (
					<Loading size='sm' className='m-auto' />
				) : (
					children?.(innerRef.current.data!)
				)}
			</Offcanvas.Header>
		</Offcanvas>
	);
}

export default memo(CommandOffcanvas);