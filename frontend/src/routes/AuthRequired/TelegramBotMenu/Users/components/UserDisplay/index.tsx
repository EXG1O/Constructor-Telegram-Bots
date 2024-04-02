import React, { ReactNode, memo } from 'react';

import { User } from 'services/api/telegram_bots/types';

import AllowButton from './components/AllowButton';
import DeleteButton from './components/DeleteButton';

export interface UserDisplayProps {
	user: User;
}

function UserDisplay({ user }: UserDisplayProps): ReactNode {
	return (
		<tr>
			<td className='text-success-emphasis'>{`[${user.activated_date}]`}</td>
			<td className='text-primary-emphasis'>{user.telegram_id}</td>
			<td className='w-100'>{user.full_name}</td>
			<td>
				<AllowButton user={user} />
			</td>
			<td>
				<DeleteButton user={user} />
			</td>
		</tr>
	);
}

export default memo(UserDisplay);