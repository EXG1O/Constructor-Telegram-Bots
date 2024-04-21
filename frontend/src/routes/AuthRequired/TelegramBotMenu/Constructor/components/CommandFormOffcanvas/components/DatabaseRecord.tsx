import React, { ReactElement, memo, useCallback, useMemo } from 'react';

import MonacoEditor, { MonacoEditorProps } from 'components/MonacoEditor';

import Block, { BlockProps } from '../../Block';

export type Value = string;

export interface DatabaseRecordProps extends Omit<BlockProps, 'title' | 'onChange' | 'children'> {
	value?: Value;
	onChange: (value: Value) => void;
}

export const defaultValue: Value = JSON.stringify({ key: 'value' }, undefined, 4);

function DatabaseRecord({ value = defaultValue, onChange, ...props }: DatabaseRecordProps): ReactElement<DatabaseRecordProps> {
	return (
		<Block {...props} title={gettext('Запись в базу данных')}>
			<Block.Body>
				<MonacoEditor
					value={value}
					defaultLanguage='json'
					options={useMemo(() => ({
						glyphMargin: false,
						folding: false,
						lineNumbers: 'off',
						lineDecorationsWidth: 0,
						lineNumbersMinChars: 0,
					}), [])}
					onChange={useCallback<NonNullable<MonacoEditorProps['onChange']>>(
						(editor, newValue) => onChange(newValue),
						[],
					)}
				/>
			</Block.Body>
		</Block>
	);
}

export default memo(DatabaseRecord);