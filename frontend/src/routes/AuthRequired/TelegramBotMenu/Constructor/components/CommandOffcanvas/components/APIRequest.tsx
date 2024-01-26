import React, { MutableRefObject, ReactElement, memo, useEffect, useRef, useState } from 'react';
import classNames from 'classnames';
import monaco from 'monaco-editor';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';
import ToggleButton, { ToggleButtonProps } from 'react-bootstrap/ToggleButton';
import Button from 'react-bootstrap/Button';
import Collapse from 'react-bootstrap/Collapse';
import InputGroup from 'react-bootstrap/InputGroup';
import MonacoEditor from '@monaco-editor/react';
import Stack from 'react-bootstrap/Stack';

import useToast from 'services/hooks/useToast';

import { updateEditorLayout, defaultEditorOptions } from 'utils/monaco_editor';

interface DataHeaders {
	key: string;
	value: string;
}

export interface Data {
	url: string;
	method: 'get' | 'post' | 'put' | 'patch' | 'delete';
	headers?: DataHeaders[];
	body?: string;
}

export interface APIRequestProps extends Omit<CardProps, 'onChange' | 'children'>  {
	initialData?: Data;
	onChange: (data: Data) => void;
}

interface Addons {
	headers: NonNullable<Data['headers']>;
	body: NonNullable<Data['body']>;
}

interface TestAPIRequestResult {
	status: number;
	json?: Record<string, any>;
}

interface KeyboardToggleButtonProps extends Omit<ToggleButtonProps, 'key' | 'id' | 'value' | 'size' | 'variant' | 'onChange' | 'children'> {
	value: Data['method'];
}

const methodToggleButtons: KeyboardToggleButtonProps[] = [
	{ value: 'get' },
	{ value: 'post' },
	{ value: 'put' },
	{ value: 'patch' },
	{ value: 'delete' },
];

