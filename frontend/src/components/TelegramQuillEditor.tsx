import React, { ReactElement, memo } from 'react';
import Quill from 'quill';

import('./TelegramQuillEditor.scss');

import QuillEditor, { QuillEditorProps } from './QuillEditor';

const Inline = Quill.import('blots/inline');

class SpoilerBlot extends Inline {
	static blotName = 'spoiler';
	static tagName = 'tg-spoiler';
}

Quill.register(SpoilerBlot);

export interface TelegramQuillEditorProps extends Omit<QuillEditorProps, 'toolbar'> {
	toolbar?: QuillEditorProps['toolbar'];
}

function TelegramQuillEditor(props: TelegramQuillEditorProps): ReactElement<TelegramQuillEditorProps> {
	return (
		<QuillEditor
			toolbar={{
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
			{...props}
		/>
	);
}

export default memo(TelegramQuillEditor);