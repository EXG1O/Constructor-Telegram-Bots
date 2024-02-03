import React, { ReactElement, memo, useEffect, useState } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';

export interface Data {
	isReplyToUserMessage: boolean;
	isDeleteUserMessage: boolean;
	isSendAsNewMessage: boolean;
}

export interface SettingsProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data;
	onChange: (data: Data) => void;
}

function Settings({ initialData, onChange, ...props }: SettingsProps): ReactElement<SettingsProps> {
	const [data, setData] = useState<Data>(initialData ?? {
		isReplyToUserMessage: false,
		isDeleteUserMessage: false,
		isSendAsNewMessage: false,
	});

	useEffect(() => onChange(data), [data]);

	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Настройки')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				<Form.Switch
					checked={data.isReplyToUserMessage}
					label={gettext('Ответить на сообщение пользователя')}
					onChange={e => setData({ ...data, isReplyToUserMessage: e.target.checked })}
				/>
				<Form.Switch
					checked={data.isDeleteUserMessage}
					label={gettext('Удалить сообщение пользователя')}
					onChange={e => setData({ ...data, isDeleteUserMessage: e.target.checked })}
				/>
				<Form.Switch
					checked={data.isSendAsNewMessage}
					label={gettext('Отправить сообщение как новое')}
					onChange={e => setData({ ...data, isSendAsNewMessage: e.target.checked })}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(Settings);