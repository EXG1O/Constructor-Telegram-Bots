import React, { ReactNode, CSSProperties, Dispatch, SetStateAction, useEffect, useState } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';
import Form from 'react-bootstrap/Form';
import Spinner from 'react-bootstrap/Spinner';

import useToast from 'services/hooks/useToast';

import { TelegramBotAPI } from 'services/api/telegram_bots/main';
import { TelegramBot } from 'services/api/telegram_bots/types';

import { telegramBotIsStartingOrStopping } from 'utils/telegram_bot';

const buttonOnlyWithIconStyle: CSSProperties = {
	cursor: 'pointer',
	fontSize: '20px',
}

export interface TelegramBotCardProps extends CardProps {
	telegramBot: TelegramBot;
	setTelegramBot?: Dispatch<SetStateAction<TelegramBot>>;
}

function TelegramBotCard({ telegramBot: telegramBotInitial, setTelegramBot: setTelegramBotInitial, ...props }: TelegramBotCardProps): ReactNode {
	const { createMessageToast } = useToast();

	const [telegramBot, setTelegramBot] = setTelegramBotInitial === undefined ? useState<TelegramBot>(telegramBotInitial) : [telegramBotInitial, setTelegramBotInitial];
	const [apiTokenInputValue, setAPITokenInputValue] = useState<string>(telegramBot.api_token);
	const [apiTokenIsEditing, setAPITokenIsEditing] = useState<boolean>(false);

	async function checkTelegramBotStatus(): Promise<void> {
		const response = await TelegramBotAPI.get(telegramBot.id);

		if (response.ok) {
			if (telegramBotIsStartingOrStopping(response.json)) {
				setTimeout(checkTelegramBotStatus, 3000);
			} else {
				setTelegramBot(response.json);
			}
		}
	}

	useEffect(() => {
		if (telegramBotIsStartingOrStopping(telegramBot)) {
			checkTelegramBotStatus();
		}
	}, [telegramBot.is_running, telegramBot.is_stopped]);

	function toggleAPITokenState(): void {
		if (!apiTokenIsEditing) {
			setAPITokenInputValue(telegramBot.api_token);
		}

		setAPITokenIsEditing(!apiTokenIsEditing);
	}

	async function handleAPITokenSaveButtonClick(): Promise<void> {
		const response = await TelegramBotAPI.update(telegramBot.id, { api_token: apiTokenInputValue });

		if (response.ok) {
			setTelegramBot(response.json.telegram_bot);
			toggleAPITokenState();
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	async function handleIsPrivateSwitchChange(): Promise<void> {
		const response = await TelegramBotAPI.update(telegramBot.id, { is_private: !telegramBot.is_private });

		if (response.ok) {
			setTelegramBot(response.json.telegram_bot);
		}

		createMessageToast({ message: response.json.message, level: response.json.level });
	}

	return (
		<Card {...props} className={(props.className ? `${props.className} ` : '') + 'border-0'}>
			<Card.Header as='h5' {...(
				telegramBotIsStartingOrStopping(telegramBot) ? {
					className: 'text-bg-secondary border border-secondary text-center',
					children: (
						<Spinner
							animation='border'
							style={{
								width: '1rem',
								height: '1rem',
								borderWidth: '0.2rem',
							}}
						/>
					),
				} : !telegramBot.is_running && telegramBot.is_stopped ? {
					className: 'text-bg-danger border border-danger fw-semibold text-center',
					children: gettext('Telegram бот выключен'),
				} : {
					className: 'text-bg-success border border-success fw-semibold text-center',
					children: gettext('Telegram бот включен'),
				}
			)} />
			<Card.Body className='border p-2'>
				<Table size='sm' borderless className='align-middle mb-0'>
					<tbody>
						<tr>
							<th scope='row'>@username:</th>
							<td className='text-break'>
								<a
									className='link-dark link-underline-opacity-0'
									href={`tg://resolve?domain=${telegramBot.username}`}
								>
									@{telegramBot.username}
								</a>
							</td>
						</tr>
						<tr>
							<th scope='row'>{gettext('API-токен')}:</th>
							<td>
								<div className='d-flex align-items-center gap-2'>
									{apiTokenIsEditing ? (
										<Form.Control
											type='text'
											value={apiTokenInputValue}
											placeholder={gettext('Введите API-токен Telegram бота')}
											onChange={(event) => setAPITokenInputValue(event.target.value)}
										/>
									) : (
										<span className='text-break flex-fill'>{telegramBot.api_token}</span>
									)}
									{apiTokenIsEditing ? (
										<>
											<i
												className='bi bi-check-lg text-success'
												style={{...buttonOnlyWithIconStyle, WebkitTextStroke: '1.4px'}}
												onClick={handleAPITokenSaveButtonClick}
											/>
											<i
												className='bi bi-x-lg text-danger'
												style={{...buttonOnlyWithIconStyle, WebkitTextStroke: '1.8px'}}
												onClick={toggleAPITokenState}
											/>
										</>
									) : (
										<i
											className='bi bi-pencil-square text-secondary'
											style={{...buttonOnlyWithIconStyle, WebkitTextStroke: '0.4px'}}
											onClick={toggleAPITokenState}
										/>
									)}
								</div>
							</td>
						</tr>
						<tr>
							<th scope='row'>{gettext('Приватный')}:</th>
							<td>
								<Form.Switch
									defaultChecked={telegramBot.is_private}
									onChange={handleIsPrivateSwitchChange}
								/>
							</td>
						</tr>
						<tr>
							<th scope='row'>{gettext('Добавлен')}:</th>
							<td>{telegramBot.added_date}</td>
						</tr>
					</tbody>
				</Table>
			</Card.Body>
			{props.children}
		</Card>
	);
}

export default TelegramBotCard;