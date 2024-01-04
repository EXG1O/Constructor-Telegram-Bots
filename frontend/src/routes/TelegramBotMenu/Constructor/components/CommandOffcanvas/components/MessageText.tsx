import 'tinymce/tinymce';
import 'tinymce/models/dom/model';
import 'tinymce/themes/silver';
import 'tinymce/icons/default';
import 'tinymce/skins/ui/oxide/skin.min.css';
import './MessageText.css';

import React, { ReactElement, memo, useEffect, useState } from 'react';
import classNames from 'classnames';

import { Editor } from '@tinymce/tinymce-react';
import Card, { CardProps } from 'react-bootstrap/Card';

export interface MessageTextProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialValue?: string | null;
	onChange: (value: string) => void;
}

function MessageText({ initialValue, onChange, ...props }: MessageTextProps): ReactElement<MessageTextProps> {
	const [value, setValue] = useState<string>(initialValue ?? '');

	useEffect(() => onChange(value), [value]);

	return (
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Текст сообщения')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Editor
					value={value}
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
					onEditorChange={value => setValue(value)}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(MessageText);