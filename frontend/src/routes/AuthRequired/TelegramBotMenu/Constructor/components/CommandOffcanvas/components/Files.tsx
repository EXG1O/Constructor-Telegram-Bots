import React, { ReactElement, ChangeEvent as ReactChangeEvent, memo, useEffect, useState } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Button from 'react-bootstrap/Button';

import useToast from 'services/hooks/useToast';

interface FileData {
	id?: number;
	file?: File;
	name: File['name'];
	size: File['size'];
}

export type Data = FileData[];

export interface FilesProps extends Omit<CardProps, 'onChange' | 'children'> {
	initialData?: Data;
	onChange: (data: Data) => void;
}

function Files({ initialData, onChange, ...props }: FilesProps): ReactElement<FilesProps> {
	const { createMessageToast } = useToast();

	const [data, setData] = useState<Data>(initialData ?? []);

	useEffect(() => onChange(data), [data]);

	function handleFilesChange(event: ReactChangeEvent<HTMLInputElement>): void {
		if (event.target.files) {
			const files: File[] = [...event.target.files];
			const filesResult: File[] = []

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
						filesResult.push(file);
					} else {
						createMessageToast({
							message: interpolate(
								gettext('Файл %(name)s уже добавлен!'),
								{ name: file.name },
								true,
							),
							level: 'error',
						});
					}
				} else {
					createMessageToast({
						message: interpolate(
							gettext('Файл %(name)s весит больше 3МБ!'),
							{ name: file.name },
							true,
						),
						level: 'error',
					});
				}
			}

			setData([
				...data,
				...Object.keys(filesResult).map(key => {
					const file: File = filesResult[parseInt(key)];

					return { file, name: file.name, size: file.size };
				}),
			]);
		}
	}

	function handleDeleteFileButtonClick(index: number): void {
		const files = [...data];
		files.splice(index, 1);
		setData(files);
	}

	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Файлы')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				{data.length ? (
					<div className='d-flex flex-wrap border rounded gap-1 p-1'>
						{data.map((file, index) => (
							<ButtonGroup key={index}>
								<small className='text-bg-dark rounded-1 rounded-end-0 px-2 py-1'>
									{file.name}
								</small>
								<Button
									as='i'
									size='sm'
									variant='danger'
									className='bi bi-trash d-flex justify-content-center align-items-center p-0'
									style={{ width: '31px', fontSize: '16px' }}
									onClick={() => handleDeleteFileButtonClick(index)}
								/>
							</ButtonGroup>
						))}
					</div>
				) : undefined}
				<input
					id='command-offcanvas-files-input-file'
					type='file'
					multiple
					hidden
					onChange={handleFilesChange}
				/>
				<Button
					as='label'
					htmlFor='command-offcanvas-files-input-file'
					size='sm'
					variant='dark'
				>
					{gettext('Добавить файл')}
				</Button>
			</Card.Body>
		</Card>
	);
}

export default memo(Files);