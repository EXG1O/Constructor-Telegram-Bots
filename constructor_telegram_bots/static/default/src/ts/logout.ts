import {askConfirmModal} from 'global_modules/modals/ask_confirm_modal';

declare const userIsAuth: boolean;
declare const userLogoutUrl: string;
declare const userLogoutAskConfirmModalTitle: string;
declare const userLogoutAskConfirmModalText: string;

if (userIsAuth) {
	const userLogoutButton = document.querySelector('#userLogoutButton') as HTMLButtonElement;

	userLogoutButton.addEventListener('click', (): void => askConfirmModal(
		userLogoutAskConfirmModalTitle,
		userLogoutAskConfirmModalText,
		() => window.location.href = userLogoutUrl,
	));
}