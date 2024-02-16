import React, { ReactElement, ReactNode, Dispatch, SetStateAction, memo, useEffect, useState } from 'react';
import classNames from 'classnames';

import Card, { CardProps } from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';
import Form from 'react-bootstrap/Form';

import Loading from './Loading';
import TelegramBotStorage from './TelegramBotStorage';

import useToast from 'services/hooks/useToast';

import { TelegramBotAPI } from 'services/api/telegram_bots/main';
import { TelegramBot } from 'services/api/telegram_bots/types';

export interface TelegramBotCardChildrenProps {
	telegramBot: TelegramBot;
	setTelegramBot: Dispatch<SetStateAction<TelegramBot>>;
}

export interface TelegramBotCardProps extends Omit<CardProps, 'children'> {
	telegramBot: TelegramBot;
	children: (props: TelegramBotCardChildrenProps) => ReactNode;
}

function TelegramBotCard({ telegramBot: initialTelegramBot, ...props }: TelegramBotCardProps): ReactElement<TelegramBotCardProps> {
	const { createMessageToast } = useToast();

	const [telegramBot, setTelegramBot] = useState<TelegramBot>(initialTelegramBot);
	const [apiTokenInputValue, setAPITokenInputValue] = useState<string>(telegramBot.api_token);
	const [apiTokenIsEditing, setAPITokenIsEditing] = useState<boolean>(false);

	async function checkTelegramBotStatus(): Promise<void> {
		const response = await TelegramBotAPI.get(telegramBot.id);

		if (response.ok) {
			if (telegramBot.is_loading) {
				setTimeout(checkTelegramBotStatus, 3000);
			} else {
				setTelegramBot(response.json);
			}
		}
	}

	useEffect(() => {
		if (telegramBot.is_loading) {
			checkTelegramBotStatus();
		}
	}, [telegramBot.is_loading]);

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
		<Card {...props} className={classNames('border-0', props.className)}>
			<Card.Header as='h5' {...(
				telegramBot.is_loading ? {
					className: 'd-flex justify-content-center juitext-bg-secondary text-bg-secondary border-secondary text-center',
					children: <Loading size='xs' />,
				} : telegramBot.is_enabled ? {
					className: 'text-bg-success border-success fw-semibold text-center',
					children: gettext('Telegram бот включен'),
				} : {
					className: 'text-bg-danger border-danger fw-semibold text-center',
					children: gettext('Telegram бот выключен'),
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
											size='sm'
											type='text'
											value={apiTokenInputValue}
											placeholder={gettext('Введите API-токен Telegram бота')}
											style={{ fontSize: '16px' }}
											onChange={(event) => setAPITokenInputValue(event.target.value)}
										/>
									) : (
										<span className='text-break flex-fill'>
											{telegramBot.api_token}
										</span>
									)}
									{apiTokenIsEditing ? (
										<div className='d-flex gap-1'>
											<i
												className='bi bi-check-lg text-success'
												style={{ cursor: 'pointer', fontSize: '22px', WebkitTextStroke: '0.3px' }}
												onClick={handleAPITokenSaveButtonClick}
											/>
											<i
												className='bi bi-x-lg text-danger my-auto'
												style={{ cursor: 'pointer', fontSize: '18px', WebkitTextStroke: '1px' }}
												onClick={toggleAPITokenState}
											/>
										</div>
									) : (
										<i
											className='d-flex bi bi-pencil-square text-secondary'
											style={{ cursor: 'pointer', fontSize: '19px' }}
											onClick={toggleAPITokenState}
										/>
									)}
								</div>
							</td>
						</tr>
						<tr>
							<th scope='row'>{gettext('Хранилище')}:</th>
							<td><TelegramBotStorage telegramBot={telegramBot} /></td>
						</tr>
						<tr>
							<th scope='row'>{gettext('Приватный')}:</th>
							<td>
								<Form.Switch
									checked={telegramBot.is_private}
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
			{props.children?.({ telegramBot, setTelegramBot })}
		</Card>
	);
}

export default memo(TelegramBotCard);