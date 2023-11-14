import {askConfirmModal} from 'global_modules/modals/ask_confirm_modal';

declare const userLogoutAskConfirmModalTitle: string;
declare const userLogoutAskConfirmModalText: string;
declare const userLogoutUrl: string;

const userLogoutButton = document.querySelector('#userLogoutButton') as HTMLButtonElement;

userLogoutButton.addEventListener('click', () => askConfirmModal(
	userLogoutAskConfirmModalTitle,
	userLogoutAskConfirmModalText,
	() => window.location.href = userLogoutUrl,
));