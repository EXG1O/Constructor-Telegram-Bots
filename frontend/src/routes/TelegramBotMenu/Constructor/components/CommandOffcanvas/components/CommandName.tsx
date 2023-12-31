import React, { ReactElement, useEffect, useState } from 'react';
import classNames from 'classnames';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';

export interface Data {
	text: string;
}

export interface CommandNameProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data | null;
	onChange: (data: Data) => void;
}

function CommandName({ initialData, onChange, ...props }: CommandNameProps): ReactElement<CommandNameProps> {
	const [data, setData] = useState<Data>(initialData ?? { text: '' });

	useEffect(() => onChange(data), [data]);

	return (
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Название команды')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Form.Control
					value={data.text}
					placeholder={gettext('Введите название команды')}
					onChange={e => setData({ ...data, text: e.target.value })}
				/>
			</Card.Body>
		</Card>
	);
}

export default CommandName;