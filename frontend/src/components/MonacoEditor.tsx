import React, { ReactElement, memo, useRef, useMemo, useState } from 'react';
import classNames from 'classnames';
import monaco from 'monaco-editor';

import('./MonacoEditor.scss');

import BaseMonacoEditor, { Monaco, EditorProps as BaseMonacoEditorProps } from '@monaco-editor/react';

import Loading from './Loading';

type Size = 'sm' | 'lg';

export interface MonacoEditorProps extends Omit<BaseMonacoEditorProps, 'loading' | 'onChange'> {
	size?: Size;
	disablePadding?: boolean;
	disableFocusEffect?: boolean;
	onFocus?: () => void;
	onBlur?: () => void;
	onChange?: (value: string, ev: monaco.editor.IModelContentChangedEvent) => void
}

function MonacoEditor({
	size,
	disablePadding,
	disableFocusEffect,
	options,
	className,
	onFocus,
	onBlur,
	onChange,
	onMount,
	...props
}: MonacoEditorProps): ReactElement<MonacoEditorProps> {
	const monacoEditor = useRef<monaco.editor.IStandaloneCodeEditor | undefined>(undefined);

	const lineHeight = useMemo<number>(() => size === 'sm' ? 19 : size === 'lg' ? 24 : 22, [size]);
	const fontSize = useMemo<number>(() => size === 'sm' ? 14 : size === 'lg' ? 18 : 16, [size]);

	const [focus, setFocus] = useState<boolean>(false);

	function updateEditorLayout(): void {
		if (monacoEditor.current) {
			const monacoEditorModel: monaco.editor.ITextModel | null = monacoEditor.current.getModel();

			if (monacoEditorModel !== null) {
				monacoEditor.current.layout({
					width: monacoEditor.current.getContainerDomNode().querySelector('.monaco-editor')!.clientWidth,
					height: monacoEditorModel.getLineCount() * lineHeight,
				});
			}
		}
	}

	function handleFocus(): void {
		if (!disableFocusEffect) {
			setFocus(true);
		}

		onFocus?.();
	}

	function handleBlur(): void {
		if (!disableFocusEffect) {
			setFocus(false);
		}

		onBlur?.();
	}

	function handleChange(value: string | undefined, event: monaco.editor.IModelContentChangedEvent): void {
		if (monacoEditor.current && value !== undefined) {
			updateEditorLayout();
			onChange?.(value, event);
		}
	}

	function handleMount(editor: monaco.editor.IStandaloneCodeEditor, monaco: Monaco): void {
		monacoEditor.current = editor;

		monacoEditor.current.onDidFocusEditorText(handleFocus);
		monacoEditor.current.onDidBlurEditorText(handleBlur);

		setTimeout(() => {
			if (monacoEditor.current) {
				updateEditorLayout();
				onMount?.(monacoEditor.current, monaco);
			}
		}, 500);
	}

	return (
		<BaseMonacoEditor
			{...props}
			loading={<Loading size='sm' />}
			options={useMemo(() => ({
				minimap: { enabled: false },
				renderLineHighlight: 'none',
				lineNumbersMinChars: 3,
				overviewRulerLanes: 0,
				scrollBeyondLastLine: false,
				scrollbar: { vertical: 'hidden' },
				inlayHints: { enabled: 'off' },
				contextmenu: false,
				fontSize,
				...options,
			}), [options])}
			className={
				classNames(
					'monaco-editor-wrapper overflow-hidden border',
					{
						rounded: size === undefined,
						'rounded-1': size === 'sm',
						'rounded-3': size === 'lg',
						padding: !disablePadding,
						focus,
					},
					className,
				)
			}
			onChange={handleChange}
			onMount={handleMount}
		/>
	);
}

export default memo(MonacoEditor);