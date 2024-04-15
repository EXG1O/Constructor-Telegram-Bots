import React, { ReactElement, memo, useState } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Collapse from 'react-bootstrap/Collapse';

export interface Data {
	text: string;
	description?: string;
}

export interface TriggerProps extends Omit<CardProps, 'onChange' | 'children'> {
	data?: Data;
	onChange: (data: Data) => void;
}

export const defaultData: Data = { text: '' };

function Trigger({ data = defaultData, onChange, ...props }: TriggerProps): ReactElement<TriggerProps> {
	const [showDescription, setShowDescription] = useState<boolean>(Boolean(data?.description));

	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Триггер')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Form.Control
					className='mb-2'
					value={data.text}
					placeholder={gettext('Введите текст')}
					onChange={e => onChange({ ...data, text: e.target.value })}
				/>
				<Button
					size='sm'
					{...(
						showDescription ? {
							variant: 'secondary',
							className: 'w-100 border-bottom-0 rounded-bottom-0',
							children: gettext('Убрать из меню'),
						} : {
							variant: 'dark',
							className: 'w-100',
							children: gettext('Добавить в меню'),
						}
					)}
					aria-controls='command-offcanvas-trigger-description-addon'
					aria-expanded={showDescription}
					onClick={() => setShowDescription(!showDescription)}
				/>
				<Collapse
					in={showDescription}
					unmountOnExit
					onExited={() => onChange({ ...data, description: undefined })}
				>
					<div id='command-offcanvas-trigger-description-addon'>
						<Form.Control
							value={data.description ?? ''}
							className='border-top-0 rounded-1 rounded-top-0'
							placeholder={gettext('Введите описание')}
							onChange={e => onChange({ ...data, description: e.target.value })}
						/>
					</div>
				</Collapse>
			</Card.Body>
		</Card>
	);
}

export default memo(Trigger);