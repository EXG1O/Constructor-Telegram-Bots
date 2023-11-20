import * as bootstrap from 'bootstrap';

const askConfirmBootstrapModal = new bootstrap.Modal('#askConfirmModal');
const askConfirmModalTitle = document.querySelector('#askConfirmModalTitle') as HTMLHeadingElement;
const askConfirmModalBody = document.querySelector('#askConfirmModalBody') as HTMLDivElement;
const askConfirmModalYesButton = document.querySelector('#askConfirmModalYesButton') as HTMLButtonElement;

askConfirmModalYesButton.addEventListener('click', () => askConfirmBootstrapModal.toggle());

export function askConfirmModal(
	title: string,
	body: string,
	func: VoidFunction,
): void {
	askConfirmModalTitle.innerHTML = title;
	askConfirmModalBody.innerHTML = body;

	if (askConfirmModalYesButton.onclick) {
		askConfirmModalYesButton.removeEventListener('click', askConfirmModalYesButton.onclick);
	}
	askConfirmModalYesButton.onclick = func;

	askConfirmBootstrapModal.toggle();
}