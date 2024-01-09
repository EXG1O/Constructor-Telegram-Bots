import React, { Dispatch, ReactElement, SetStateAction, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';

import Loading from 'components/Loading';
import AskConfirmModal from 'components/AskConfirmModal';

import useToast from 'services/hooks/useToast';

import { TelegramBotAPI } from 'services/api/telegram_bots/main';

import { telegramBotIsStartingOrStopping } from 'utils/telegram_bot';

import { TelegramBot } from 'services/api/telegram_bots/types';

export interface TelegramBotCardFooterProps {
	telegramBot: TelegramBot;
	setTelegramBot: Dispatch<SetStateAction<TelegramBot>>;
}

function TelegramBotCardFooter({ telegramBot, setTelegramBot }: TelegramBotCardFooterProps): ReactElement<TelegramBotCardFooterProps> {
	const navigate = useNavigate();

	const { createMessageToast } = useToast();

	const [showDeleteTelegramBotModal, setShowDeleteTelegramBotModal] = useState<boolean>(false);

	async function handleConfirmDeleteTelegramBotButtonClick(): Promise<void> {
		setShowDeleteTelegramBotModal(false);

		const response = await TelegramBotAPI.delete_(telegramBot.id);

		if (response.ok) {
			navigate('/personal-cabinet/');
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	async function handleStartOrStopTelegramBotButtonClick(action: 'start' | 'stop'): Promise<void> {
		const response = await TelegramBotAPI[action](telegramBot.id);

		if (response.ok) {
			const isStartAction = action === 'start';

			setTelegramBot({
				...telegramBot,
				is_running: isStartAction,
				is_stopped: isStartAction,
			});
		}
	}

	return (
		<>
			<AskConfirmModal
				show={showDeleteTelegramBotModal}
				title={gettext('Удаление Telegram бота')}
				onConfirmButtonClick={handleConfirmDeleteTelegramBotButtonClick}
				onHide={() => setShowDeleteTelegramBotModal(false)}
			>
				{gettext('Вы точно хотите удалить Telegram бота?')}
			</AskConfirmModal>
			<Card.Footer className='d-flex flex-wrap border border-top-0 p-3 gap-3'>
				{telegramBotIsStartingOrStopping(telegramBot) ? (
					<Button
						disabled
						variant='secondary'
						className='flex-fill'
					>
						<Loading size='xs' />
					</Button>
				) : !telegramBot.is_running && telegramBot.is_stopped ? (
					<Button
						variant='success'
						className='flex-fill'
						onClick={() => handleStartOrStopTelegramBotButtonClick('start')}
					>
						{gettext('Включить Telegram бота')}
					</Button>
				) : (
					<Button
						variant='danger'
						className='flex-fill'
						onClick={() => handleStartOrStopTelegramBotButtonClick('stop')}
					>
						{gettext('Выключить Telegram бота')}
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