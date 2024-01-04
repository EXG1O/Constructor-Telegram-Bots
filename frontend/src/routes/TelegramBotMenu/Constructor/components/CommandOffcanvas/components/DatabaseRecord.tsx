import React, { ReactElement, memo, useEffect, useRef, useState } from 'react';
import classNames from 'classnames';
import monaco from 'monaco-editor';

import Card, { CardProps } from 'react-bootstrap/Card';
import MonacoEditor from '@monaco-editor/react';

import { updateEditorLayout, defaultEditorOptions } from 'utils/monaco_editor';

export interface DatabaseRecordProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialValue?: string | null;
	onChange: (value: string) => void;
}

function DatabaseRecord({ initialValue, onChange, ...props }: DatabaseRecordProps): ReactElement<DatabaseRecordProps> {
	const [value, setValue] = useState<string>(initialValue ?? JSON.stringify({ key: 'value' }, undefined, 4));

	const monacoEditor = useRef<monaco.editor.IStandaloneCodeEditor | undefined>(undefined);

	useEffect(() => onChange(value), [value]);

	function handleMonacoEditorMount(editor: monaco.editor.IStandaloneCodeEditor): void {
		monacoEditor.current = editor;

		setTimeout(() => {
			if (monacoEditor.current) {
				updateEditorLayout(monacoEditor.current);
			}
		}, 250);
	}

	function handleMonacoEditorChange(value?: string): void {
		if (monacoEditor.current && value !== undefined) {
			setValue(value);

			updateEditorLayout(monacoEditor.current);
		}
	}

	return (
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Запись в базу данных')}
			</Card.Header>
			<Card.Body className='p-2'>
				<MonacoEditor
					defaultLanguage='json'
					defaultValue={value}
					options={{
						...defaultEditorOptions,
						glyphMargin: false,
						folding: false,
						lineNumbers: 'off',
						lineDecorationsWidth: 0,
						lineNumbersMinChars: 0,
					}}
					className='overflow-hidden border rounded p-2'
					onMount={editor => handleMonacoEditorMount(editor)}
					onChange={value => handleMonacoEditorChange(value)}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(DatabaseRecord);