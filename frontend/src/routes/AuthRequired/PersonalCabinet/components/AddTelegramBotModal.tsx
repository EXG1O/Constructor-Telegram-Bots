import React, { ReactElement, useState } from 'react';

import Modal from 'react-bootstrap/Modal';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

import Loading from 'components/Loading';

import useToast from 'services/hooks/useToast';
import useTelegramBots from '../services/hooks/useTelegramBots';

import { TelegramBotAPI } from 'services/api/telegram_bots/main';

interface Data {
	api_token: string;
	is_private: boolean;
}

export interface AddTelegramBotModalProps {
	show: boolean;
	onHide: () => void;
}

const defaultData: Data = { api_token: '', is_private: false };

function AddTelegramBotModal({ show, onHide }: AddTelegramBotModalProps): ReactElement<AddTelegramBotModalProps> {
	const { createMessageToast } = useToast();
	const [telegramBots, setTelegramBots] = useTelegramBots();

	const [data, setData] = useState<Data>(defaultData);
	const [loading, setLoading] = useState<boolean>(false);

	async function handleAddTelegramBotButtonClick(): Promise<void> {
		setLoading(true);

		const response = await TelegramBotAPI.create(data);

		if (response.ok) {
			setTelegramBots([...telegramBots, response.json.telegram_bot]);
			onHide();
		}

		setLoading(false);
		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<Modal
			show={show}
			onHide={onHide}
			onExited={() => setData(defaultData)}
		>
			<Modal.Header closeButton>
				<Modal.Title as='h5'>
					{gettext('Добавление Telegram бота')}
				</Modal.Title>
			</Modal.Header>
			{!loading ? (
				<>
					<Modal.Body className='vstack gap-2'>
						<Form.Control
							value={data.api_token}
							placeholder={gettext('Введите API-токен Telegram бота')}
							onChange={e => setData({ ...data, api_token: e.target.value })}
						/>
						<Form.Switch
							checked={data.is_private}
							label={gettext('Сделать Telegram бота приватным')}
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
				</>
			) : (
				<Modal.Body className='d-flex justify-content-center'>
					<Loading size='md' />
				</Modal.Body>
			)}
		</Modal>
	);
}

export default AddTelegramBotModal;