import React, { ReactNode, useState } from 'react';

import Button from 'react-bootstrap/Button';

import AskConfirmModal from 'components/AskConfirmModal';

import useTelegramBot from 'services/hooks/useTelegramBot';
import useToast from 'services/hooks/useToast';

import { TelegramBotUserAPI, TelegramBotAllowedUserAPI } from 'services/api/telegram_bots/main';
import { TelegramBotUser as TelegramBotUserType } from 'services/api/telegram_bots/types';

export interface TelegramBotUserProps {
	telegramBotUser: TelegramBotUserType;
	updateTelegramBotUsers: () => Promise<void>;
}

function TelegramBotUser({ telegramBotUser, updateTelegramBotUsers }: TelegramBotUserProps): ReactNode {
	const { telegramBot } = useTelegramBot();
	const { createMessageToast } = useToast();

	const [showDeleteTelegramBotUserModal, setShowDeleteTelegramBotUserModal] = useState<boolean>(false);

	async function handleSetOrUnsetAllowedButtonClick(): Promise<void> {
		const response = await TelegramBotAllowedUserAPI[telegramBotUser.is_allowed ? 'unset' : 'set'](telegramBot.id, telegramBotUser.id);

		if (response.ok) {
			updateTelegramBotUsers();
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	async function handleDeleteButtonClick(): Promise<void> {
		const response = await TelegramBotUserAPI.delete_(telegramBot.id, telegramBotUser.id);

		if (response.ok) {
			updateTelegramBotUsers();
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<>
			<AskConfirmModal
				show={showDeleteTelegramBotUserModal}
				title={'Удаление пользователя'}
				onHide={() => setShowDeleteTelegramBotUserModal(false)}
				onConfirmButtonClick={handleDeleteButtonClick}
			>
				{gettext('Вы точно хотите удалить пользователя Telegram бота?')}
			</AskConfirmModal>
			<div className='d-flex align-items-center gap-2'>
				<p className='flex-fill text-break m-0'>
					{'['}
					<span className='text-success-emphasis'>
						{telegramBotUser.activated_date}
					</span>
					{']: '}
					<span className='text-primary-emphasis'>
						{telegramBotUser.user_id}
					</span>
					{' - '}
					{telegramBotUser.full_name}
				</p>
				<div className='btn-group' role='group'>
					{!telegramBot.is_private && (
						<Button
							variant='warning'
							className={`text-light bi bi-${telegramBotUser.is_allowed ? 'star-fill' : 'star'} px-2 py-0`}
							style={{ fontSize: '20px' }}
							onClick={handleSetOrUnsetAllowedButtonClick}
						/>
					)}
					<Button
						variant='danger'
						className='text-light bi bi-bi bi-ban px-2 py-0'
						style={{ fontSize: '20px', WebkitTextStrokeWidth: '0.2px' }}
					/>
				</div>
				<Button
					variant='danger'
					className='bi bi-trash px-2 py-0'
					style={{ fontSize: '20px' }}
					onClick={() => setShowDeleteTelegramBotUserModal(true)}
				/>
			</div>
		</>
	);
}

export default TelegramBotUser;