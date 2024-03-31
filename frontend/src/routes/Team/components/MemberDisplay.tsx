import React, { ReactElement, HTMLAttributes } from 'react';
import classNames from 'classnames';

import './MemberDisplay.scss';

import { Member } from 'services/api/team/types';

export interface MemberDisplayProps extends Omit<HTMLAttributes<HTMLDivElement>, 'children'> {
	member: Member;
}

function MemberDisplay({ member, className, ...props }: MemberDisplayProps): ReactElement<MemberDisplayProps> {
	return (
		<div {...props} className={classNames('team-member d-flex flex-column align-items-center', className)}>
			<img src={member.image} className='mb-1' />
			<a
				className='h5 link-dark link-underline-opacity-0 fw-semibold mb-0'
				href={`tg://resolve?domain=${member.username}`}
			>
				{member.username}
			</a>
			<span>{member.speciality}</span>
		</div>
	);
}

export default MemberDisplay;