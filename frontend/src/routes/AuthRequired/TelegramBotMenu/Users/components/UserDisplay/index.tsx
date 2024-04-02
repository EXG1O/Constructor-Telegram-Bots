import React, { ReactNode, memo } from 'react';

import { User } from 'services/api/telegram_bots/types';

import AllowButton from './components/AllowButton';
import UnallowButton from './components/UnallowButton';
import BlockButton from './components/BlockButton';
import UnblockButton from './components/UnblockButton';
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
				<UnallowButton user={user} />
			</td>
			<td>
				<BlockButton user={user} />
			</td>
			<td>
				<UnblockButton user={user} />
			</td>
			<td>
				<DeleteButton user={user} />
			</td>
		</tr>
	);
}

export default memo(UserDisplay);