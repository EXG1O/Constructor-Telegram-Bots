import React, { ReactNode, useEffect, useState } from 'react';

import Card from 'react-bootstrap/Card';
import Stack from 'react-bootstrap/Stack';
import Form from 'react-bootstrap/Form';

export type AddonsName = 'description';

export interface Data {
	text: string;
	description?: string;
}

export interface CommandProps {
	initialData?: Data;
	onChange: (data: Data) => void;
}

function Command({ initialData, onChange }: CommandProps): ReactNode {
	const [data, setData] = useState<Data>(initialData ?? { text: '' });
	const [addons, setAddons] = useState<Record<AddonsName, boolean>>({ description: Boolean(initialData?.description) });

	useEffect(() => onChange(data), [data]);

	function toggleAddon(name: AddonsName): void {
		setAddons({ ...addons, [name]: !addons[name] });

		if (addons[name]) {
			setData({ ...data, [name]: undefined });
		}
	}

	return (
		<Card className='border'>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Команда')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Stack gap={2}>
					<Form.Control
						value={data.text}
						placeholder={gettext('Введите команду')}
						onChange={e => setData({ ...data, text: e.target.value })}
					/>
					<Form.Switch
						checked={addons.description}
						label={gettext('Добавить в меню')}
						className='mb-0'
						style={{ width: 'max-content' }}
						onChange={() => toggleAddon('description')}
					/>
					{addons.description && (
						<Form.Control
							value={data.description ?? ''}
							placeholder={gettext('Введите описание команды')}
							onChange={e => setData({ ...data, description: e.target.value })}
						/>
					)}
				</Stack>
			</Card.Body>
		</Card>
	);
}

export default Command;