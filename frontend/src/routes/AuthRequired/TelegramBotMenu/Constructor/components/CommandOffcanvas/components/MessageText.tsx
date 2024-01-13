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
	initialValue?: string;
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
						toolbar: 'bold italic underline strikethrough',
						placeholder: gettext('Введите текст сообщения'),
						formats: { underline: { inline: 'u' } },
						newline_behavior: 'linebreak',
						menubar: false,
						promotion: false,
						statusbar: false,
						resize: false,
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
						`,
					}}
					onEditorChange={value => setValue(value)}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(MessageText);