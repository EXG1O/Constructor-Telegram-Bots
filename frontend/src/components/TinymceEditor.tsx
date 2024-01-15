import React, { ReactElement } from 'react';

import 'tinymce/tinymce';
import 'tinymce/models/dom/model';
import 'tinymce/themes/silver';
import 'tinymce/icons/default';
import 'tinymce/skins/ui/oxide/skin.min.css';
import './TinymceEditor.css';

import { Editor, IAllProps } from '@tinymce/tinymce-react';

export type TinymceEditorProps = IAllProps;

function TinymceEditor(props: TinymceEditorProps): ReactElement<TinymceEditorProps> {
	return (
		<Editor
			{...props}
			init={{
				height: 260,
				...props.init,
				toolbar: 'bold italic underline strikethrough',
				formats: { underline: { inline: 'u' }, ...props.init?.formats },
				newline_behavior: 'linebreak',
				menubar: false,
				statusbar: false,
				resize: false,
				promotion: false,
				skin: false,
				content_css: false,
				content_style: `
					body {
						font-family: system-ui, -apple-system, "Segoe UI", Roboto, "Helvetica Neue", "Noto Sans", "Liberation Sans", Arial, sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
						margin: 6px 12px;
					}

					body[data-mce-placeholder]:not(.mce-visualblocks)::before {
						color: rgba(34, 47, 62, 0.7);
						content: attr(data-mce-placeholder);
						position: absolute;
					}

					p {
						margin: 0px;
					}
				` + props.init?.content_style ?? '',
			}}
		/>
	);
}

export default TinymceEditor;