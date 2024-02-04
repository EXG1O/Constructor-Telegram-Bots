import React, { ReactElement, memo } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';

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
				{gettext('Название команды')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Form.Control
					value={value}
					placeholder={gettext('Введите название команды')}
					onChange={e => onChange(e.target.value)}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(Name);