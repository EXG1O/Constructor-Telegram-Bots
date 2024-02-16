import React, { ReactElement, Dispatch, SetStateAction, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

import Loading from 'components/Loading';
import AskConfirmModal from 'components/AskConfirmModal';

import useToast from 'services/hooks/useToast';

import { TelegramBotAPI } from 'services/api/telegram_bots/main';
import { TelegramBot } from 'services/api/telegram_bots/types';

export interface TelegramBotCardFooterProps {
	telegramBot: TelegramBot;
	setTelegramBot: Dispatch<SetStateAction<TelegramBot>>;
}

function TelegramBotCardFooter({ telegramBot, setTelegramBot }: TelegramBotCardFooterProps): ReactElement<TelegramBotCardFooterProps> {
	const navigate = useNavigate();

	const { createMessageToast } = useToast();

	const [showDeleteTelegramBotModal, setShowDeleteTelegramBotModal] = useState<boolean>(false);

	async function handleConfirmDelete(): Promise<void> {
		setShowDeleteTelegramBotModal(false);

		const response = await TelegramBotAPI._delete(telegramBot.id);

		if (response.ok) {
			navigate('/personal-cabinet/');
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	async function handleStartOrStopTelegramBotButtonClick(action: 'start' | 'stop'): Promise<void> {
		const response = await TelegramBotAPI[action](telegramBot.id);

		if (response.ok) {
			setTelegramBot({ ...telegramBot, is_loading: true });
		}
	}

	return (
		<>
			<AskConfirmModal
				show={showDeleteTelegramBotModal}
				title={gettext('Удаление Telegram бота')}
				onConfirm={handleConfirmDelete}
				onHide={() => setShowDeleteTelegramBotModal(false)}
			>
				{gettext('Вы точно хотите удалить Telegram бота?')}
			</AskConfirmModal>
			<Card.Footer className='d-flex flex-wrap border border-top-0 p-3 gap-3'>
				{telegramBot.is_loading ? (
					<Button
						disabled
						variant='secondary'
						className='flex-fill d-flex justify-content-center'
					>
						<Loading size='xs' />
					</Button>
				) : telegramBot.is_enabled ? (
					<Button
						variant='danger'
						className='flex-fill'
						onClick={() => handleStartOrStopTelegramBotButtonClick('stop')}
					>
						{gettext('Выключить Telegram бота')}
					</Button>
				) : (
					<Button
						variant='success'
						className='flex-fill'
						onClick={() => handleStartOrStopTelegramBotButtonClick('start')}
					>
						{gettext('Включить Telegram бота')}
					</Button>
				)}
				<Button
					variant='danger'
					className='flex-fill'
					onClick={() => setShowDeleteTelegramBotModal(true)}
				>
					{gettext('Удалить Telegram бота')}
				</Button>
			</Card.Footer>
		</>
	);
}

export default TelegramBotCardFooter;