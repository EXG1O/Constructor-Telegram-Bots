import 'tinymce/tinymce';
import 'tinymce/models/dom/model';
import 'tinymce/themes/silver';
import 'tinymce/icons/default';
import 'tinymce/skins/ui/oxide/skin.min.css';
import './CreateVariableModal.css';

import React, { ReactElement, memo, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Modal, { ModalProps } from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import { Editor } from '@tinymce/tinymce-react';
import Button from 'react-bootstrap/Button';

import Loading from 'components/Loading';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import useToast from 'services/hooks/useToast';

import { TelegramBotVariableAPI } from 'services/api/telegram_bots/main';
import { TelegramBotVariable, Data } from 'services/api/telegram_bots/types';

export interface CreateVariableModalProps extends Omit<ModalProps, 'onHide' | 'children'> {
	onCreate: (variable: TelegramBotVariable) => void;
	onHide: NonNullable<ModalProps['onHide']>;
}

function CreateVariableModal({ onCreate, ...props }: CreateVariableModalProps): ReactElement<CreateVariableModalProps> {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [data, setData] = useState<Data.TelegramBotVariableAPI.Create>({
		name: '',
		value: '',
		description: '',
	});
	const [loading, setLoading] = useState<boolean>(false);

	async function handleCreateButtonClick(): Promise<void> {
		setLoading(true);

		const response = await TelegramBotVariableAPI.create(telegramBot.id, data);

		if (response.ok) {
			onCreate(response.json.telegram_bot_variable);
		}

		setLoading(false);
		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<Modal {...props}>
			<Modal.Header closeButton>
				<Modal.Title as='h5'>{gettext('Создание переменной')}</Modal.Title>
			</Modal.Header>
				{!loading ? (
					<Modal.Body className='vstack gap-2'>
						<Form.Control
							value={data.name}
							placeholder={gettext('Придумайте название переменной')}
							onChange={e => setData({ ...data, name: e.target.value })}
						/>
						<Editor
							value={data.value}
							init={{
								skin: false,
								content_css: false,
								height: 260,
								toolbar: 'bold italic underline strikethrough',
								placeholder: gettext('Введите значение переменной'),
								formats: { underline: { inline: 'u' } },
								newline_behavior: 'linebreak',
								menubar: false,
								promotion: false,
								statusbar: false,
								resize: false,
								content_style: `
									body {
										font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
										margin: 6px 12px;
									}

									body[data-mce-placeholder]:not(.mce-visualblocks)::before {
										color: rgba(34, 47, 62, 0.7);
										content: attr(data-mce-placeholder);
										position: absolute;
									}

									p {
										margin: 0px;
									}
								`,
							}}
							onEditorChange={value => setData({ ...data, value })}
						/>
						<Form.Control
							value={data.description}
							placeholder={gettext('Введите описание переменной')}
							onChange={e => setData({ ...data, description: e.target.value })}
						/>
					</Modal.Body>
				) : (
					<Modal.Body className='d-flex justify-content-center d-flex align-items-center'>
						<Loading size='md' />
					</Modal.Body>
				)}
			{!loading ? (
				<Modal.Footer>
					<Button
						variant='success'
						className='w-100'
						onClick={handleCreateButtonClick}
					>
						{gettext('Создать')}
					</Button>
				</Modal.Footer>
			) : undefined}
		</Modal>
	);
}

export default memo(CreateVariableModal);