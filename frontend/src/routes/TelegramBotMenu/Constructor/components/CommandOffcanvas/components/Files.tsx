import React, { ReactElement, ChangeEvent as ReactChangeEvent, memo, useEffect, useState } from 'react';
import classNames from 'classnames';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';

import useToast from 'services/hooks/useToast';

export interface Data {
	files?: File[] | null;
}

export interface FilesProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data | null;
	onChange: (data: Data) => void;
}

function Files({ initialData, onChange, ...props }: FilesProps): ReactElement<FilesProps> {
	const { createMessageToast } = useToast();

	const [data, setData] = useState<Data>(initialData ?? {});

	useEffect(() => onChange(data), [data]);

	function handleFilesChange(event: ReactChangeEvent<HTMLInputElement>): void {
		if (event.target.files) {
			const files: File[] = []

			for (const file of event.target.files) {
				if (file.size < 3145728) {
					files.push(file);
				} else {
					createMessageToast({ message: interpolate(
						gettext('Файл %(name)s весит больше 3МБ!'),
						{ name: file.name },
						true,
					), level: 'danger' });
				}
			}

			setData({ ...data, files });
		}
	}

	return (
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Файлы')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				<Form.Control
					type='file'
					multiple
					onChange={handleFilesChange}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(Files);