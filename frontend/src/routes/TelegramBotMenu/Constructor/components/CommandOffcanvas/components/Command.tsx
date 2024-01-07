import React, { ReactElement, memo, useEffect, useState } from 'react';
import classNames from 'classnames';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Collapse from 'react-bootstrap/Collapse';

export interface Data {
	text: string;
	description?: string;
}

export interface CommandProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data;
	onChange: (data: Data) => void;
}

type AddonNames = 'description';

function Command({ initialData, onChange, ...props }: CommandProps): ReactElement<CommandProps> {
	const [data, setData] = useState<Data>(initialData ?? { text: '' });
	const [showAddons, setShowAddons] = useState<Record<AddonNames, boolean>>({ description: Boolean(initialData?.description) });

	useEffect(() => onChange(data), [data]);

	function toggleAddon(name: AddonNames): void {
		setShowAddons({ ...showAddons, [name]: !showAddons[name] });

		if (showAddons[name]) {
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
					{...(
						showAddons.description ? {
							variant: 'secondary',
							className: 'w-100 border-bottom-0 rounded-bottom-0',
							children: gettext('Убрать из меню'),
						} : {
							variant: 'dark',
							className: 'w-100',
							children: gettext('Добавить в меню'),
						}
					)}
					aria-controls='command-offcanvas-command-description-addon'
					aria-expanded={showAddons.description}
					onClick={() => toggleAddon('description')}
				/>
				<Collapse in={showAddons.description}>
					<div id='command-offcanvas-command-description-addon'>
						<Form.Control
							value={data.description ?? ''}
							className='border-top-0 rounded-top-0'
							placeholder={gettext('Введите описание команды')}
							onChange={e => setData({ ...data, description: e.target.value })}
						/>
					</div>
				</Collapse>
			</Card.Body>
		</Card>
	);
}

export default memo(Command);