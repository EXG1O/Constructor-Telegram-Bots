import React, { ReactElement, memo } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';

import TelegramQuillEditor from 'components/TelegramQuillEditor';

export type Value = string;

export interface MessageTextProps extends Omit<CardProps, 'onChange' | 'children'> {
	value?: Value;
	onChange: (value: Value) => void;
}

export const defaultValue: Value = '';

function MessageText({ value = defaultValue, onChange, ...props }: MessageTextProps): ReactElement<MessageTextProps> {
	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Текст сообщения')}
			</Card.Header>
			<Card.Body className='p-2'>
				<TelegramQuillEditor
					height={220}
					value={value}
					placeholder={gettext('Введите текст сообщения')}
					onChange={onChange}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(MessageText);