import React, { ReactElement, memo, useEffect, useRef, useState } from 'react';
import classNames from 'classnames';

import('./QuillEditor.scss');

import Quill, { Sources } from 'quill';
import ReactQuill, { ReactQuillProps, UnprivilegedEditor, Range } from 'react-quill';

export type QuillEditor = Quill & ReactQuill;

export interface QuillEditorToolbar {
	container: string[];
	handlers?: Record<string, (value: any) => void>;
}

export interface QuillEditorProps extends Omit<ReactQuillProps, 'modules' | 'children'> {
	height?: number;
	toolbar: QuillEditorToolbar;
	onMount?: (quillEditor: QuillEditor) => void;
}

function QuillEditor({
	height,
	toolbar,
	onFocus,
	onBlur,
	onMount,
	...props
}: QuillEditorProps): ReactElement<QuillEditorProps> {
	const quillRef = useRef<Quill | undefined>(undefined);
    const reactQuillRef = useRef<ReactQuill | null>(null);
	const [focus, setFocus] = useState<boolean>(false);

	useEffect(() => {
		if (!reactQuillRef.current) {
			throw Error('reactQuillRef should not be null!');
		}

		quillRef.current = reactQuillRef.current.getEditor() as unknown as Quill;

		if (height !== undefined) {
			quillRef.current.root.style.height = `${height}px`;
		}

		onMount?.(Object.assign(quillRef.current, reactQuillRef.current));
	}, []);

	function handleFocus(selection: Range, source: Sources, editor: UnprivilegedEditor): void {
		setFocus(true);
		onFocus?.(selection, source, editor);
	}

	function handleBlur(selection: Range, source: Sources, editor: UnprivilegedEditor): void {
		setFocus(false);
		onBlur?.(selection, source, editor);
	}

	return (
		<ReactQuill
			ref={reactQuillRef}
			{...props}
			modules={{ toolbar }}
			className={
				classNames(
					'border rounded',
					focus ? 'focus' : undefined,
					props.className,
				)
			}
			onFocus={handleFocus}
			onBlur={handleBlur}
		/>
	);
}

export default memo(QuillEditor);