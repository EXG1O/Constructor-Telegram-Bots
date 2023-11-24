import 'monaco-editor/min/vs/editor/editor.main.css';

import { Toast } from 'global_modules/toast';
import { TelegramBotDatabaseRecordsApi } from 'telegram_bot_api/main';
import { TelegramBotDatabaseRecord } from 'telegram_bot_api/types';
import * as Components from './components';

declare const telegramBotId: number;

const recordsComponent: Components.RecordAsExist.ListGroupItem[] = [];

async function update(): Promise<void> {
	const response = await TelegramBotDatabaseRecordsApi.get(telegramBotId);

	if (response.ok) {
		recordsComponent.forEach(recordComponent => recordComponent.delete());
		response.json.forEach(record => recordsComponent.push(Components.RecordAsExist.create(record)));
	} else {
		new Toast(response.json.message, response.json.level).show();
	}
}

update();

const collapseButton = document.querySelector('#telegramBotDatabaseRecordsСollapseButton') as HTMLButtonElement;
const updateButton = document.querySelector('#telegramBotDatabaseRecordsUpdateButton') as HTMLButtonElement;
const addButton = document.querySelector('#telegramBotDatabaseRecordsAddButton') as HTMLButtonElement;

collapseButton.addEventListener('click', () => {
	updateButton.classList.toggle('disabled');
	addButton.classList.toggle('disabled');
});
updateButton.addEventListener('click', async () => await update());
addButton.addEventListener('click', () => {
	const component = Components.RecordAsNotExist.create();

	component.onDidSaveFunc = (record: TelegramBotDatabaseRecord): void => {
		recordsComponent.push(Components.RecordAsExist.create(record));
	}
});