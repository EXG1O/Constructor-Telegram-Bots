import React, { ReactNode } from 'react';

import monaco from 'monaco-editor';

import Modal, { ModalProps } from 'react-bootstrap/Modal';
import Editor from '@monaco-editor/react';

import { TelegramBotDatabaseRecordAPI } from 'services/api/telegram_bots/main';

import useTelegramBot from 'services/hooks/useTelegramBot';
import useToast from 'services/hooks/useToast';

import { updateEditorLayout, defaultEditorOptions } from 'utils/monaco_editor';

const buttonWithOnlyIconStyle: React.CSSProperties = {
	fontSize: '20px',
}

export interface CreateRecordModalProps extends Omit<ModalProps, 'onHide'> {
	onCreate: () => void;
	onHide: NonNullable<ModalProps['onHide']>;
}

function CreateRecordModal({ onCreate, ...modalProps }: CreateRecordModalProps): ReactNode {
	const { telegramBot } = useTelegramBot();
	const { createMessageToast } = useToast();

	const editorRef = React.useRef<monaco.editor.IStandaloneCodeEditor | undefined>(undefined);

	function resetEditorValue(): void {
		editorRef.current!.setValue(JSON.stringify({ key: 'value' }, null, 4));

		updateEditorLayout(editorRef.current!);
	}

	function handleEditorDidMount(editor: monaco.editor.IStandaloneCodeEditor): void {
		editorRef.current = editor;

		resetEditorValue();
		updateEditorLayout(editorRef.current);
	}

	function handleEditorChange(): void {
		updateEditorLayout(editorRef.current!);
	}

	async function handleAddButtonClick(): Promise<void> {
		const response = await TelegramBotDatabaseRecordAPI.create(telegramBot.id, { record: JSON.parse(editorRef.current!.getValue()) })

		if (response.ok) {
			resetEditorValue();

			onCreate();
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	function handleCancelButtonClick(): void {
		resetEditorValue();

		modalProps.onHide();
	}

	return (
		<Modal {...modalProps}>
			<Modal.Header closeButton>
				<Modal.Title as='h5'>{gettext('Добавление записи')}</Modal.Title>
			</Modal.Header>
			<Modal.Body>
				<div className='d-flex justify-content-between align-items-center gap-3'>
					<div className='flex-fill border border-2 border-dark-subtle rounded p-2'>
						<Editor
							defaultLanguage='json'
							options={defaultEditorOptions}
							onMount={handleEditorDidMount}
							onChange={handleEditorChange}
						/>
					</div>
					<div className='btn-group'>
						<button
							className='btn btn-success bi bi-check-lg px-2 py-0'
							onClick={handleAddButtonClick}
							style={buttonWithOnlyIconStyle}
						></button>
						<button
							className='btn btn-danger bi bi-x-lg px-2 py-0'
							onClick={handleCancelButtonClick}
							style={buttonWithOnlyIconStyle}
						></button>
					</div>
				</div>
			</Modal.Body>
		</Modal>
	);
}

export default CreateRecordModal;