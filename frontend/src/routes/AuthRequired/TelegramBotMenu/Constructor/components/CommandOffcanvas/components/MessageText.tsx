import React, { ReactElement, memo, useEffect, useState } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';

import TinymceEditor from 'components/TinymceEditor';

export type Value = string;

export interface MessageTextProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialValue?: Value;
	onChange: (value: Value) => void;
}

function MessageText({ initialValue, onChange, ...props }: MessageTextProps): ReactElement<MessageTextProps> {
	const [value, setValue] = useState<Value>(initialValue ?? '');

	useEffect(() => onChange(value), [value]);

	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Текст сообщения')}
			</Card.Header>
			<Card.Body className='p-2'>
				<TinymceEditor
					value={value}
					init={{ placeholder: gettext('Введите текст сообщения') }}
					onEditorChange={value => setValue(value)}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(MessageText);