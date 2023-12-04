import Toast from 'global_modules/toast';
import { updateEditorLayout, defaultEditorOptions } from 'global_modules/monaco_editor';
import { TelegramBotDatabaseRecordApi } from 'telegram_bot_api/main';
import monaco from 'monaco-editor';
import Editor from '@monaco-editor/react';
import React from 'react';

declare const telegramBotId: number;

const buttonWithOnlyIconStyle: React.CSSProperties = {
	fontSize: '20px',
}

interface AddRecordModalBodyProps {
	onAdd: () => void;
	onCancel: () => void;
}

export default function AddRecordModalBody({onAdd, onCancel}: AddRecordModalBodyProps): React.JSX.Element {
	const editorRef = React.useRef<monaco.editor.IStandaloneCodeEditor>();

	function resetEditorValue(): void {
		editorRef.current!.setValue(JSON.stringify({key: 'value'}, null, 4));

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
		const response = await TelegramBotDatabaseRecordApi.create(telegramBotId, {record: JSON.parse(editorRef.current!.getValue())})

		if (response.ok) {
			resetEditorValue();

			onAdd();
		}

		new Toast(response.json.message, response.json.level).show();
	}

	function handleCancelButtonClick(): void {
		resetEditorValue();

		onCancel();
	}

	return (
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
	);
}