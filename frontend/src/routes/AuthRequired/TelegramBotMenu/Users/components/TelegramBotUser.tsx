import React, { ReactNode, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Button from 'react-bootstrap/Button';

import AskConfirmModal from 'components/AskConfirmModal';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import useToast from 'services/hooks/useToast';

import { TelegramBotUserAPI } from 'services/api/telegram_bots/main';
import { TelegramBotUser as TelegramBotUserType } from 'services/api/telegram_bots/types';

export interface TelegramBotUserProps {
	telegramBotUser: TelegramBotUserType;
	updateTelegramBotUsers: () => Promise<void>;
}

function TelegramBotUser({ telegramBotUser, updateTelegramBotUsers }: TelegramBotUserProps): ReactNode {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [showDeleteTelegramBotUserModal, setShowDeleteTelegramBotUserModal] = useState<boolean>(false);

	async function handleSetOrUnsetAllowedButtonClick(): Promise<void> {
		const response = await TelegramBotUserAPI.post(telegramBot.id, telegramBotUser.id, telegramBotUser.is_allowed ? 'unallow' : 'allow');

		if (response.ok) {
			updateTelegramBotUsers();
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	async function handleConfirmDelete(): Promise<void> {
		const response = await TelegramBotUserAPI._delete(telegramBot.id, telegramBotUser.id);

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
				onConfirm={handleConfirmDelete}
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
						{telegramBotUser.telegram_id}
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