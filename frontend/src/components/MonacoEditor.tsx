import React, { ReactElement, memo, useRef, useState } from 'react';
import classNames from 'classnames';
import monaco from 'monaco-editor';

import('./MonacoEditor.scss');

import BaseMonacoEditor, { Monaco, EditorProps as BaseMonacoEditorProps } from '@monaco-editor/react';

import Loading from './Loading';

import { updateEditorLayout } from 'utils/monaco_editor';

export interface MonacoEditorProps extends Omit<BaseMonacoEditorProps, 'onChange'> {
	disablePadding?: boolean;
	disableFocusEffect?: boolean;
	onChange?: (value: string, ev: monaco.editor.IModelContentChangedEvent) => void
}

function MonacoEditor({
	disablePadding,
	disableFocusEffect,
	options,
	className,
	onChange,
	onMount,
	...props
}: MonacoEditorProps): ReactElement<MonacoEditorProps> {
	const monacoEditor = useRef<monaco.editor.IStandaloneCodeEditor | undefined>(undefined);

	const [focus, setFocus] = useState<boolean>(false);

	function handleMount(editor: monaco.editor.IStandaloneCodeEditor, monaco: Monaco): void {
		if (!disableFocusEffect) {
			editor.onDidFocusEditorText(() => setFocus(true));
			editor.onDidBlurEditorText(() => setFocus(false));
		}

		monacoEditor.current = editor;

		setTimeout(() => {
			if (monacoEditor.current) {
				updateEditorLayout(monacoEditor.current);
				onMount?.(editor, monaco);
			}
		}, 500);
	}

	function handleChange(value: string | undefined, event: monaco.editor.IModelContentChangedEvent): void {
		if (monacoEditor.current && value !== undefined) {
			updateEditorLayout(monacoEditor.current);
			onChange?.(value, event);
		}
	}

	return (
		<BaseMonacoEditor
			{...props}
			loading={<Loading size='sm' />}
			options={{
				minimap: { enabled: false },
				renderLineHighlight: 'none',
				lineNumbersMinChars: 3,
				overviewRulerLanes: 0,
				scrollBeyondLastLine: false,
				scrollbar: { vertical: 'hidden' },
				inlayHints: { enabled: 'off' },
				...options,
			}}
			className={
				classNames(
					'monaco-editor-wrapper overflow-hidden border rounded',
					{ padding: !disablePadding, focus },
					className,
				)
			}
			onChange={handleChange}
			onMount={handleMount}
		/>
	);
}

export default memo(MonacoEditor);