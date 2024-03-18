import React, { ReactElement, memo } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';
import Input from 'react-bootstrap/FormControl';

export type Value = string;

export interface NameProps extends Omit<CardProps, 'onChange' | 'children'> {
	value?: Value;
	onChange: (value: Value) => void;
}

export const defaultValue: Value = '';

function Name({ value = defaultValue, onChange, ...props }: NameProps): ReactElement<NameProps> {
	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Название')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Input
					value={value}
					placeholder={gettext('Введите название')}
					onChange={e => onChange(e.target.value)}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(Name);