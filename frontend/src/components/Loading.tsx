import React, { ReactElement, memo } from 'react';

import Spinner, { SpinnerProps } from 'react-bootstrap/Spinner';

interface LoadingProps extends Omit<SpinnerProps, 'size' | 'animation' | 'style'> {
	size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl';
}

function Loading({ size, ...props }: LoadingProps): ReactElement<LoadingProps> {
	let multiplier: number | undefined;

	switch (size) {
		case 'xs':
			multiplier = 1;
			break;
		case 'sm':
			multiplier = 2;
			break;
		case 'md':
			multiplier = 3;
			break;
		case 'lg':
			multiplier = 4;
			break;
		case 'xl':
			multiplier = 5;
			break;
	}

	return (
		<Spinner
			{...props}
			animation='border'
			style={
				multiplier ? {
					width: `${1 + 0.5 * multiplier}rem`,
					height: `${1 + 0.5 * multiplier}rem`,
					borderWidth: `${0.1 + 0.05 * multiplier}rem`,
				} : undefined
			}
		/>
	);
}

export default memo(Loading);