import React, { ReactElement, memo, useCallback } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';

import TelegramQuillEditor from 'components/TelegramQuillEditor';

export interface Data {
	text: string;
}

export interface MessageProps extends Omit<CardProps, 'onChange' | 'children'> {
	data?: Data;
	onChange: (data: Data) => void;
}

export const defaultData: Data = { text: '' };

function Message({ data = defaultData, onChange, ...props }: MessageProps): ReactElement<MessageProps> {
	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Сообщение')}
			</Card.Header>
			<Card.Body className='p-2'>
				<TelegramQuillEditor
					height={220}
					value={data.text}
					placeholder={gettext('Введите текст')}
					onChange={useCallback((text: string) => onChange({ ...data, text }), [])}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(Message);