import React, { ReactNode, useEffect, useState } from 'react';

import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';

export interface Data {
	text: string;
}

export interface CommandNameProps {
	initialData?: Data;
	onChange: (data: Data) => void;
}

function CommandName({ initialData, onChange }: CommandNameProps): ReactNode {
	const [data, setData] = useState<Data>(initialData ?? { text: '' });

	useEffect(() => onChange(data), [data]);

	return (
		<Card className='border'>
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