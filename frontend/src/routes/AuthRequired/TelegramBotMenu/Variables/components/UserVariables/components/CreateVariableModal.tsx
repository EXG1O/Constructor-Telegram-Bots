import React, { ReactElement, memo, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Modal, { ModalProps } from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import Loading from 'components/Loading';
import TinymceEditor from 'components/TinymceEditor';

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
						<TinymceEditor
							value={data.value}
							init={{ placeholder: gettext('Введите значение переменной') }}
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