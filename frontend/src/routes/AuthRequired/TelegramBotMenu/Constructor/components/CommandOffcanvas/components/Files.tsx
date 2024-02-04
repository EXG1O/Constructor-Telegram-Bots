import React, { ReactElement, ChangeEvent as ReactChangeEvent, memo } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';
import ButtonGroup from 'react-bootstrap/ButtonGroup';
import Button from 'react-bootstrap/Button';

import useToast from 'services/hooks/useToast';

interface FileData extends Pick<File, 'name' | 'size'> {
	id?: number;
	key: string;
	file?: File;
}

export type Data = FileData[];

export interface FilesProps extends Omit<CardProps, 'onChange' | 'children'> {
	data?: Data;
	onChange: (data: Data) => void;
}

export const defaultData: Data = [];

function Files({ data = defaultData, onChange, ...props }: FilesProps): ReactElement<FilesProps> {
	const { createMessageToast } = useToast();

	function handleFilesChange(event: ReactChangeEvent<HTMLInputElement>): void {
		if (event.target.files) {
			const files: File[] = Object.values(event.target.files);

			event.target.value = '';

			onChange([
				...data,
				...files.filter(file => {
					if (file.size < 3145728) {
						for (const _file of data) {
							if (
								_file.name === file.name &&
								_file.size === file.size
							) {
								createMessageToast({
									message: interpolate(
										gettext('Файл %(name)s уже добавлен!'),
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
								gettext('Файл %(name)s весит больше 3МБ!'),
								{ name: file.name },
								true,
							),
							level: 'error',
						});
					}
				}).map(file => ({
					key: crypto.randomUUID(),
					file,
					name: file.name,
					size: file.size,
				})),
			]);
		}
	}

	function handleDeleteFileButtonClick(index: number): void {
		const files = [...data];

		files.splice(index, 1);

		onChange(files);
	}

	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('Файлы')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				{Boolean(data.length) && (
					<div className='d-flex flex-wrap border rounded-1 gap-1 p-1'>
						{data.map((file, index) => (
							<ButtonGroup key={file.key}>
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
				)}
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