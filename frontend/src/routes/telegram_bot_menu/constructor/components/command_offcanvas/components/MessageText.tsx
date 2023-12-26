import 'tinymce/tinymce';
import 'tinymce/models/dom/model';
import 'tinymce/themes/silver';
import 'tinymce/icons/default';
import 'tinymce/skins/ui/oxide/skin.min.css';
import './MessageText.css';

import React, { ReactNode, useEffect, useState } from 'react';

import { Editor } from '@tinymce/tinymce-react';
import Card from 'react-bootstrap/Card';

export interface Data {
	text: string;
}

export interface MessageTextProps {
	onChange: (data: Data) => void;
}

function MessageText({ onChange }: MessageTextProps): ReactNode {
	const [data, setData] = useState<Data>({ text: '' });

	useEffect(() => onChange(data), [data]);

	return (
		<Card className='border'>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Текст сообщения')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Editor
					value={data.text}
					init={{
						skin: false,
						content_css: false,
						height: 260,
						placeholder: gettext('Введите текст сообщения'),
						newline_behavior: 'linebreak',
						toolbar: 'bold italic underline strikethrough',
						formats: { underline: { inline: 'u' } },
						menubar: false,
						promotion: false,
						statusbar: false,
						resize: false,
					}}
					onEditorChange={text => setData({ ...data, text })}
				/>
			</Card.Body>
		</Card>
	);
}

export default MessageText;