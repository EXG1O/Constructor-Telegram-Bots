import React, { ReactElement, useEffect, useRef, useState } from 'react';
import classNames from 'classnames';

import './QuillEditor.scss';

import Quill, { Sources } from 'quill';
import ReactQuill, { ReactQuillProps, UnprivilegedEditor } from 'react-quill';

export interface QuillEditorToolbar {
	container: string[];
	handlers?: Record<string, (value: any) => void>;
}

export interface QuillEditorProps extends Omit<ReactQuillProps, 'modules' | 'onFocus' | 'onBlur' | 'children'> {
	height?: number;
	toolbar: QuillEditorToolbar;
	onMount?: (quill: Quill, reactQuill: ReactQuill) => void;
}

export type DeltaStatic = Parameters<NonNullable<ReactQuillProps['onChange']>>[1];

function QuillEditor({ height, toolbar, onMount, onChange, ...props }: QuillEditorProps): ReactElement<QuillEditorProps> {
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

		onMount?.(quillRef.current, reactQuillRef.current);
	}, []);

	function handleChange(value: string, delta: DeltaStatic, source: Sources, editor: UnprivilegedEditor): void {
		if (quillRef.current && onChange) {
			onChange(
				Object.values(quillRef.current.root.children).reduce<string[]>((lines, children) => {
					let html: string | undefined;

					if (children.tagName === 'P') {
						html = children.innerHTML;

						if (html === '<br>') {
							html = '';
						}
					} else if (children.tagName === 'PRE') {
						html = children.outerHTML.replace(' class="ql-syntax" spellcheck="false"', '');
					} else if (children.tagName === 'BLOCKQUOTE') {
						html = children.outerHTML;
					}

					if (html !== undefined) {
						lines.push(html.replaceAll(/&nbsp;|\s*rel="noopener noreferrer"\s+target="_blank"\s*|\<span\s+class="ql.*"\s*\>.*\<\/span\>/gi, ''));
					}

					return lines;
				}, []).join('<br>'),
				delta,
				source,
				editor,
			);
		}
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
			onFocus={() => setFocus(true)}
			onBlur={() => setFocus(false)}
			onChange={handleChange}
		/>
	);
}

export default QuillEditor;