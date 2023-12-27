import React, { ChangeEvent, ReactNode, useEffect, useState } from 'react';

import Card from 'react-bootstrap/Card';
import Stack from 'react-bootstrap/Stack'
import RBImage from 'react-bootstrap/Image';
import Form from 'react-bootstrap/Form';

import useToast from 'services/hooks/useToast';

export interface Data {
	file?: Blob;
	fileURL?: string;
}

export interface ImageProps {
	initialData?: Data;
	onChange: (data: Data) => void;
}

function Image({ initialData, onChange }: ImageProps): ReactNode {
	const { createMessageToast } = useToast();

	const [data, setData] = useState<Data>(initialData ?? {});

	useEffect(() => onChange(data), [data]);

	function handleImageChange(event: ChangeEvent<HTMLInputElement>): void {
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
		<Card className='border'>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Изображение')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Stack gap={2}>
					{data.fileURL && (
						<RBImage thumbnail className='p-0' src={data.fileURL} />
					)}
					<Form.Control
						type='file'
						accept='image/*'
						onChange={handleImageChange}
					/>
				</Stack>
			</Card.Body>
		</Card>
	);
}

export default Image;