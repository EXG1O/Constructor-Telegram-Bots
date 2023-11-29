import { askConfirmModal } from 'global_modules/modals/ask_confirm_modal';

declare const userIsAuth: boolean;
declare const userLogoutUrl: string;
declare const userLogoutAskConfirmModalTitle: string;
declare const userLogoutAskConfirmModalText: string;

if (userIsAuth) {
	(document.querySelector('#userLogoutButton') as HTMLButtonElement).addEventListener('click', (): void => {
		askConfirmModal(
			userLogoutAskConfirmModalTitle,
			userLogoutAskConfirmModalText,
			(): string => window.location.href = userLogoutUrl,
		);
	});
}