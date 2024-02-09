import React, { ReactElement, ReactNode, memo, useEffect, useMemo, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Offcanvas, { OffcanvasProps } from 'react-bootstrap/Offcanvas';
import Button, { ButtonProps } from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';
import Collapse from 'react-bootstrap/Collapse';

import Loading from 'components/Loading';
import TelegramBotStorage from 'components/TelegramBotStorage';

import Name, { Value as NameValue } from './components/Name';
import Settings, { Data as SettingsData } from './components/Settings';
import Command, { Data as CommandData } from './components/Command';
import Images, { Data as ImagesData } from './components/Images';
import MessageText, { Value as MessageTextValue } from './components/MessageText';
import Keyboard, { Data as KeyboardData } from './components/Keyboard';
import Files, { Data as FilesData } from './components/Files';
import APIRequest, { Data as APIRequestData } from './components/APIRequest';
import DatabaseRecord, { Value as DatabaseRecordValue } from './components/DatabaseRecord';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

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
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const [name, setName] = useState<NameValue | undefined>(initialData?.name);
	const [settings, setSettings] = useState<SettingsData | undefined>(initialData?.settings);
	const [command, setCommand] = useState<CommandData | undefined>(initialData?.command);
	const [images, setImages] = useState<ImagesData | undefined>(initialData?.images);
	const [files, setFiles] = useState<FilesData | undefined>(initialData?.files);
	const [messageText, setMessageText] = useState<MessageTextValue | undefined>(initialData?.messageText);
	const [keyboard, setKeyboard] = useState<KeyboardData | undefined>(initialData?.keyboard);
	const [apiRequest, setAPIRequest] = useState<APIRequestData | undefined>(initialData?.apiRequest);
	const [databaseRecord, setDatabaseRecord] = useState<DatabaseRecordValue | undefined>(initialData?.databaseRecord);

	const getAddonsState = (): Record<AddonNames, boolean> => ({
		command: Boolean(initialData?.command),
		images: Boolean(initialData?.images),
		files: Boolean(initialData?.files),
		keyboard: Boolean(initialData?.keyboard),
		apiRequest: Boolean(initialData?.apiRequest),
		databaseRecord: Boolean(initialData?.databaseRecord),
	});

	const [showAddons, setShowAddons] = useState<Record<AddonNames, boolean>>(getAddonsState());
	const [showAddonButtons, setShowAddonButtons] = useState<boolean>(false);

	const usedStorageSize: number = useMemo(() => {
		let size: number = telegramBot.used_storage_size;

		size += images?.reduce((totalSize, image) => totalSize + image.size, 0) ?? 0;
		size += files?.reduce((totalSize, file) => totalSize + file.size, 0) ?? 0;

		return size;
	}, [images, files]);
	const remainingStorageSize: number = useMemo(() => telegramBot.storage_size - usedStorageSize, [usedStorageSize]);

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
		setShowAddons(getAddonsState());
	}, [initialData]);

	return (
		<Offcanvas {...props}>
			<Offcanvas.Header closeButton>
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
									remainingStorageSize={remainingStorageSize}
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
									remainingStorageSize={remainingStorageSize}
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
					</Offcanvas.Body>
					<div className='offcanvas-footer gap-2'>
						<TelegramBotStorage
							telegramBot={telegramBot}
							usedStorageSize={usedStorageSize}
						/>
						<div>
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
						</div>
					</div>
					{children && (
						<div className='offcanvas-footer'>
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
						</div>
					)}
				</>
			) : (
				<Offcanvas.Body className='d-flex justify-content-center'>
					<Loading size='md' className='align-self-center' />
				</Offcanvas.Body>
			)}
		</Offcanvas>
	);
}

export default memo(CommandOffcanvas);