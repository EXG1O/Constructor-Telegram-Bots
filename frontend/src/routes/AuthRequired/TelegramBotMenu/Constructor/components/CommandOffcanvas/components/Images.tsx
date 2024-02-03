import React, { ReactElement, ChangeEvent as ReactChangeEvent, memo, useEffect, useState } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';
import Carousel from 'react-bootstrap/Carousel';
import Image from 'react-bootstrap/Image';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Button from 'react-bootstrap/Button';

import Loading from 'components/Loading';

import useToast from 'services/hooks/useToast';

interface ImageData extends Pick<File, 'name' | 'size'> {
	id?: number;
	key: string;
	file?: File;
	url: string;
}

export type Data = ImageData[];

export interface ImagesProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data;
	onChange: (data: Data) => void;
}

interface ProcessedFile extends File {
	url?: string;
}

function Images({ initialData, onChange, ...props }: ImagesProps): ReactElement<ImagesProps> {
	const { createMessageToast } = useToast();

	const [data, setData] = useState<Data>(initialData ?? []);
	const [loading, setLoading] = useState<boolean>(false);

	useEffect(() => onChange(data), [data]);

	function handleImagesChange(event: ReactChangeEvent<HTMLInputElement>): void {
		if (event.target.files) {
			setLoading(true);

			const files: File[] = Object.values(event.target.files);

			event.target.value = '';

			const processedFiles: ProcessedFile[] = files.filter(file => {
				if (file.size < 3145728) {
					for (const _file of data) {
						if (
							_file.name === file.name &&
							_file.size === file.size
						) {
							createMessageToast({
								message: interpolate(
									gettext('Изображение %(name)s уже добавлено!'),
									{ name: file.name },
									true,
								),
								level: 'error',
							});
							return false;
						}
					}

					return true;
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
			}).map((file, index) => {
				const fileRender = new FileReader();
				fileRender.readAsDataURL(file);
				fileRender.addEventListener('loadend', e => {
					if (e.target?.result) {
						processedFiles[index].url = e.target.result as string;
					} else {
						delete processedFiles[index];
					}
				});

				return file;
			});

			const checkFilesResult = (): void => {
				for (const file of processedFiles) {
					if (!file.url) {
						setTimeout(checkFilesResult, 500);
						return;
					}
				}

				setData([
					...data,
					...processedFiles.map(file => ({
						key: crypto.randomUUID(),
						file: file,
						name: file.name,
						size: file.size,
						url: file.url!,
					})),
				]);
				setLoading(false);
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
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Изображение')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				{!loading ? (
					Boolean(data.length) && (
						<>
							<Carousel
								interval={null}
								controls={data.length > 1}
								indicators={data.length > 1}
								variant='dark'
							>
								{data.map(image => (
									<Carousel.Item
										key={image.key}
										className='overflow-hidden border rounded'
									>
										<Image
											src={image.url}
											className='w-100 p-0'
											style={{ objectFit: 'contain', height: '200px' }}
										/>
									</Carousel.Item>
								))}
							</Carousel>
							<div className='d-flex flex-wrap border rounded-1 gap-1 p-1'>
								{data.map((image, index) => (
									<ButtonGroup key={image.key}>
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
					)
				) : (
					<div className='d-flex justify-content-center border rounded' style={{ height: '200px' }}>
						<Loading size='md' className='align-self-center' />
					</div>
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