import React, { ReactElement, memo, useEffect, useState } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';

import MonacoEditor from 'components/MonacoEditor';

export type Value = string;

export interface DatabaseRecordProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialValue?: Value;
	onChange: (value: Value) => void;
}

const defaultValue = JSON.stringify({ key: 'value' }, undefined, 4);

function DatabaseRecord({ initialValue, onChange, ...props }: DatabaseRecordProps): ReactElement<DatabaseRecordProps> {
	const [value, setValue] = useState<Value>(initialValue ?? defaultValue);

	useEffect(() => onChange(value), [value]);

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
					onChange={value => setValue(value ?? defaultValue)}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(DatabaseRecord);