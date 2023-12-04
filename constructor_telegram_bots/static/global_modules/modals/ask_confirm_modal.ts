import { Modal } from 'bootstrap';

const modal = new Modal('#askConfirmModal');
const titleElement = document.querySelector<HTMLHeadingElement>('#askConfirmModalTitle')!;
const bodyElement = document.querySelector<HTMLDivElement>('#askConfirmModalBody')!;
const yesButtonElement = document.querySelector<HTMLButtonElement>('#askConfirmModalYesButton')!;

yesButtonElement.addEventListener('click', (): void => modal.toggle());

export function askConfirmModal(title: string, body: string, func: () => any): void {
	titleElement.innerHTML = title;
	bodyElement.innerHTML = body;

	if (yesButtonElement.onclick) {
		yesButtonElement.removeEventListener('click', yesButtonElement.onclick);
	}
	yesButtonElement.onclick = func;

	modal.toggle();
}