import React, { ReactElement, memo } from 'react';

import Spinner, { SpinnerProps } from 'react-bootstrap/Spinner';

interface LoadingProps extends Omit<SpinnerProps, 'size' | 'animation' | 'style'> {
	size: 'sm' | 'md' | 'lg';
}

function Loading({ size, ...props }: LoadingProps): ReactElement<LoadingProps> {
	return (
		<Spinner
			{...props}
			animation='border'
			style={
				size === 'sm' ? {
					width: '2rem',
					height: '2rem',
					borderWidth: '0.2rem',
				} : size === 'md' ? {
					width: '2.5rem',
					height: '2.5rem',
					borderWidth: '0.25rem',
				} : size === 'lg' ? {
					width: '3rem',
					height: '3rem',
					borderWidth: '0.3rem',
				} : undefined
			}
		/>
	);
}

export default memo(Loading);