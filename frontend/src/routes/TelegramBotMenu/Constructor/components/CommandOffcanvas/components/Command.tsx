import React, { ReactElement, useEffect, useState } from 'react';
import classNames from 'classnames';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Collapse from 'react-bootstrap/Collapse';

export type AddonsName = 'description';

export interface Data {
	text: string;
	description?: string | null;
}

export interface CommandProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data | null;
	onChange: (data: Data) => void;
}

function Command({ initialData, onChange, ...props }: CommandProps): ReactElement<CommandProps> {
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
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Команда')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Form.Control
					className='mb-2'
					value={data.text}
					placeholder={gettext('Введите команду')}
					onChange={e => setData({ ...data, text: e.target.value })}
				/>
				<Button
					size='sm'
					variant={addons.description ? 'secondary' : 'dark'}
					className='w-100'
					aria-controls='command-offcanvas-command-description-addon'
					aria-expanded={addons.description}
					onClick={() => toggleAddon('description')}
				>
					{gettext('Добавить в меню')}
				</Button>
				<Collapse in={addons.description}>
					<div id='command-offcanvas-command-description-addon'>
						<Form.Control
							className='mt-2'
							value={data.description ?? ''}
							placeholder={gettext('Введите описание команды')}
							onChange={e => setData({ ...data, description: e.target.value })}
						/>
					</div>
				</Collapse>
			</Card.Body>
		</Card>
	);
}

export default Command;