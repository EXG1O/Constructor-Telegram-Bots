import React, { ReactElement, HTMLAttributes } from 'react';
import classNames from 'classnames';

import './Member.scss';

import { TeamMember } from 'services/api/team/types';

export interface MemberProps extends Omit<HTMLAttributes<HTMLDivElement>, 'children'> {
	member: TeamMember;
}

function Member({ member, ...props }: MemberProps): ReactElement<MemberProps> {
	return (
		<div {...props} className={classNames('team-member d-flex flex-column align-items-center', props.className)}>
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

export default Member;