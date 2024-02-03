import React, { ReactElement, memo } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';

import TelegramQuillEditor from 'components/TelegramQuillEditor';

export type Value = string;

export interface MessageTextProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialValue?: Value;
	onChange: (value: Value) => void;
}

function MessageText({ initialValue, onChange, ...props }: MessageTextProps): ReactElement<MessageTextProps> {
	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Текст сообщения')}
			</Card.Header>
			<Card.Body className='p-2'>
				<TelegramQuillEditor
					defaultValue={initialValue}
					placeholder={gettext('Введите текст сообщения')}
					style={{ height: 260 }}
					onChange={onChange}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(MessageText);