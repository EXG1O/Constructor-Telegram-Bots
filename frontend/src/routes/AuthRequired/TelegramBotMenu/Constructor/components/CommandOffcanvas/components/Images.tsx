import React, { ReactElement, ChangeEvent as ReactChangeEvent, memo, useEffect, useState } from 'react';
import classNames from 'classnames';

import Card, { CardProps } from 'react-bootstrap/Card';
import Carousel from 'react-bootstrap/Carousel';
import Image from 'react-bootstrap/Image';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Button from 'react-bootstrap/Button';

import Loading from 'components/Loading';

import useToast from 'services/hooks/useToast';

interface ImageData {
	id?: number;
	file?: File;
	name: File['name'];
	size: File['size'];
	url: string;
}

export type Data = ImageData[];

export interface ImagesProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data;
	onChange: (data: Data) => void;
}

interface FileResult {
	file: File;
	url?: string;
}

function Images({ initialData, onChange, ...props }: ImagesProps): ReactElement<ImagesProps> {
	const { createMessageToast } = useToast();

	const [data, setData] = useState<Data>(initialData ?? []);
	const [loadingImages, setLoadingImages] = useState<boolean>(false);

	useEffect(() => onChange(data), [data]);

	function handleImagesChange(event: ReactChangeEvent<HTMLInputElement>): void {
		if (event.target.files) {
			setLoadingImages(true);

			const files: File[] = [...event.target.files];
			const filesResult: Record<number, FileResult> = {};
			let index = 0;

			event.target.value = '';

			for (const file of files) {
				if (file.size < 3145728) {
					let isFinded = false;

					for (const file_ of data) {
						if (
							file_.name === file.name &&
							file_.size === file.size
						) {
							isFinded = true;
							break;
						}
					}

					if (!isFinded) {
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
						createMessageToast({
							message: interpolate(
								gettext('Изображение %(name)s уже добавлено!'),
								{ name: file.name },
								true,
							),
							level: 'error',
						});
					}
				} else {
					createMessageToast({
						message: interpolate(
							gettext('Изображение %(name)s весит больше 3МБ!'),
							{ name: file.name },
							true,
						),
						level: 'error',
					});
				}
			}

			const checkFilesResult = () => {
				for (const key of Object.keys(filesResult)) {
					if (!filesResult[parseInt(key)].url) {
						setTimeout(checkFilesResult, 500);
						return;
					}
				}

				setData([
					...data,
					...Object.keys(filesResult).map(key => {
						const file: FileResult = filesResult[parseInt(key)];

						return {
							file: file.file,
							name: file.file.name,
							size: file.file.size,
							url: file.url!,
						}
					}),
				]);
				setLoadingImages(false);
			}

			checkFilesResult();
		}
	}

	function handleDeleteImageButtonClick(index: number): void {
		const images = [...data];
		images.splice(index, 1);
		setData(images);
	}

	return (
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('Изображение')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				{loadingImages ? (
					<div className='d-flex border rounded' style={{ height: '200px' }}>
						<Loading size='md' className='m-auto' />
					</div>
				) : (
					data.length ? (
						<>
							<Carousel interval={null} variant='dark'>
								{data.map((image, index) => (
									<Carousel.Item
										key={index}
										className='overflow-hidden border rounded'
									>
										<Image
											className='w-100 p-0'
											src={image.url}
											style={{ objectFit: 'contain', height: '200px' }}
										/>
									</Carousel.Item>
								))}
							</Carousel>
							<div className='d-flex flex-wrap border rounded gap-1 p-1'>
								{data.map((image, index) => (
									<ButtonGroup key={index}>
										<small className='text-bg-dark rounded-1 rounded-end-0 px-2 py-1'>
											{image.name}
										</small>
										<Button
											as='i'
											size='sm'
											variant='danger'
											className='bi bi-trash d-flex justify-content-center align-items-center p-0'
											style={{ width: '31px', fontSize: '16px' }}
											onClick={() => handleDeleteImageButtonClick(index)}
										/>
									</ButtonGroup>
								))}
							</div>
						</>
					) : undefined
				)}
				<input
					id='command-offcanvas-images-input-file'
					type='file'
					accept='image/*'
					multiple
					hidden
					onChange={handleImagesChange}
				/>
				<Button
					as='label'
					htmlFor='command-offcanvas-images-input-file'
					size='sm'
					variant='dark'
				>
					{gettext('Добавить изображение')}
				</Button>
			</Card.Body>
		</Card>
	);
}

export default memo(Images);