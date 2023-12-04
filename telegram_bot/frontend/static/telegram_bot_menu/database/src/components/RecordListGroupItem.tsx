import Toast from 'global_modules/toast';
import { askConfirmModal } from 'global_modules/modals/ask_confirm_modal';
import { updateEditorLayout, defaultEditorOptions } from 'global_modules/monaco_editor';
import { TelegramBotDatabaseRecordApi } from 'telegram_bot_api/main';
import { TelegramBotDatabaseRecord } from 'telegram_bot_api/types';
import { RecordListGroup } from '../main';
import monaco from 'monaco-editor';
import Editor from '@monaco-editor/react';
import React from 'react';

declare const telegramBotId: number;
declare const telegramBotDatabaseRecordIsNotJson: string;
declare const askConfirmModalDeleteTelegramBotDatabaseRecordTitle: string;
declare const askConfirmModalDeleteTelegramBotDatabaseRecordText: string;

const buttonWithOnlyIconStyle: React.CSSProperties = {
	fontSize: '20px',
}

interface RecordListGroupItemProps {
	recordInitial: TelegramBotDatabaseRecord;
}

export default function RecordListGroupItem({recordInitial}: RecordListGroupItemProps): React.JSX.Element {
	const [record, setRecord] = React.useState<TelegramBotDatabaseRecord>(recordInitial);
	const [recordIsEditing, setRecordIsEditing] = React.useState<boolean>(false);

	const editorRef = React.useRef<monaco.editor.IStandaloneCodeEditor>();

	function handleEditorDidMount(editor: monaco.editor.IStandaloneCodeEditor): void {
		editorRef.current = editor;

		updateEditorLayout(editorRef.current);
	}

	function handleEditorChange(): void {
		if (!recordIsEditing) {
			setRecordIsEditing(true);
		}

		updateEditorLayout(editorRef.current!, !recordIsEditing);
	}

	async function handleSaveEditedRecordButtonClick(): Promise<void> {
		try {
			const response = await TelegramBotDatabaseRecordApi.update(telegramBotId, record._id, {record: JSON.parse(editorRef.current!.getValue())});

			if (response.ok) {
				setRecordIsEditing(false);
				setRecord(response.json.record);

				updateEditorLayout(editorRef.current!, true);
			}

			new Toast(response.json.message, response.json.level).show();
		} catch {
			new Toast(telegramBotDatabaseRecordIsNotJson, 'danger').show();
		}
	}

	function handleCancelEditRecordButtonClick(): void {
		setRecordIsEditing(false);

		editorRef.current!.setValue(JSON.stringify(record, null, 4));

		updateEditorLayout(editorRef.current!, true);
	}

	function handleDeleteRecordButtonClick(): void {
		askConfirmModal(
			askConfirmModalDeleteTelegramBotDatabaseRecordTitle,
			askConfirmModalDeleteTelegramBotDatabaseRecordText,
			async (): Promise<void> => {
				const response = await TelegramBotDatabaseRecordApi.delete_(telegramBotId, record._id);

				if (response.ok) {
					RecordListGroup.update();
				}

				new Toast(response.json.message, response.json.level).show();
			}
		);
	}

	return (
		<div className='list-group-item p-3'>
			<div className='d-flex justify-content-between align-items-center gap-3'>
				<div className='flex-fill border border-2 border-dark-subtle rounded p-2'>
					<Editor
						defaultValue={JSON.stringify(record, null, 4)}
						defaultLanguage='json'
						options={defaultEditorOptions}
						onMount={handleEditorDidMount}
						onChange={handleEditorChange}
					/>
				</div>
				<div className='d-flex gap-2'>
					{recordIsEditing && (
						<div className='btn-group'>
							<button
								className='btn btn-success bi bi-check-lg px-2 py-0'
								onClick={handleSaveEditedRecordButtonClick}
								style={buttonWithOnlyIconStyle}
							></button>
							<button
								className='btn btn-danger bi bi-x-lg px-2 py-0'
								onClick={handleCancelEditRecordButtonClick}
								style={buttonWithOnlyIconStyle}
							></button>
						</div>
					)}
					<button
						className='btn btn-danger bi bi-trash px-2 py-0'
						onClick={handleDeleteRecordButtonClick}
						style={buttonWithOnlyIconStyle}
					></button>
				</div>
			</div>
		</div>
	);
}