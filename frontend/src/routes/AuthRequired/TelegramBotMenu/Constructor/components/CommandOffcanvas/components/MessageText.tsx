import React, { ReactElement, memo, useEffect, useState } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';

import TinymceEditor from 'components/TinymceEditor';

export interface MessageTextProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialValue?: string;
	onChange: (value: string) => void;
}

function MessageText({ initialValue, onChange, ...props }: MessageTextProps): ReactElement<MessageTextProps> {
	const [value, setValue] = useState<string>(initialValue ?? '');

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