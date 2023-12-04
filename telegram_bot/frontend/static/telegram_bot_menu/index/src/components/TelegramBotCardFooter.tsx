import Toast from 'global_modules/toast';
import { askConfirmModal } from 'global_modules/modals/ask_confirm_modal';
import { TelegramBotApi } from 'telegram_bot_api/main';
import { TelegramBotContext } from 'telegram_bot_frontend/components/TelegramBotCard';
import React from 'react';

declare const personalCabinetUrl: string;
declare const askConfirmModalDeleteTelegramBotTitle: string;
declare const askConfirmModalDeleteTelegramBotText: string;
declare const telegramBotCardFooterStartButtonText: string;
declare const telegramBotCardFooterStopButtonText: string;
declare const telegramBotCardFooterDeleteButtonText: string;

export default function TelegramBotCardFooter(): React.JSX.Element {
	const telegramBotContext = React.useContext(TelegramBotContext)!;
	const telegramBot = telegramBotContext.telegramBot;

	function handleDeleteButtonClick(): void {
		askConfirmModal(
			askConfirmModalDeleteTelegramBotTitle,
			askConfirmModalDeleteTelegramBotText,
			async (): Promise<void> => {
				const response = await TelegramBotApi.delete_(telegramBot.id);

				if (response.ok) {
					setTimeout((): string => window.location.href = personalCabinetUrl, 2000);
				}

				new Toast(response.json.message, response.json.level).show();
			},
		);
	}

	return (
		<div className='card-footer d-flex flex-wrap border border-top-0 p-3 gap-3'>
			{!telegramBot.is_running && telegramBot.is_stopped ? (
				<button
					className='btn btn-success flex-fill'
					type='button'
					onClick={() => TelegramBotApi.start(telegramBot.id)}
				>{telegramBotCardFooterStartButtonText}</button>
			) : (
				<button
					className='btn btn-danger flex-fill'
					type='button'
					onClick={() => TelegramBotApi.stop(telegramBot.id)}
				>{telegramBotCardFooterStopButtonText}</button>
			)}
			<button
				className='btn btn-danger flex-fill'
				type='button'
				onClick={handleDeleteButtonClick}
			>{telegramBotCardFooterDeleteButtonText}</button>
		</div>
	);
}