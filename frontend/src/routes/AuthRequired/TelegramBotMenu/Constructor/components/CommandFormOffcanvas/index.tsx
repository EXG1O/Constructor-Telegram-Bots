import React, { ReactElement, ReactNode, useMemo, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Button, { ButtonProps } from 'react-bootstrap/Button';
import Stack from 'react-bootstrap/Stack';
import Collapse from 'react-bootstrap/Collapse';

import Offcanvas, { OffcanvasProps } from 'components/Offcanvas';
import TelegramBotStorage from 'components/TelegramBotStorage';

import Name, { Value as NameValue } from '../Name';
import Settings, { Data as SettingsData } from './components/Settings';
import Trigger, { Data as TriggerData, defaultData as triggerDefaultData } from './components/Trigger';
import Images, { Data as ImagesData, defaultData as imagesDefaultData } from './components/Images';
import FilesCard, { Data as FilesData, defaultData as filesDefaultData } from './components/Files';
import Message, { Value as MessageValue } from './components/Message';
import Keyboard, { Data as KeyboardData, defaultData as keyboardDefaultData } from './components/Keyboard';
import APIRequest, { Data as APIRequestData, defaultData as apiRequestDefaultData } from '../APIRequest';
import DatabaseRecord, { Value as DatabaseRecordValue, defaultValue as databaseRecordDefaultValue } from './components/DatabaseRecord';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

export interface CommandFormOffcanvasProps extends OffcanvasProps {
	name?: NameValue;
	settings?: SettingsData;
	trigger?: TriggerData;
	images?: ImagesData;
	files?: FilesData,
	message?: MessageValue;
	keyboard?: KeyboardData;
	apiRequest?: APIRequestData;
	databaseRecord?: DatabaseRecordValue;
	title: ReactNode;
	onNameChange: (value: NameValue) => void;
	onSettingsChange: (data: SettingsData) => void;
	onTriggerChange: (data: TriggerData | undefined) => void;
	onImagesChange: (data: ImagesData | undefined) => void;
	onFilesChange: (data: FilesData | undefined) => void;
	onMessageChange: (value: MessageValue) => void;
	onKeyboardChange: (data: KeyboardData | undefined) => void;
	onAPIRequestChange: (data: APIRequestData | undefined) => void;
	onDatabaseRecordChange: (value: DatabaseRecordValue | undefined) => void;
}

type AddonNames = 'trigger' | 'images' | 'files' | 'keyboard' | 'apiRequest' | 'databaseRecord';

interface AddonButtonsProps extends Omit<ButtonProps, 'key' | 'size' | 'variant' | 'onClick'> {
	name: AddonNames;
	onShow: () => void;
	onHide: () => void;
	children: string;
}

function CommandFormOffcanvas({
	name,
	settings,
	trigger,
	images,
	files,
	message,
	keyboard,
	apiRequest,
	databaseRecord,
	title,
	children,
	onNameChange,
	onSettingsChange,
	onTriggerChange,
	onImagesChange,
	onFilesChange,
	onMessageChange,
	onKeyboardChange,
	onAPIRequestChange,
	onDatabaseRecordChange,
	...props
}: CommandFormOffcanvasProps): ReactElement<CommandFormOffcanvasProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const addonButtons = useMemo<AddonButtonsProps[]>(() => [
		{
			name: 'trigger',
			onShow: () => onTriggerChange(triggerDefaultData),
			onHide: () => onTriggerChange(undefined),
			children: gettext('Триггер'),
		},
		{
			name: 'images',
			onShow: () => onImagesChange(imagesDefaultData),
			onHide: () => onImagesChange(undefined),
			children: gettext('Изображения'),
		},
		{
			name: 'files',
			onShow: () => onFilesChange(filesDefaultData),
			onHide: () => onFilesChange(undefined),
			children: gettext('Файлы'),
		},
		{
			name: 'keyboard',
			onShow: () => onKeyboardChange(keyboardDefaultData),
			onHide: () => onKeyboardChange(undefined),
			children: gettext('Клавиатура'),
		},
		{
			name: 'apiRequest',
			onShow: () => onAPIRequestChange(apiRequestDefaultData),
			onHide: () => onAPIRequestChange(undefined),
			children: gettext('API-запрос'),
		},
		{
			name: 'databaseRecord',
			onShow: () => onDatabaseRecordChange(databaseRecordDefaultValue),
			onHide: () => onDatabaseRecordChange(undefined),
			children: gettext('Запись в базу данных'),
		},
	], [
		onTriggerChange,
		onImagesChange,
		onFilesChange,
		onKeyboardChange,
		onAPIRequestChange,
		onDatabaseRecordChange,
	]);
	const showAddons = useMemo<Record<AddonNames, boolean>>(() => ({
		trigger: trigger !== undefined,
		images: images !== undefined,
		files: files !== undefined,
		keyboard: keyboard !== undefined,
		apiRequest: apiRequest !== undefined,
		databaseRecord: databaseRecord !== undefined,
	}), [trigger, images, files, keyboard, apiRequest, databaseRecord]);

	const [showAddonButtons, setShowAddonButtons] = useState<boolean>(false);

	const usedStorageSize: number = useMemo(() => {
		let size: number = telegramBot.used_storage_size;

		size += images?.reduce((totalSize, image) => totalSize + image.size, 0) ?? 0;
		size += files?.reduce((totalSize, file) => totalSize + file.size, 0) ?? 0;

		return size;
	}, [images, files]);
	const remainingStorageSize: number = useMemo(() => telegramBot.storage_size - usedStorageSize, [usedStorageSize]);

	return (
		<Offcanvas {...props}>
			<Offcanvas.Header closeButton>
				<Offcanvas.Title as='h5'>{title}</Offcanvas.Title>
			</Offcanvas.Header>
			<Offcanvas.Body>
				<Name
					value={name}
					className='mb-3'
					onChange={onNameChange}
				/>
				<Settings
					data={settings}
					className='mb-3'
					onChange={onSettingsChange}
				/>
				<Collapse in={showAddons.trigger} unmountOnExit>
					<div>
						<Trigger
							data={trigger}
							className='mb-3'
							onChange={onTriggerChange}
						/>
					</div>
				</Collapse>
				<Collapse in={showAddons.images} unmountOnExit>
					<div id='command-offcanvas-image-addon'>
						<Images
							data={images}
							remainingStorageSize={remainingStorageSize}
							className='mb-3'
							onChange={onImagesChange}
						/>
					</div>
				</Collapse>
				<Collapse in={showAddons.files} unmountOnExit>
					<div>
						<FilesCard
							data={files}
							remainingStorageSize={remainingStorageSize}
							className='mb-3'
							onChange={onFilesChange}
						/>
					</div>
				</Collapse>
				<Message
					value={message}
					className='mb-3'
					onChange={onMessageChange}
				/>
				<Collapse in={showAddons.keyboard} unmountOnExit>
					<div>
						<Keyboard
							data={keyboard}
							className='mb-3'
							onChange={onKeyboardChange}
						/>
					</div>
				</Collapse>
				<Collapse in={showAddons.apiRequest} unmountOnExit>
					<div>
						<APIRequest
							data={apiRequest}
							className='mb-3'
							onChange={onAPIRequestChange}
						/>
					</div>
				</Collapse>
				<Collapse in={showAddons.databaseRecord} unmountOnExit>
					<div>
						<DatabaseRecord
							value={databaseRecord}
							className='mb-3'
							onChange={onDatabaseRecordChange}
						/>
					</div>
				</Collapse>
			</Offcanvas.Body>
			<Offcanvas.Footer className='gap-2'>
				<TelegramBotStorage
					size='sm'
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
						<div>
							<Stack className='border border-top-0 rounded-1 rounded-top-0 p-1' gap={1}>
								{addonButtons.map(({ name, onShow, onHide, ...props }, index) => (
									<Button
										{...props}
										key={index}
										size='sm'
										variant={showAddons[name] ? 'secondary' : 'dark'}
										onClick={showAddons[name] ? onHide : onShow}
									/>
								))}
							</Stack>
						</div>
					</Collapse>
				</div>
			</Offcanvas.Footer>
			{children}
		</Offcanvas>
	);
}

export default Object.assign(CommandFormOffcanvas, { Footer: Offcanvas.Footer });