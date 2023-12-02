import { Toast } from 'global_modules/toast';
import { TelegramBotApi } from 'telegram_bot_api/main';
import { TelegramBot } from 'telegram_bot_api/types';
import React from 'react';

declare const telegramBotCardHeaderIsRunningText: string;
declare const telegramBotCardHeaderIsNotRunningText: string;
declare const telegramBotCardBodyTableLineApiTokenText: string;
declare const telegramBotCardBodyTableLineApiTokenInputPlaceholderText: string;
declare const telegramBotCardBodyTableLineIsPrivateText: string;
declare const telegramBotCardBodyTableLineDateAddedText: string;

type TelegramBotContextType = {
	telegramBot: TelegramBot;
	setTelegramBot: React.Dispatch<React.SetStateAction<TelegramBot>>;
}

export const TelegramBotContext = React.createContext<TelegramBotContextType | undefined>(undefined);

function TelegramBotCardHeader(): React.JSX.Element {
	const telegramBotContext = React.useContext(TelegramBotContext);

	if (telegramBotContext) {
		const telegramBot = telegramBotContext.telegramBot;
		let color: 'success' | 'danger', text: string;

		if (!telegramBot.is_running && telegramBot.is_stopped) {
			[color, text] = ['danger', telegramBotCardHeaderIsNotRunningText];
		} else {
			[color, text] = ['success', telegramBotCardHeaderIsRunningText];
		}

		return <h5 className={`card-header text-bg-${color} border border-${color} fw-semibold text-center`}>{text}</h5>;
	} else {
		return <></>;
	}
}

function TelegramBotCardBody(): React.JSX.Element {
	const telegramBotContext = React.useContext(TelegramBotContext);

	if (telegramBotContext) {
		const [telegramBot, setTelegramBot] = [telegramBotContext.telegramBot, telegramBotContext.setTelegramBot];
		const [apiTokenIsEditing, setApiTokenAsEditing] = React.useState<boolean>(false);
		const [apiTokenInputValue, setApiTokenInputValue] = React.useState<string>(telegramBot.api_token);

		const buttonStyle: React.CSSProperties = {
			cursor: 'pointer',
			fontSize: '20px',
		}

		function toggleApiToken (): void {
			if (!apiTokenIsEditing) {
				setApiTokenInputValue(telegramBot.api_token);
			}

			setApiTokenAsEditing(!apiTokenIsEditing);
		}

		async function handleApiTokenSaveButtonClick(): Promise<void> {
			const response = await TelegramBotApi.update(telegramBot.id, {
				api_token: apiTokenInputValue,
				is_private: null,
			});

			if (response.ok) {
				setTelegramBot({...telegramBot, api_token: apiTokenInputValue});
				toggleApiToken();
			}

			new Toast(response.json.message, response.json.level).show();
		}

		async function handleIsPrivateCheckboxChange(event: {target:{checked: boolean}}): Promise<void> {
			const response = await TelegramBotApi.update(telegramBot.id, {
				api_token: null,
				is_private: event.target.checked,
			});

			if (response.ok) {
				setTelegramBot({...telegramBot, is_private: event.target.checked});
			}

			new Toast(response.json.message, response.json.level).show();
		}

		return (
			<div className='card-body border p-2'>
				<table className='table table-sm table-borderless align-middle mb-0'>
					<tbody>
						<tr>
							<th scope='row'>@username:</th>
							<td className='text-break'>
								<a
									className='link-dark link-underline-opacity-0'
									href={`tg://resolve?domain=${telegramBot.username}`}
								>@{telegramBot.username}</a>
							</td>
						</tr>
						<tr>
							<th scope='row'>{telegramBotCardBodyTableLineApiTokenText}:</th>
							<td className='text-break'>
								<div className='d-flex gap-2'>
									{apiTokenIsEditing ? (
										<input
											className='form-control'
											type='text'
											onChange={(event) => setApiTokenInputValue(event.target.value)}
											placeholder={telegramBotCardBodyTableLineApiTokenInputPlaceholderText}
											value={apiTokenInputValue}
										/>
									) : (
										<span className='flex-fill'>{telegramBot.api_token}</span>
									)}
									<div className='d-flex justify-content-center align-items-center gap-1'>
										{apiTokenIsEditing ? (
											<>
												<i
													className='bi bi-check-lg text-success'
													onClick={handleApiTokenSaveButtonClick}
													style={{...buttonStyle, WebkitTextStroke: '1.4px'}}
												></i>
												<i
													className='bi bi-x-lg text-danger'
													onClick={toggleApiToken}
													style={{...buttonStyle, WebkitTextStroke: '1.8px'}}
												></i>
											</>
										) : (
											<i
												className='bi bi-pencil-square text-secondary'
												onClick={toggleApiToken}
												style={{...buttonStyle, WebkitTextStroke: '0.4px'}}
											></i>
										)}
									</div>
								</div>
							</td>
						</tr>
						<tr>
							<th scope='row'>{telegramBotCardBodyTableLineIsPrivateText}:</th>
							<td>
								<div className='form-check form-switch mb-0'>
									<input
										className='form-check-input'
										type='checkbox'
										onChange={handleIsPrivateCheckboxChange}
										defaultChecked={telegramBot.is_private}
									/>
								</div>
							</td>
						</tr>
						<tr>
							<th scope='row'>{telegramBotCardBodyTableLineDateAddedText}:</th>
							<td>{telegramBot.added_date}</td>
						</tr>
					</tbody>
				</table>
			</div>
		)
	} else {
		return <></>;
	}
}

export function TelegramBotCard({telegramBotInitial, children}: {telegramBotInitial: TelegramBot, children?: React.ReactNode}): React.JSX.Element {
	const [telegramBot, setTelegramBot] = React.useState<TelegramBot>(telegramBotInitial);

	return (
		<div className='card border-0'>
			<TelegramBotContext.Provider value={{telegramBot, setTelegramBot}}>
				<TelegramBotCardHeader/>
				<TelegramBotCardBody/>
				{children}
			</TelegramBotContext.Provider>
		</div>
	);
}