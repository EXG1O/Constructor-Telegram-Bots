import React, { ChangeEvent, ReactNode, useEffect, useState } from 'react';

import Card from 'react-bootstrap/Card';
import Stack from 'react-bootstrap/Stack'
import RBImage from 'react-bootstrap/Image';
import Form from 'react-bootstrap/Form';

import useToast from 'services/hooks/useToast';

export interface Data {
	image?: Blob;
	imageURL?: string;
}

export interface ImageProps {
	onChange: (data: Data) => void;
}

function Image({ onChange }: ImageProps): ReactNode {
	const { createMessageToast } = useToast();

	const [data, setData] = useState<Data>({});

	useEffect(() => onChange(data));

	function handleImageChange(event: ChangeEvent<HTMLInputElement>): void {
		if (event.target.files) {
			const file: File = event.target.files[0];

			if (file.size < 3145728) {
				const fileRender = new FileReader();
				fileRender.readAsDataURL(file);
				fileRender.addEventListener('loadend', e => setData({ ...data, imageURL: e.target?.result as string | null ?? undefined }));

				setData({ ...data, image: file });
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
					{data.imageURL && (
						<RBImage thumbnail src={data.imageURL} />
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