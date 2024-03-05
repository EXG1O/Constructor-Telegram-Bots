import React, { ReactElement, memo, useRef, useState } from 'react';
import classNames from 'classnames';
import monaco from 'monaco-editor';

import('./MonacoEditor.scss');

import _MonacoEditor, { Monaco, EditorProps as _MonacoEditorProps } from '@monaco-editor/react';

import Loading from './Loading';

import { updateEditorLayout } from 'utils/monaco_editor';

export interface MonacoEditorProps extends _MonacoEditorProps {
	disablePadding?: boolean;
	disableFocusEffect?: boolean;
}

function MonacoEditor({
	disablePadding,
	disableFocusEffect,
	onChange,
	onMount,
	...props
}: MonacoEditorProps): ReactElement<MonacoEditorProps> {
	const monacoEditor = useRef<monaco.editor.IStandaloneCodeEditor | undefined>(undefined);
	const [focus, setFocus] = useState<boolean>(false);

	function handleMonacoEditorMount(editor: monaco.editor.IStandaloneCodeEditor, monaco: Monaco): void {
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

	function handleMonacoEditorChange(value: string | undefined, event: monaco.editor.IModelContentChangedEvent): void {
		if (monacoEditor.current && value !== undefined) {
			updateEditorLayout(monacoEditor.current);
			onChange?.(value, event);
		}
	}

	return (
		<_MonacoEditor
			loading={<Loading size='sm' />}
			{...props}
			options={{
				minimap: { enabled: false },
				renderLineHighlight: 'none',
				lineNumbersMinChars: 3,
				overviewRulerLanes: 0,
				scrollBeyondLastLine: false,
				scrollbar: { vertical: 'hidden' },
				inlayHints: { enabled: 'off' },
				...props.options,
			}}
			className={
				classNames(
					'monaco-editor-wrapper overflow-hidden border rounded',
					disablePadding ? undefined : 'padding',
					focus ? 'focus' : undefined,
					props.className,
				)
			}
			onChange={handleMonacoEditorChange}
			onMount={handleMonacoEditorMount}
		/>
	);
}

export default memo(MonacoEditor);