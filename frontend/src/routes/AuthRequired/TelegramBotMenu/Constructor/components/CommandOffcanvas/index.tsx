import React, { ReactElement, ReactNode, memo, useEffect, useState } from 'react';

import Offcanvas, { OffcanvasProps } from 'react-bootstrap/Offcanvas';
import Button, { ButtonProps } from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';
import Collapse from 'react-bootstrap/Collapse';

import Loading from 'components/Loading';

import Name, { Value as NameValue } from './components/Name';
import Settings, { Data as SettingsData } from './components/Settings';
import Command, { Data as CommandData } from './components/Command';
import Images, { Data as ImagesData } from './components/Images';
import MessageText, { Value as MessageTextValue } from './components/MessageText';
import Keyboard, { Data as KeyboardData } from './components/Keyboard';
import Files, { Data as FilesData } from './components/Files';
import APIRequest, { Data as APIRequestData } from './components/APIRequest';
import DatabaseRecord, { Value as DatabaseRecordValue } from './components/DatabaseRecord';

export interface Data {
	name?: NameValue;
	settings?: SettingsData;
	command?: CommandData;
	images?: ImagesData;
	files?: FilesData,
	messageText?: MessageTextValue;
	keyboard?: KeyboardData;
	apiRequest?: APIRequestData;
	databaseRecord?: DatabaseRecordValue;
}

export interface CommandOffcanvasProps extends OffcanvasProps {
	loading?: boolean;
	title: ReactNode;
	initialData?: Data;
	children?: (data: Data) => ReactNode;
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

function CommandOffcanvas({ loading, title, initialData, children, ...props }: CommandOffcanvasProps): ReactElement<CommandOffcanvasProps> {
	const [name, setName] = useState<NameValue | undefined>(initialData?.name);
	const [settings, setSettings] = useState<SettingsData | undefined>(initialData?.settings);
	const [command, setCommand] = useState<CommandData | undefined>(initialData?.command);
	const [images, setImages] = useState<ImagesData | undefined>(initialData?.images);
	const [files, setFiles] = useState<FilesData | undefined>(initialData?.files);
	const [messageText, setMessageText] = useState<MessageTextValue | undefined>(initialData?.messageText);
	const [keyboard, setKeyboard] = useState<KeyboardData | undefined>(initialData?.keyboard);
	const [apiRequest, setAPIRequest] = useState<APIRequestData | undefined>(initialData?.apiRequest);
	const [databaseRecord, setDatabaseRecord] = useState<DatabaseRecordValue | undefined>(initialData?.databaseRecord);

	const [showAddons, setShowAddons] = useState<Record<AddonNames, boolean>>({
		command: Boolean(initialData?.command),
		images: Boolean(initialData?.images),
		files: Boolean(initialData?.files),
		keyboard: Boolean(initialData?.keyboard),
		apiRequest: Boolean(initialData?.apiRequest),
		databaseRecord: Boolean(initialData?.databaseRecord),
	});
	const [showAddonButtons, setShowAddonButtons] = useState<boolean>(true);

	useEffect(() => {
		setName(initialData?.name);
		setSettings(initialData?.settings);
		setCommand(initialData?.command);
		setImages(initialData?.images);
		setFiles(initialData?.files);
		setMessageText(initialData?.messageText);
		setKeyboard(initialData?.keyboard);
		setAPIRequest(initialData?.apiRequest);
		setDatabaseRecord(initialData?.databaseRecord);
		setShowAddons({
			command: Boolean(initialData?.command),
			images: Boolean(initialData?.images),
			files: Boolean(initialData?.files),
			keyboard: Boolean(initialData?.keyboard),
			apiRequest: Boolean(initialData?.apiRequest),
			databaseRecord: Boolean(initialData?.databaseRecord),
		});
	}, [initialData]);

	return (
		<Offcanvas {...props}>
			<Offcanvas.Header className='border-bottom' closeButton>
				<Offcanvas.Title as='h5'>{title}</Offcanvas.Title>
			</Offcanvas.Header>
			{!loading ? (
				<>
					<Offcanvas.Body>
						<Name
							value={name}
							className='mb-3'
							onChange={setName}
						/>
						<Settings
							data={settings}
							className='mb-3'
							onChange={setSettings}
						/>
						<Collapse
							in={showAddons.command}
							unmountOnExit
							onExited={() => setCommand(undefined)}
						>
							<div id='command-offcanvas-command-addon'>
								<Command
									data={command}
									className='mb-3'
									onChange={setCommand}
								/>
							</div>
						</Collapse>
						<Collapse
							in={showAddons.images}
							unmountOnExit
							onExited={() => setImages(undefined)}
						>
							<div id='command-offcanvas-image-addon'>
								<Images
									data={images}
									className='mb-3'
									onChange={setImages}
								/>
							</div>
						</Collapse>
						<Collapse
							in={showAddons.files}
							unmountOnExit
							onExited={() => setFiles(undefined)}
						>
							<div id='command-offcanvas-files-addon'>
								<Files
									data={files}
									className='mb-3'
									onChange={setFiles}
								/>
							</div>
						</Collapse>
						<MessageText value={messageText} onChange={setMessageText} />
						<Collapse
							in={showAddons.keyboard}
							unmountOnExit
							onExited={() => setKeyboard(undefined)}
						>
							<div id='command-offcanvas-keyboard-addon'>
								<Keyboard
									data={keyboard}
									className='mb-3'
									onChange={setKeyboard}
								/>
							</div>
						</Collapse>
						<Collapse
							in={showAddons.apiRequest}
							unmountOnExit
							onExited={() => setAPIRequest(undefined)}
						>
							<div id='command-offcanvas-apiRequest-addon'>
								<APIRequest
									data={apiRequest}
									className='mb-3'
									onChange={setAPIRequest}
								/>
							</div>
						</Collapse>
						<Collapse
							in={showAddons.databaseRecord}
							unmountOnExit
							onExited={() => setDatabaseRecord(undefined)}
						>
							<div id='command-offcanvas-databaseRecord-addon'>
								<DatabaseRecord
									value={databaseRecord}
									className='mb-3'
									onChange={setDatabaseRecord}
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
								<Stack className='border border-top-0 rounded-1 rounded-top-0 p-1' gap={1}>
									{addonButtons.map(({ name, ...props }, index) => (
										<Button
											{...props}
											key={index}
											size='sm'
											variant={showAddons[name] ? 'secondary' : 'dark'}
											aria-controls={`command-offcanvas-${name}-addon`}
											aria-expanded={showAddons[name]}
											onClick={() => setShowAddons({ ...showAddons, [name]: !showAddons[name] })}
										/>
									))}
								</Stack>
							</div>
						</Collapse>
					</Offcanvas.Body>
					{children && (
						<Offcanvas.Header className='border-top'>
							{children({
								name,
								settings,
								command,
								images,
								files,
								messageText,
								keyboard,
								apiRequest,
								databaseRecord,
							})}
						</Offcanvas.Header>
					)}
				</>
			) : (
				<Offcanvas.Body className='d-flex'>
					<Loading size='md' className='m-auto' />
				</Offcanvas.Body>
			)}
		</Offcanvas>
	);
}

export default memo(CommandOffcanvas);