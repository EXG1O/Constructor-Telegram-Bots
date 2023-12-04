import { Modal } from 'bootstrap';
import QRCode from 'qrcode';

declare const userIsAuth: boolean;

if (!userIsAuth) {
	const modal = new Modal('#loginViaTelegramModal');
	const modalToggleButtonElement = document.querySelector<HTMLAnchorElement>('#loginViaTelegramModalButton')!;

	QRCode.toCanvas(
		document.querySelector<HTMLCanvasElement>('#loginViaTelegramModal .qrcode'),
		modalToggleButtonElement.href,
		{width: 256, margin: 0},
	);

	modalToggleButtonElement.addEventListener('click', (): void => modal.toggle());

	if (new URLSearchParams(window.location.search).has('require-login')) {
		modalToggleButtonElement.click();
	}
}