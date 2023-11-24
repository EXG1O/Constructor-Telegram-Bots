import { Toast } from 'global_modules/toast';
import { askConfirmModal } from 'global_modules/modals/ask_confirm_modal';
import { TelegramBotDatabaseRecordApi } from 'telegram_bot_api/main';
import { TelegramBotDatabaseRecord } from 'telegram_bot_api/types';
import * as monacoEditor from 'global_modules/monaco_editor';

declare const telegramBotId: number;
declare const telegramBotDatabaseRecordIsNotJson: string;
declare const askConfirmModalDeleteTelegramBotDatabaseRecordTitle: string;
declare const askConfirmModalDeleteTelegramBotDatabaseRecordText: string;

const recordsParentElement = document.querySelector('#telegramBotDatabaseRecords') as HTMLDivElement;

export namespace RecordAsExist {
	export class ListGroupItem extends monacoEditor.Components.ListGroupItem {
		public record: TelegramBotDatabaseRecord;
		public editorContentChangeActionButtonsDiv!: HTMLDivElement;

		public constructor(record: TelegramBotDatabaseRecord) {
			super(recordsParentElement, 'dark-subtle', 'json', JSON.stringify(record, null, 4));

			this.record = record;
		}

		protected onDidChangeEditorContent(): void {
			const isFindedClass = this.editorContentChangeActionButtonsDiv.classList.contains('d-none');

			if (isFindedClass) {
				this.editorContentChangeActionButtonsDiv.classList.remove('d-none');
			}

			this.updateEditorLayout(isFindedClass);
		}

		protected hideEditorContentChangeActionButtons(): void {
			this.monacoEditor.setValue(JSON.stringify(this.record, null, 4));

			this.editorContentChangeActionButtonsDiv.classList.add('d-none');

			this.updateEditorLayout(true);
		}

		protected createEditorContentChangeActionButtons(): void {
			const confirmButton = this.createActionButton('success', 'check-lg');
			const cancelButton = this.createActionButton('danger', 'x-lg');

			this.editorContentChangeActionButtonsDiv.append(confirmButton, cancelButton);

			confirmButton.addEventListener('click', async () => {
				try {
					const response = await TelegramBotDatabaseRecordApi.update(
						telegramBotId,
						this.record._id,
						{record: JSON.parse(this.monacoEditor.getValue())},
					);

					if (response.ok) {
						this.record = response.json.record;

						this.hideEditorContentChangeActionButtons();
					}

					new Toast(response.json.message, response.json.level).show();
				} catch {
					new Toast(telegramBotDatabaseRecordIsNotJson, 'danger').show();
				}
			});
			cancelButton.addEventListener('click', () => this.hideEditorContentChangeActionButtons());
		}

		protected createActionButtons(): void {
			this.editorContentChangeActionButtonsDiv = document.createElement('div');
			this.editorContentChangeActionButtonsDiv.className = 'btn-group btn-editor-content-change-group d-none';
			this.editorContentChangeActionButtonsDiv.role = 'group';
			this.actionButtonsDiv.appendChild(this.editorContentChangeActionButtonsDiv);

			this.createEditorContentChangeActionButtons();

			const deleteButton = this.createActionButton('danger', 'trash');
			this.actionButtonsDiv.appendChild(deleteButton);

			deleteButton.addEventListener('click', () => {
				askConfirmModal(
					askConfirmModalDeleteTelegramBotDatabaseRecordTitle,
					askConfirmModalDeleteTelegramBotDatabaseRecordText,
					async () => {
						const response = await TelegramBotDatabaseRecordApi.delete_(telegramBotId, this.record._id);

						if (response.ok) {
							this.delete();
						}

						new Toast(response.json.message, response.json.level).show();
					}
				);
			});
		}
	}

	export const create = (record: TelegramBotDatabaseRecord): ListGroupItem => new ListGroupItem(record);
}

export namespace RecordAsNotExist {
	export class ListGroupItem extends monacoEditor.Components.ListGroupItem {
		public onDidSaveFunc?: (record: TelegramBotDatabaseRecord) => void;

		public constructor() {
			super(recordsParentElement, 'success-subtle', 'json', JSON.stringify({key: 'value'}, null, 4));

			this.actionButtonsDiv.className = 'btn-group btn-action-group';
			this.actionButtonsDiv.role = 'group';
		}

		protected createActionButtons(): void {
			const confirmButton = this.createActionButton('success', 'check-lg');
			const cancelButton = this.createActionButton('danger', 'x-lg');

			this.actionButtonsDiv.append(confirmButton, cancelButton);

			confirmButton.addEventListener('click', async () => {
				try {
					const response = await TelegramBotDatabaseRecordApi.create(telegramBotId, {record: JSON.parse(this.monacoEditor.getValue())});

					if (response.ok) {
						if (this.onDidSaveFunc) {
							this.onDidSaveFunc(response.json.record);
						}

						this.delete();
					}

					new Toast(response.json.message, response.json.level).show();
				} catch {
					new Toast(telegramBotDatabaseRecordIsNotJson, 'danger').show();
				}
			});
			cancelButton.addEventListener('click', () => this.delete());
		}
	}

	export const create = (): ListGroupItem => new ListGroupItem();
}