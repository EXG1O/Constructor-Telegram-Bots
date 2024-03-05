import React, { ReactElement, memo } from 'react';

import Spinner, { SpinnerProps } from 'react-bootstrap/Spinner';

export interface LoadingProps extends Omit<SpinnerProps, 'size' | 'animation' | 'style'> {
	size?: keyof typeof multipliers;
}

const multipliers = { 'xs': 1, 'sm': 2, 'md': 3, 'lg': 4, 'xl': 5 };

function Loading({ size, ...props }: LoadingProps): ReactElement<LoadingProps> {
	const multiplier: number | undefined = size && multipliers[size];

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