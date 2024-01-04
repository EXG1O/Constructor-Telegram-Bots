import React, { ReactElement, ChangeEvent as ReactChangeEvent, memo, useEffect, useState } from 'react';
import classNames from 'classnames';

import Card, { CardProps } from 'react-bootstrap/Card';
import Carousel from 'react-bootstrap/Carousel';
import Image from 'react-bootstrap/Image';
import Spinner from 'react-bootstrap/Spinner';
import Form from 'react-bootstrap/Form';

import useToast from 'services/hooks/useToast';

export interface Data {
	files?: File[] | null;
	filesURL?: string[] | null;
}

export interface ImagesProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data | null;
	onChange: (data: Data) => void;
}

interface FilesResult {
	file: File,
	url?: string,
}

function Images({ initialData, onChange, ...props }: ImagesProps): ReactElement<ImagesProps> {
	const { createMessageToast } = useToast();

	const [data, setData] = useState<Data>(initialData ?? {});
	const [loadingImages, setLoadingImages] = useState<boolean>(false);

	useEffect(() => onChange(data), [data]);

	function handleImagesChange(event: ReactChangeEvent<HTMLInputElement>): void {
		if (event.target.files) {
			setLoadingImages(true);

			const files: FileList = event.target.files;
			const filesResult: Record<number, FilesResult> = {}
			let index = 0;

			for (const file of files) {
				if (file.size < 3145728) {
					const index_ = index;

					filesResult[index_] = { file, url: undefined };

					const fileRender = new FileReader();
					fileRender.readAsDataURL(file);
					fileRender.addEventListener('loadend', e => {
						if (e.target?.result) {
							filesResult[index_].url = e.target.result as string;
						} else {
							delete filesResult[index_];
						}
					});

					index += 1;
				} else {
					createMessageToast({ message: interpolate(
						gettext('Изображение %(name)s весит больше 3МБ!'),
						{ name: file.name },
						true,
					), level: 'danger' });
				}
			}

			const checkFilesResult = () => {
				for (const key of Object.keys(filesResult)) {
					if (!filesResult[parseInt(key)].url) {
						setTimeout(checkFilesResult, 500);
						return;
					}
				}

				setData({
					files: Object.keys(filesResult).map(key => filesResult[parseInt(key)].file),
					filesURL: Object.keys(filesResult).map(key => filesResult[parseInt(key)].url!),
				});
				setLoadingImages(false);
			}

			checkFilesResult();
		}
	}

	return (
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Изображение')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				{loadingImages ? (
					<div className='d-flex border rounded' style={{ height: '200px' }}>
						<Spinner
							animation='border'
							className='m-auto'
							style={{
								width: '2.25rem',
								height: '2.25rem',
								borderWidth: '0.225rem',
							}}
						/>
					</div>
				) : (
					data.filesURL && (
						<Carousel interval={null} variant='dark'>
							{data.filesURL.map((fileURL, index) => (
								<Carousel.Item key={index} className='overflow-hidden border rounded'>
									<Image
										className='w-100 p-0'
										src={fileURL}
										style={{ objectFit: 'contain', height: '200px' }}
									/>
								</Carousel.Item>
							))}
						</Carousel>
					)
				)}
				<Form.Control
					type='file'
					accept='image/*'
					multiple
					onChange={handleImagesChange}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(Images);