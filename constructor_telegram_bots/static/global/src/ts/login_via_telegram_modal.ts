import * as bootstrap from 'bootstrap';

declare const QRCode: any;

const loginViaTelegramBootstrapModal = new bootstrap.Modal('#loginViaTelegramModal');
const loginViaTelegramModalButton = document.querySelector('#loginViaTelegramModalButton') as HTMLAnchorElement;

new QRCode(
	document.querySelector('#loginViaTelegramModal .qrcode') as HTMLDivElement,
	loginViaTelegramModalButton.href,
);

loginViaTelegramModalButton.addEventListener('click', () => loginViaTelegramBootstrapModal.toggle());

if (new URLSearchParams(window.location.search).has('require-login')) {
	loginViaTelegramModalButton.click();
}