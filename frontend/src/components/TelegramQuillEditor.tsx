import React, { ReactElement, memo, useMemo } from 'react';
import Quill from 'quill';

import('./TelegramQuillEditor.scss');

import QuillEditor, { QuillEditorProps } from './QuillEditor';

const Inline = Quill.import('blots/inline');

class SpoilerBlot extends Inline {
	static blotName = 'spoiler';
	static tagName = 'tg-spoiler';
}

Quill.register(SpoilerBlot);

export type TelegramQuillEditorProps = Omit<QuillEditorProps, 'toolbar'>;

function TelegramQuillEditor(props: TelegramQuillEditorProps): ReactElement<TelegramQuillEditorProps> {
	const toolbar = useMemo<QuillEditorProps['toolbar']>(() => ({
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
	}), []);

	return <QuillEditor {...props} toolbar={toolbar} />;
}

export default memo(TelegramQuillEditor);