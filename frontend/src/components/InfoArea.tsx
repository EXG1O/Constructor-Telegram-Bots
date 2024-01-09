import React, { ReactElement, ReactNode, HTMLAttributes, memo } from 'react';

export interface InfoAreaProps extends Omit<HTMLAttributes<HTMLDivElement>, 'children'> {
	value: ReactNode;
	description: ReactNode;
}

function InfoArea({ description, value, ...props }: InfoAreaProps): ReactElement<InfoAreaProps> {
	return (
		<div {...props}>
			<div className='border border-2 rounded-4 fw-semibold p-2'>{value}</div>
			<span>{description}</span>
		</div>
	);
}

export default memo(InfoArea);