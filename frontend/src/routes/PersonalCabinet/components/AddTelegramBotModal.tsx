import React, { ReactNode, useState } from 'react';

import Modal, { ModalProps } from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import useToast from 'services/hooks/useToast';
import useTelegramBots from '../services/hooks/useTelegramBots';

import { TelegramBotAPI } from 'services/api/telegram_bots/main';

interface Data {
	api_token: string;
	is_private: boolean;
}

export interface AddTelegramBotModalProps extends Omit<ModalProps, 'onHide'> {
	onHide: NonNullable<ModalProps['onHide']>;
}

function AddTelegramBotModal(props: AddTelegramBotModalProps): ReactNode {
	const { createMessageToast } = useToast();
	const { telegramBots, setTelegramBots } = useTelegramBots();

	const [data, setData] = useState<Data>({ api_token: '', is_private: false });

	async function handleAddTelegramBotButtonClick(): Promise<void> {
		const response = await TelegramBotAPI.create(data);

		if (response.ok) {
			setTelegramBots([...telegramBots, response.json.telegram_bot]);
			props.onHide();
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<Modal {...props}>
			<Modal.Header closeButton>
				<Modal.Title as='h5'>{gettext('Добавление Telegram бота')}</Modal.Title>
			</Modal.Header>
			<Modal.Body className='vstack gap-2'>
				<Form.Control
					value={data.api_token}
					placeholder={gettext('Введите API-токен Telegram бота')}
					onChange={e => setData({ ...data, api_token: e.target.value })}
				/>
				<Form.Switch
					checked={data.is_private}
					label={gettext('Сделать Telegram бота приватным')}
					style={{ width: 'max-content' }}
					onChange={e => setData({ ...data, is_private: e.target.checked })}
				/>
			</Modal.Body>
			<Modal.Footer>
				<Button
					variant='success'
					className='w-100'
					onClick={handleAddTelegramBotButtonClick}
				>
					{gettext('Добавить Telegram бота')}
				</Button>
			</Modal.Footer>
		</Modal>
	);
}

export default AddTelegramBotModal;