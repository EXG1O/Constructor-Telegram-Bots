import React, { ReactNode, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import AskConfirmModal from 'components/AskConfirmModal';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import useToast from 'services/hooks/useToast';

import { TelegramBotUserAPI } from 'services/api/telegram_bots/main';
import { TelegramBotUser as TelegramBotUserType } from 'services/api/telegram_bots/types';

export interface TelegramBotUserProps {
	telegramBotUser: TelegramBotUserType;
	onDeleted: () => Promise<void>;
}

function TelegramBotUser({ telegramBotUser, onDeleted }: TelegramBotUserProps): ReactNode {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [showDeleteTelegramBotUserModal, setShowDeleteTelegramBotUserModal] = useState<boolean>(false);
	const [loadingDeleteTelegramBotUserModal, setLoadingDeleteTelegramBotUserModal] = useState<boolean>(false);

	async function handleConfirmDelete(): Promise<void> {
		setLoadingDeleteTelegramBotUserModal(true);

		const response = await TelegramBotUserAPI._delete(telegramBot.id, telegramBotUser.id);

		if (response.ok) {
			onDeleted();
			setShowDeleteTelegramBotUserModal(false);
		}

		setLoadingDeleteTelegramBotUserModal(false);
		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<>
			<AskConfirmModal
				show={showDeleteTelegramBotUserModal}
				loading={loadingDeleteTelegramBotUserModal}
				title={gettext('Удаление пользователя')}
				onConfirm={handleConfirmDelete}
				onHide={() => setShowDeleteTelegramBotUserModal(false)}
			>
				{gettext('Вы точно хотите удалить пользователя Telegram бота?')}
			</AskConfirmModal>
			<tr>
				<td className='text-success-emphasis'>
					{`[${telegramBotUser.activated_date}]`}
				</td>
				<td className='text-primary-emphasis'>
					{telegramBotUser.telegram_id}
				</td>
				<td className='w-100'>
					{telegramBotUser.full_name}
				</td>
				<td>
					<i
						className='d-flex bi bi-trash text-danger'
						style={{ fontSize: '19px', cursor: 'pointer' }}
						onClick={() => setShowDeleteTelegramBotUserModal(true)}
					/>
				</td>
			</tr>
		</>
	);
}

export default TelegramBotUser;