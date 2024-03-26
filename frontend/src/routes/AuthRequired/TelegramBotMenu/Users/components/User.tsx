import React, { ReactNode, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import AskConfirmModal from 'components/AskConfirmModal';

import useToast from 'services/hooks/useToast';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { UserAPI } from 'services/api/telegram_bots/main';
import { User as UserType } from 'services/api/telegram_bots/types';

export interface UserProps {
	user: UserType;
	onDeleted: () => Promise<void> | void;
}

function User({ user, onDeleted }: UserProps): ReactNode {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();

	const [showDeleteUserModal, setShowDeleteUserModal] = useState<boolean>(false);
	const [loadingDeleteUserModal, setLoadingDeleteUserModal] = useState<boolean>(false);

	async function handleConfirmDelete(): Promise<void> {
		setLoadingDeleteUserModal(true);

		const response = await UserAPI._delete(telegramBot.id, user.id);

		if (response.ok) {
			onDeleted();
			setShowDeleteUserModal(false);
			createMessageToast({
				message: gettext('Вы успешно удалили пользователя.'),
				level: 'success',
			});
		} else {
			createMessageToast({
				message: gettext('Не удалось удалить пользователя!'),
				level: 'error',
			});
		}

		setLoadingDeleteUserModal(false);
	}

	return (
		<>
			<AskConfirmModal
				show={showDeleteUserModal}
				loading={loadingDeleteUserModal}
				title={gettext('Удаление пользователя')}
				onConfirm={handleConfirmDelete}
				onHide={() => setShowDeleteUserModal(false)}
			>
				{gettext('Вы точно хотите удалить пользователя Telegram бота?')}
			</AskConfirmModal>
			<tr>
				<td className='text-success-emphasis'>{`[${user.activated_date}]`}</td>
				<td className='text-primary-emphasis'>{user.telegram_id}</td>
				<td className='w-100'>{user.full_name}</td>
				<td>
					<i
						className='d-flex bi bi-trash text-danger'
						style={{ fontSize: '19px', cursor: 'pointer' }}
						onClick={() => setShowDeleteUserModal(true)}
					/>
				</td>
			</tr>
		</>
	);
}

export default User;