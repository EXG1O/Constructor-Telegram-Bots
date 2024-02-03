import React, { ReactElement } from 'react';
import Quill from 'quill';

import './TelegramTextEditor.scss';

import QuillEditor, { QuillEditorProps } from './QuillEditor';

const Inline = Quill.import('blots/inline');

class SpoilerBlot extends Inline {
	static blotName = 'spoiler';
	static tagName = 'tg-spoiler';
}

Quill.register(SpoilerBlot);

export type TelegramTextEditorProps = QuillEditorProps;

function TelegramTextEditor(props: TelegramTextEditorProps): ReactElement<TelegramTextEditorProps> {
	return (
		<QuillEditor
			{...props}
			toolbar={props.toolbar ?? {
				container: [
					'bold',
					'italic',
					'underline',
					'strike',
					'link',
					'code',
					'code-block',
					'blockquote',
					'spoiler',
					'clean',
				],
			}}
		/>
	);
}

export default TelegramTextEditor;