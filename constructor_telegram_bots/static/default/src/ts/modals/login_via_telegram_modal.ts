import * as bootstrap from 'bootstrap';
import * as QRCode from 'qrcode';

declare const userIsAuth: boolean;

if (!userIsAuth) {
	const loginViaTelegramBootstrapModal = new bootstrap.Modal('#loginViaTelegramModal');
	const loginViaTelegramModalButton = document.querySelector('#loginViaTelegramModalButton') as HTMLAnchorElement;

	QRCode.toCanvas(
		document.querySelector('#loginViaTelegramModal .qrcode') as HTMLCanvasElement,
		loginViaTelegramModalButton.href,
		{
			width: 256,
			margin: 0,
		},
	);

	loginViaTelegramModalButton.addEventListener('click', (): void => loginViaTelegramBootstrapModal.toggle());

	if (new URLSearchParams(window.location.search).has('require-login')) {
		loginViaTelegramModalButton.click();
	}
}