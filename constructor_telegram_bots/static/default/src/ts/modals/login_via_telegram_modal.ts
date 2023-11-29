import { Modal } from 'bootstrap';
import * as QRCode from 'qrcode';

declare const userIsAuth: boolean;

if (!userIsAuth) {
	const modal = new Modal('#loginViaTelegramModal');
	const modalToggleButtonElement = document.querySelector('#loginViaTelegramModalButton') as HTMLAnchorElement;

	QRCode.toCanvas(
		document.querySelector('#loginViaTelegramModal .qrcode') as HTMLCanvasElement,
		modalToggleButtonElement.href,
		{width: 256, margin: 0},
	);

	modalToggleButtonElement.addEventListener('click', (): void => modal.toggle());

	if (new URLSearchParams(window.location.search).has('require-login')) {
		modalToggleButtonElement.click();
	}
}