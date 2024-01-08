import React, { ReactElement, memo, useEffect, useState } from 'react';
import classNames from 'classnames';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';

export interface CommandNameProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialValue?: string;
	onChange: (value: string) => void;
}

function CommandName({ initialValue, onChange, ...props }: CommandNameProps): ReactElement<CommandNameProps> {
	const [value, setValue] = useState<string>(initialValue ?? '');

	useEffect(() => onChange(value), [value]);

	return (
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
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