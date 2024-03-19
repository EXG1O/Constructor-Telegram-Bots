import React, { ReactElement, memo } from 'react';
import classNames from 'classnames';

import Button, { ButtonProps } from 'react-bootstrap/Button';

export type AddButtonProps = ButtonProps;

type SizeOptions = Record<NonNullable<ButtonProps['size']>, number>;

const sizePaddingStart: SizeOptions = { 'sm': 1, 'lg': 2 };
const sizeIconFontSize: SizeOptions = { 'sm': 21, 'lg': 30 };

function AddButton({ size, children, ...props }: ButtonProps): ReactElement<ButtonProps> {
	const paddingStart: number = size ? sizePaddingStart[size] : 2;
	const iconFontSize: number = size ? sizeIconFontSize[size] : 24;

	return (
		<Button
			size={size}
			{...props}
			className={classNames(`d-flex ps-${paddingStart}`, props.className)}
		>
			<i className='d-flex bi bi-plus' style={{ fontSize: `${iconFontSize}px` }} />
			{children}
		</Button>
	);
}

export default memo(AddButton);