import React, { ReactElement, memo } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';

import MonacoEditor from 'components/MonacoEditor';

export type Value = string;

export interface DatabaseRecordProps extends Omit<CardProps, 'onChange' | 'children'> {
	value?: Value;
	onChange: (value: Value) => void;
}

export const defaultValue = JSON.stringify({ key: 'value' }, undefined, 4);

function DatabaseRecord({ value = defaultValue, onChange, ...props }: DatabaseRecordProps): ReactElement<DatabaseRecordProps> {
	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Запись в базу данных')}
			</Card.Header>
			<Card.Body className='p-2'>
				<MonacoEditor
					value={value}
					defaultLanguage='json'
					options={{
						glyphMargin: false,
						folding: false,
						lineNumbers: 'off',
						lineDecorationsWidth: 0,
						lineNumbersMinChars: 0,
					}}
					onChange={value => onChange(value ?? defaultValue)}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(DatabaseRecord);