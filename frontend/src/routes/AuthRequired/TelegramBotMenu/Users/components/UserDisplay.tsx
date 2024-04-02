import React, { ReactNode, memo, useCallback, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import AskConfirmModal from 'components/AskConfirmModal';

import useToast from 'services/hooks/useToast';
import useUsers from '../hooks/useUsers';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import { UserAPI } from 'services/api/telegram_bots/main';
import { User } from 'services/api/telegram_bots/types';

export interface UserDisplayProps {
	user: User;
}

function UserDisplay({ user }: UserDisplayProps): ReactNode {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	const { createMessageToast } = useToast();
	const { updateUsers } = useUsers();

	const [showDeleteUserModal, setShowDeleteUserModal] = useState<boolean>(false);
	const [loadingDeleteUserModal, setLoadingDeleteUserModal] = useState<boolean>(false);

	async function handleConfirmDelete(): Promise<void> {
		setLoadingDeleteUserModal(true);

		const response = await UserAPI._delete(telegramBot.id, user.id);

		if (response.ok) {
			updateUsers();
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
				onHide={useCallback(() => setShowDeleteUserModal(false), [])}
			>
				{gettext('Вы точно хотите удалить пользователя?')}
			</AskConfirmModal>
			<tr>
				<td className='text-success-emphasis'>{`[${user.activated_date}]`}</td>
				<td className='text-primary-emphasis'>{user.telegram_id}</td>
				<td className='w-100'>{user.full_name}</td>
				<td>
					<i
						className='d-flex bi bi-trash text-danger'
						style={{ fontSize: '18px', cursor: 'pointer' }}
						onClick={() => setShowDeleteUserModal(true)}
					/>
				</td>
			</tr>
		</>
	);
}

export default memo(UserDisplay);