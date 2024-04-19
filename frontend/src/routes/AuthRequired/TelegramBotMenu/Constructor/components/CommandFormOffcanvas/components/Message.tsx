import React, { ReactElement, memo } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';

import TelegramQuillEditor from 'components/TelegramQuillEditor';

export type Value = string;

export interface MessageProps extends Omit<CardProps, 'onChange' | 'children'> {
	value?: Value;
	onChange: (value: Value) => void;
}

export const defaultValue: Value = '';

function Message({ value = defaultValue, onChange, ...props }: MessageProps): ReactElement<MessageProps> {
	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Сообщение')}
			</Card.Header>
			<Card.Body className='p-2'>
				<TelegramQuillEditor
					height={220}
					value={value}
					placeholder={gettext('Введите текст')}
					onChange={onChange}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(Message);