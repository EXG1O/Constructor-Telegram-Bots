import React, { ReactNode } from 'react';

import monaco from 'monaco-editor';

import Editor from '@monaco-editor/react';

import useTelegramBot from 'services/hooks/useTelegramBot';
import useToast from 'services/hooks/useToast';

import { TelegramBotDatabaseRecordAPI } from 'services/api/telegram_bots/main';
import { TelegramBotDatabaseRecord } from 'services/api/telegram_bots/types';

import { updateEditorLayout, defaultEditorOptions } from 'utils/monaco_editor';

const buttonWithOnlyIconStyle: React.CSSProperties = {
	fontSize: '20px',
}

export interface DatabaseRecordProps {
	databaseRecord: TelegramBotDatabaseRecord;
}

function DatabaseRecord({ databaseRecord: databaseRecordInitial }: DatabaseRecordProps): ReactNode {
	const { telegramBot } = useTelegramBot();
	const { createMessageToast } = useToast();

	const [databaseRecord, setDatabaseRecord] = React.useState<TelegramBotDatabaseRecord>(databaseRecordInitial);
	const [databaseRecordIsEditing, setDatabaseRecordIsEditing] = React.useState<boolean>(false);

	const editorRef = React.useRef<monaco.editor.IStandaloneCodeEditor>();

	function handleEditorDidMount(editor: monaco.editor.IStandaloneCodeEditor): void {
		editorRef.current = editor;

		updateEditorLayout(editorRef.current);
	}

	function handleEditorChange(): void {
		if (!databaseRecordIsEditing) {
			setDatabaseRecordIsEditing(true);
		}

		updateEditorLayout(editorRef.current!, !databaseRecordIsEditing);
	}

	async function handleSaveEditedRecordButtonClick(): Promise<void> {
		try {
			const response = await TelegramBotDatabaseRecordAPI.update(
				telegramBot.id,
				databaseRecord._id,
				{ record: JSON.parse(editorRef.current!.getValue()) },
			);

			if (response.ok) {
				setDatabaseRecordIsEditing(false);
				setDatabaseRecord(response.json.record);

				updateEditorLayout(editorRef.current!, true);
			}

			createMessageToast({ message: response.json.message, level: response.json.level });
		} catch {
			createMessageToast({ message: gettext('Запись базы данных должна быть в формате JSON!'), level: 'danger' });
		}
	}

	function handleCancelEditRecordButtonClick(): void {
		setDatabaseRecordIsEditing(false);

		editorRef.current!.setValue(JSON.stringify(databaseRecord, null, 4));

		updateEditorLayout(editorRef.current!, true);
	}

	// function handleDeleteRecordButtonClick(): void {
	// 	askConfirmModal(
	// 		askConfirmModalDeleteTelegramBotDatabaseRecordTitle,
	// 		askConfirmModalDeleteTelegramBotDatabaseRecordText,
	// 		async (): Promise<void> => {
	// 			const response = await TelegramBotDatabaseRecordApi.delete_(telegramBotId, databaseRecord._id);

	// 			if (response.ok) {
	// 				RecordListGroup.update();
	// 			}

	// 			new Toast(response.json.message, response.json.level).show();
	// 		}
	// 	);
	// }

	return (
		<div className='d-flex justify-content-between align-items-center gap-3'>
			<div className='flex-fill border border-2 border-dark-subtle rounded p-2'>
				<Editor
					defaultValue={JSON.stringify(databaseRecord, null, 4)}
					defaultLanguage='json'
					options={defaultEditorOptions}
					onMount={handleEditorDidMount}
					onChange={handleEditorChange}
				/>
			</div>
			<div className='d-flex gap-2'>
				{databaseRecordIsEditing && (
					<div className='btn-group'>
						<button
							className='btn btn-success bi bi-check-lg px-2 py-0'
							onClick={handleSaveEditedRecordButtonClick}
							style={buttonWithOnlyIconStyle}
						/>
						<button
							className='btn btn-danger bi bi-x-lg px-2 py-0'
							onClick={handleCancelEditRecordButtonClick}
							style={buttonWithOnlyIconStyle}
						/>
					</div>
				)}
				<button
					className='btn btn-danger bi bi-trash px-2 py-0'
					// onClick={handleDeleteRecordButtonClick}
					style={buttonWithOnlyIconStyle}
				/>
			</div>
		</div>
	);
}

export default DatabaseRecord;