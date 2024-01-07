import React, { ReactElement, memo } from 'react';

import Spinner, { SpinnerProps } from 'react-bootstrap/Spinner';

interface LoadingProps extends Omit<SpinnerProps, 'size' | 'animation' | 'style'> {
	size: 'xs' | 'sm' | 'md' | 'lg' | 'xl' | 'xxl';
}

function Loading({ size, ...props }: LoadingProps): ReactElement<LoadingProps> {
	return (
		<Spinner
			{...props}
			animation='border'
			style={
				size === 'xs' ? {
					width: '1.5rem',
					height: '1.5rem',
					borderWidth: '0.15rem',
				} : size === 'sm' ? {
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
				} : size === 'xl' ? {
					width: '3.5rem',
					height: '3.5rem',
					borderWidth: '0.35rem',
				} : size === 'xxl' ? {
					width: '4rem',
					height: '4rem',
					borderWidth: '0.4rem',
				} : undefined
			}
		/>
	);
}

export default memo(Loading);