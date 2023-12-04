import Toast from 'global_modules/toast';
import { askConfirmModal } from 'global_modules/modals/ask_confirm_modal';
import { TelegramBotUserApi, TelegramBotAllowedUserApi } from 'telegram_bot_api/main';
import { TelegramBotUser } from 'telegram_bot_api/types';
import { UserListGroup } from '../main';
import React from 'react';

declare const telegramBotId: number;
declare const telegramBotIsPrivate: boolean;
declare const askConfirmModalDeleteTelegramBotUserTitle: string;
declare const askConfirmModalDeleteTelegramBotUserText: string;

const buttonWithOnlyIconStyle: React.CSSProperties = {
	fontSize: '20px',
}

interface UserListGroupItemProps {
	userInitial: TelegramBotUser;
}

export default function UserListGroupItem({userInitial}: UserListGroupItemProps): React.JSX.Element {
	const [user, setUser] = React.useState<TelegramBotUser>(userInitial);

	async function handleSetOrUnsetAllowedButtonClick(): Promise<void> {
		const response = await TelegramBotAllowedUserApi[(user.is_allowed) ? 'unset' : 'set'](telegramBotId, user.id);

		if (response.ok) {
			setUser({...user, is_allowed: !user.is_allowed});
		}

		new Toast(response.json.message, response.json.level).show();
	}

	function handleDeleteButtonClick(): void {
		askConfirmModal(
			askConfirmModalDeleteTelegramBotUserTitle,
			askConfirmModalDeleteTelegramBotUserText,
			async (): Promise<void> => {
				const response = await TelegramBotUserApi.delete_(telegramBotId, user.id);

				if (response.ok) {
					UserListGroup.update();
				}

				new Toast(response.json.message, response.json.level).show();
			},
		);
	}

	return (
		<div className='list-group-item p-3'>
			<div className='d-flex align-items-center gap-3'>
				<p className='flex-fill m-0'>[<span className='text-success-emphasis'>{user.activated_date}</span>]: <span className='text-primary'>{user.user_id}</span> - {user.full_name}</p>
				<div className='btn-group' role='group'>
					{telegramBotIsPrivate && (
						<button
							className={`btn btn-warning text-light bi bi-${user.is_allowed ? 'star-fill' : 'star'} px-2 py-0`}
							onClick={handleSetOrUnsetAllowedButtonClick}
							style={buttonWithOnlyIconStyle}
						></button>
					)}
					<button
						className='btn btn-danger bi bi-trash px-2 py-0'
						onClick={handleDeleteButtonClick}
						style={buttonWithOnlyIconStyle}
					></button>
				</div>
			</div>
		</div>
	);
}