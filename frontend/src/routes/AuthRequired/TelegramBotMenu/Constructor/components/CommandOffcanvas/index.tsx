import React, { ReactElement, ReactNode, memo, useCallback, useRef, useState } from 'react';

import Offcanvas, { OffcanvasProps } from 'react-bootstrap/Offcanvas';
import Button, { ButtonProps } from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';
import Collapse from 'react-bootstrap/Collapse';

import Loading from 'components/Loading';

import CommandName from './components/CommandName';
import Settings, { Data as SettingsData } from './components/Settings';
import Command, { Data as CommandData } from './components/Command';
import Images, { Data as ImagesData } from './components/Images';
import MessageText from './components/MessageText';
import Keyboard, { Data as KeyboardData } from './components/Keyboard';
import Files, { Data as FilesData } from './components/Files';
import APIRequest, { Data as APIRequestData } from './components/APIRequest';
import DatabaseRecord from './components/DatabaseRecord';

export interface Data {
	name?: string;
	settings?: SettingsData;
	command?: CommandData;
	images?: ImagesData;
	files?: FilesData,
	messageText?: string;
	keyboard?: KeyboardData;
	apiRequest?: APIRequestData;
	databaseRecord?: string;
}

export interface CommandOffcanvasProps extends OffcanvasProps {
	loading?: boolean;
	title: ReactNode;
	initialData?: Data;
	children?: (data: Data) => ReactNode;
}

type CommandOffcanvasBodyProps = Omit<CommandOffcanvasProps, 'loading' | 'title'>;

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

function CommandOffcanvasBody({ initialData, children }: CommandOffcanvasBodyProps): ReactElement<CommandOffcanvasBodyProps> {
	const data = useRef<Data>(initialData ?? {});

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
			data.current[name] = undefined;
		}
	}

	return (
		<>
			<Offcanvas.Body>
				<CommandName
					className='mb-3'
					initialValue={initialData?.name}
					onChange={useCallback(commandName => { data.current.name = commandName }, [])}
				/>
				<Settings
					className='mb-3'
					initialData={initialData?.settings}
					onChange={useCallback(settings => { data.current.settings = settings }, [])}
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
							initialData={initialData?.images}
							onChange={useCallback(images => { data.current.images = images }, [])}
						/>
					</div>
				</Collapse>
				<Collapse in={showAddons.files} unmountOnExit>
					<div id='command-offcanvas-files-addon'>
						<Files
							className='mb-3'
							initialData={initialData?.files}
							onChange={useCallback(files => { data.current.files = files }, [])}
						/>
					</div>
				</Collapse>
				<MessageText
					className='mb-3'
					initialValue={initialData?.messageText}
					onChange={useCallback(messageText => { data.current.messageText = messageText }, [])}
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
				<Collapse in={showAddons.apiRequest} unmountOnExit>
					<div id='command-offcanvas-apiRequest-addon'>
						<APIRequest
							className='mb-3'
							initialData={initialData?.apiRequest}
							onChange={useCallback(apiRequest => { data.current.apiRequest = apiRequest }, [])}
						/>
					</div>
				</Collapse>
				<Collapse in={showAddons.databaseRecord} unmountOnExit>
					<div id='command-offcanvas-databaseRecord-addon'>
						<DatabaseRecord
							className='mb-3'
							initialValue={initialData?.databaseRecord}
							onChange={useCallback(databaseRecord => { data.current.databaseRecord = databaseRecord }, [])}
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
				/>
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
		</>
	);
}

function CommandOffcanvas({ loading, title, initialData, children, ...props }: CommandOffcanvasProps): ReactElement<CommandOffcanvasProps> {
	return (
		<Offcanvas {...props}>
			<Offcanvas.Header className='border-bottom' closeButton>
				<Offcanvas.Title as='h5'>{title}</Offcanvas.Title>
			</Offcanvas.Header>
			{!loading ? (
				<CommandOffcanvasBody
					initialData={initialData}
					children={children}
				/>
			) : (
				<Offcanvas.Body className='d-flex'>
					<Loading size='md' className='m-auto' />
				</Offcanvas.Body>
			)}
		</Offcanvas>
	);
}

export default memo(CommandOffcanvas);