function APIRequest({ initialData, onChange, ...props }: APIRequestProps): ReactElement<APIRequestProps> {
	const { createMessageToast } = useToast();

	const [data, setData] = useState<Data>(initialData ?? { url: '', method: 'get' });
	const [showAddons, setShowAddons] = useState<Record<keyof Addons, boolean>>({
		headers: Boolean(initialData?.headers),
		body: Boolean(initialData?.body),
	});
	const [testAPIRequestResult, setTestAPIRequestResult] = useState<TestAPIRequestResult | undefined>(undefined);

	const bodyMonacoEditor = useRef<monaco.editor.IStandaloneCodeEditor | undefined>(undefined);
	const testAPIRequestResultMonacoEditor = useRef<monaco.editor.IStandaloneCodeEditor | undefined>(undefined);

	useEffect(() => onChange(data), [data]);

	function handleHeaderChange(index: number, name: keyof DataHeaders, value: DataHeaders[keyof DataHeaders]): void {
		if (data.headers) {
			const headers = [...data.headers];

			headers[index][name] = value;

			setData({ ...data, headers });
		}
	}

	function handleDeleteHeaderButtonClick(index: number): void {
		if (data.headers) {
			const headers = [...data.headers];

			headers.splice(index, 1);

			setData({ ...data, headers });
		}
	}

	function handleMonacoEditorMount(
		ref: MutableRefObject<monaco.editor.IStandaloneCodeEditor | undefined>,
		editor: monaco.editor.IStandaloneCodeEditor,
	): void {
		ref.current = editor;

		setTimeout(() => {
			if (ref.current) {
				updateEditorLayout(ref.current);
			}
		}, 250);
	}

	function handleMonacoEditorChange(ref: MutableRefObject<monaco.editor.IStandaloneCodeEditor | undefined>, value?: string): void {
		if (ref.current && value !== undefined) {
			setData({ ...data, body: value });

			updateEditorLayout(ref.current);
		}
	}

	async function handleMakeTestAPIRequestButtonClick(): Promise<void> {
		if (!data.url) {
			createMessageToast({ message: gettext('Введите URL-адрес!'), level: 'error' });
			return;
		}

		try {
			new URL(data.url);
		} catch {
			createMessageToast({ message: gettext('Введите правильный URL-адрес!'), level: 'error' });
			return;
		}

		const headers: HeadersInit = {};

		data.headers?.forEach(header => headers[header.key] = header.value);

		try {
			const response = await fetch(data.url, {
				method: data.method,
				headers,
				body: data.body && JSON.parse(data.body),
			});

			let responseJSON: Record<string, any> | undefined;

			try {
				responseJSON = await response.json();
			} catch {
				responseJSON = undefined;
			}

			setTestAPIRequestResult({
				status: response.status,
				json: responseJSON,
			});
		} catch {
			createMessageToast({ message: gettext('Произошла ошибка во время отпрвки API-запроса!'), level: 'error' });
		}
	}

	return (
		<Card {...props} className={classNames('border', props.className)}>
			<Card.Header as='h6' className='border-bottom text-center'>
				{gettext('API-запрос')}
			</Card.Header>
			<Card.Body className='p-2'>
				<Form.Control
					value={data.url}
					className='mb-2'
					placeholder={gettext('Введите URL-адрес')}
					onChange={e => setData({ ...data, url: e.target.value })}
				/>
				<ToggleButtonGroup
					type='radio'
					name='api-request-methods'
					defaultValue='get'
					className='w-100 mb-2'
				>
					{methodToggleButtons.map((props, index) => (
						<ToggleButton
							{...props}
							key={index}
							id={`api-request-method-${props.value}`}
							size='sm'
							variant='outline-dark'
							onChange={() => setData({ ...data, method: props.value })}
						>
							{props.value.toUpperCase()}
						</ToggleButton>
					))}
				</ToggleButtonGroup>
				<Button
					size='sm'
					{...(
						showAddons.headers ? {
							variant: 'secondary',
							className: 'w-100 border-bottom-0 rounded-bottom-0',
							children: gettext('Убрать заголовки'),
						} : {
							variant: 'dark',
							className: 'w-100',
							children: gettext('Добавить заголовки'),
						}
					)}
					aria-controls='command-offcanvas-api-request-headers-addon'
					aria-expanded={showAddons.headers}
					onClick={() => setShowAddons({ ...showAddons, headers: !showAddons.headers })}
				/>
				<Collapse
					in={showAddons.headers}
					unmountOnExit
					onEnter={() => setData({ ...data, headers: [] })}
					onExited={() => setData({ ...data, headers: undefined })}
				>
					<div id='command-offcanvas-api-request-headers-addon'>
						<div className='vstack border border-top-0 rounded rounded-top-0 gap-1 p-1'>
							{data.headers?.map((header, index) => (
								<InputGroup key={index}>
									<Form.Control
										size='sm'
										value={header.key}
										placeholder={gettext('Ключ')}
										onChange={e => handleHeaderChange(index, 'key', e.target.value)}
									/>
									<Form.Control
										size='sm'
										value={header.value}
										placeholder={gettext('Значение')}
										onChange={e => handleHeaderChange(index, 'value', e.target.value)}
									/>
									<Button
										as='i'
										size='sm'
										variant='danger'
										className='bi bi-trash d-flex justify-content-center align-items-center p-0'
										style={{ width: '31px', height: '31px', fontSize: '18px' }}
										onClick={() => handleDeleteHeaderButtonClick(index)}
									/>
								</InputGroup>
							))}
							<Button
								size='sm'
								variant='dark'
								onClick={() => setData({ ...data, headers: [...data.headers!, { key: '', value: '' }] })}
							>
								{gettext('Добавить заголовок')}
							</Button>
						</div>
					</div>
				</Collapse>
				<Button
					size='sm'
					{...(
						showAddons.body ? {
							variant: 'secondary',
							className: 'w-100 border-bottom-0 rounded-bottom-0 mt-2',
							children: gettext('Убрать данные'),
						} : {
							variant: 'dark',
							className: 'w-100 mt-2',
							children: gettext('Добавить данные'),
						}
					)}
					aria-controls='command-offcanvas-api-request-body-addon'
					aria-expanded={showAddons.body}
					onClick={() => setShowAddons({ ...showAddons, body: !showAddons.body })}
				/>
				<Collapse
					in={showAddons.body}
					unmountOnExit
					onExited={() => setData({ ...data, body: undefined })}
				>
					<div id='command-offcanvas-api-request-body-addon'>
						<MonacoEditor
							defaultLanguage='json'
							defaultValue={data.body ?? JSON.stringify({ key: 'value' }, undefined, 4)}
							options={{
								...defaultEditorOptions,
								glyphMargin: false,
								folding: false,
								lineNumbers: 'off',
								lineDecorationsWidth: 0,
								lineNumbersMinChars: 0,
							}}
							className='overflow-hidden border border-top-0 rounded rounded-top-0 p-2'
							onMount={editor => handleMonacoEditorMount(bodyMonacoEditor, editor)}
							onChange={value => handleMonacoEditorChange(bodyMonacoEditor, value)}
						/>
					</div>
				</Collapse>
				<Button
					size='sm'
					variant='dark'
					className={classNames('w-100 mt-2', testAPIRequestResult ? 'border-bottom-0 rounded-bottom-0' : undefined)}
					onClick={() => handleMakeTestAPIRequestButtonClick()}
				>
					{gettext('Протестировать')}
				</Button>
				<Collapse
					in={testAPIRequestResult !== undefined}
					unmountOnExit
				>
					<div className='command-offcanvas-api-request-test-result'>
						<Stack gap={1} className='border border-top-0 rounded rounded-top-0 p-1'>
							{testAPIRequestResult && (
								<>
									<div className='d-flex gap-1'>
										<div
											className={`align-self-center bg-${testAPIRequestResult.status <= 399 ? 'success' : 'danger'}`}
											style={{
												width: '14px',
												height: '14px',
												borderRadius: '50%',
											}}
										/>
										{testAPIRequestResult.status}
									</div>
									{testAPIRequestResult?.json && (
										<MonacoEditor
											defaultLanguage='json'
											value={JSON.stringify(testAPIRequestResult.json, undefined, 4)}
											options={{
												...defaultEditorOptions,
												readOnly: true,
												domReadOnly: true,
												glyphMargin: false,
												folding: false,
												lineNumbers: 'off',
												lineDecorationsWidth: 0,
												lineNumbersMinChars: 0,
											}}
											onMount={editor => handleMonacoEditorMount(testAPIRequestResultMonacoEditor, editor)}
											onChange={() => updateEditorLayout(testAPIRequestResultMonacoEditor.current!)}
										/>
									)}
								</>
							)}
						</Stack>
					</div>
				</Collapse>
			</Card.Body>
		</Card>
	);
}

export default memo(APIRequest);