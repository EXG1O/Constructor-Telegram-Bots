import React, { ReactElement, ReactNode, HTMLAttributes, memo } from 'react';

export interface InfoAreaProps extends HTMLAttributes<HTMLDivElement> {
	value: ReactNode;
}

function InfoArea({ value, children, ...props }: InfoAreaProps): ReactElement<InfoAreaProps> {
	return (
		<div {...props}>
			<div className='border border-2 rounded-4 fw-semibold p-2'>{value}</div>
			<span>{children}</span>
		</div>
	);
}

export default memo(InfoArea);