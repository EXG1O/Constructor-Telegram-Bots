import React, { HTMLAttributes, ReactNode } from 'react';

export interface InfoAreaProps extends HTMLAttributes<HTMLDivElement> {
	description: ReactNode;
}

function InfoArea({ description, children, ...divProps }: InfoAreaProps): ReactNode {
	return (
		<div {...divProps}>
			<div className='border border-2 rounded-4 fw-semibold p-2'>{children}</div>
			<span>{description}</span>
		</div>
	);
}

export default InfoArea;