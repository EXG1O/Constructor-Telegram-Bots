import Toast from 'global_modules/toast';
import { TelegramBotDatabaseRecordsApi } from 'telegram_bot_api/main';
import { TelegramBotDatabaseRecord } from 'telegram_bot_api/types';
import RecordListGroupItem from './components/RecordListGroupItem';
import AddRecordModalBody from './components/AddRecordModalBody';
import { Collapse, Modal } from 'bootstrap';
import { createRoot } from 'react-dom/client';
import React from 'react';

declare const telegramBotId: number;

const collapseButtonElement = document.querySelector<HTMLButtonElement>('#telegramBotDatabaseRecordsСollapseButton')!;
const updateButtonElement = document.querySelector<HTMLButtonElement>('#telegramBotDatabaseRecordsUpdateButton')!;
const addButtonElement = document.querySelector<HTMLButtonElement>('#telegramBotDatabaseRecordsAddButton')!;

export namespace RecordListGroup {
	const element = document.querySelector<HTMLDivElement>('#telegramBotDatabaseRecords')!;
	const collapse = Collapse.getOrCreateInstance(element, {toggle: true});

	const root = createRoot(element);

	interface AppProps {
		records: TelegramBotDatabaseRecord[];
	}

	function App({records}: AppProps): React.JSX.Element {
		const [isVisible, setIsVisible] = React.useState<boolean>(true);

		React.useEffect(() => {
			element.addEventListener('shown.bs.collapse', () => setIsVisible(true));
			element.addEventListener('hidden.bs.collapse', () => setIsVisible(false));
		}, []);

		return <>{isVisible && records.map(record => <RecordListGroupItem key={record._id} recordInitial={record} />)}</>;
	}

	export async function update(): Promise<void> {
		const response = await TelegramBotDatabaseRecordsApi.get(telegramBotId);

		if (response.ok) {
			root.render(<App records={response.json} />);
		} else {
			new Toast(response.json.message, response.json.level).show();
		}
	}

	update();

	collapseButtonElement.addEventListener('click', (): void => {
		collapse.toggle();

		updateButtonElement.classList.toggle('disabled');
		addButtonElement.classList.toggle('disabled');
	});
}

export namespace AddRecordModal {
	const root = createRoot(document.querySelector<HTMLDivElement>('#addRecordModalBody')!);

	const modalElement = document.querySelector<HTMLDivElement>('#addRecordModal')!;
	const modal = Modal.getOrCreateInstance(modalElement);

	export function App(): React.JSX.Element {
		const [isVisible, setIsVisible] = React.useState<boolean>(false);

		React.useEffect(() => {
			modalElement.addEventListener('shown.bs.modal', () => setIsVisible(true));
			modalElement.addEventListener('hidden.bs.modal', () => setIsVisible(false));
			addButtonElement.addEventListener('click', () => modal.show());
		}, []);

		async function handleOnAdd(): Promise<void> {
			modal.hide()

			await RecordListGroup.update();
		}

		return isVisible ? <AddRecordModalBody onAdd={handleOnAdd} onCancel={() => modal.hide()} /> : <></>;
	}

	root.render(<App />);
}

updateButtonElement.addEventListener('click', async (): Promise<void> => await RecordListGroup.update());