import React, { ReactElement, ChangeEvent as ReactChangeEvent, useEffect, useState } from 'react';
import classNames from 'classnames';

import Card, { CardProps } from 'react-bootstrap/Card';
import RBImage from 'react-bootstrap/Image';
import Form from 'react-bootstrap/Form';

import useToast from 'services/hooks/useToast';

export interface Data {
	file?: Blob | string | null;
	fileURL?: string | null;
}

export interface ImageProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data | null;
	onChange: (data: Data) => void;
}

function Image({ initialData, onChange, ...props }: ImageProps): ReactElement<ImageProps> {
	const { createMessageToast } = useToast();

	const [data, setData] = useState<Data>(initialData ?? {});

	useEffect(() => onChange(data), [data]);

	function handleImageChange(event: ReactChangeEvent<HTMLInputElement>): void {
		if (event.target.files) {
			const file: File = event.target.files[0];

			if (file.size < 3145728) {
				const fileRender = new FileReader();
				fileRender.readAsDataURL(file);
				fileRender.addEventListener('loadend', e => setData({ ...data, file, fileURL: e.target?.result as string | null ?? undefined }));
			} else {
				createMessageToast({ message: gettext('Изображение весит больше 3МБ!'), level: 'danger' });
			}
		}
	}

	return (
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Изображение')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				{data.fileURL && (
					<RBImage thumbnail className='p-0' src={data.fileURL} />
				)}
				<Form.Control
					type='file'
					accept='image/*'
					onChange={handleImageChange}
				/>
			</Card.Body>
		</Card>
	);
}

export default Image;