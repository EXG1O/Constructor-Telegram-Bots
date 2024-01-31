import React, { ReactElement, memo, useEffect, useState } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';

export type Value = string;

export interface CommandNameProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialValue?: Value;
	onChange: (value: Value) => void;
}

function CommandName({ initialValue, onChange, ...props }: CommandNameProps): ReactElement<CommandNameProps> {
	const [value, setValue] = useState<Value>(initialValue ?? '');

	useEffect(() => onChange(value), [value]);

	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Название команды')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Form.Control
					value={value}
					placeholder={gettext('Введите название команды')}
					onChange={e => setValue(e.target.value)}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(CommandName);