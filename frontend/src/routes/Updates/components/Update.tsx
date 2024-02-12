import React, { ReactElement, HTMLAttributes } from 'react';
import classNames from 'classnames';

import './Update.scss';

import { Update as _Update } from 'services/api/updates/types';

export interface UpdateProps extends Omit<HTMLAttributes<HTMLDivElement>, 'dangerouslySetInnerHTML'> {
	update: _Update;
}

function Update({ update, ...props }: UpdateProps): ReactElement<UpdateProps> {
	return (
		<div
			{...props}
			className={classNames('update-block border rounded p-3', props.className)}
			dangerouslySetInnerHTML={{ __html: update.description }}
		/>
	);
}

export default Update;