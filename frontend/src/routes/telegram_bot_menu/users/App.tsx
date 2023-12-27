import React, { ReactNode, useEffect, useState } from 'react';
import { Params, useNavigate, useParams } from 'react-router-dom';
import * as fuzz from 'fuzzball';

import Card from 'react-bootstrap/Card';
import Stack from 'react-bootstrap/Stack';
import Form from 'react-bootstrap/Form';
import InputGroup from 'react-bootstrap/InputGroup';
import ListGroup from 'react-bootstrap/ListGroup';
import Button from 'react-bootstrap/Button';

import TelegramBotUser from './components/TelegramBotUser';

import { TelegramBotUsersAPI } from 'services/api/telegram_bots/main';
import { TelegramBotUser as TelegramBotUserType } from 'services/api/telegram_bots/types';

interface TelegramBotUsersIsSortedState {
	search: boolean;
}

function App(): ReactNode {
	const { telegramBotID } = useParams<Params<'telegramBotID'>>();
	const navigate = useNavigate();

	const [telegramBotUsers, setTelegramBotUsers] = useState<TelegramBotUserType[]>([]);
	const [sortedTelegramBotUsers, setSortedTelegramBotUsers] = useState<TelegramBotUserType[]>(telegramBotUsers);
	const [telegramBotUsersIsSorted, setTelegramBotUsersIsSorted] = useState<TelegramBotUsersIsSortedState>({ search: false });
	const [searchInputValue, setSearchInputValue] = useState<string>('');

	useEffect(() => { updateTelegramBotUsers() }, []);
	useEffect(() => {
		setSortedTelegramBotUsers(telegramBotUsers);

		if (telegramBotUsersIsSorted.search) {
			searchTelegramBotUser();
		}
	}, [telegramBotUsers]);

	async function updateTelegramBotUsers(): Promise<void> {
		const response = await TelegramBotUsersAPI.get(parseInt(telegramBotID!));

		if (response.ok) {
			setTelegramBotUsers(response.json);
		} else {
			navigate('/personal-cabinet/');
		}
	}

	function searchTelegramBotUser(): void {
		const choices: Record<number, string> = {};

		telegramBotUsers.forEach(telegramBotUser => choices[telegramBotUser.id] = telegramBotUser.full_name);

		const result: TelegramBotUserType[] = [];
		const stringMatchingResults = fuzz.extract(searchInputValue, choices, { scorer: fuzz.token_set_ratio });

		for (const stringMatchingResult of stringMatchingResults) {
			for (const telegramBotUser of telegramBotUsers) {
				if (stringMatchingResult[2] === telegramBotUser.id.toString()) {
					result.push(telegramBotUser);
					break;
				}
			}
		}

		setSortedTelegramBotUsers(result);
	}

	function handleSearchButtonClick(): void {
		searchTelegramBotUser();
		setTelegramBotUsersIsSorted({ ...telegramBotUsersIsSorted, search: true });
	}

	function handleCancelSearchButtonClick(): void {
		setSearchInputValue('');

		if (telegramBotUsersIsSorted.search) {
			setSortedTelegramBotUsers(telegramBotUsers);
			setTelegramBotUsersIsSorted({ ...telegramBotUsersIsSorted, search: true });
		}
	}

	return (
		<>
			<Card className='border'>
				<Card.Header as='h5' className='border-bottom text-center'>{gettext('Список пользователей')}</Card.Header>
				<Card.Body className='vstack gap-2'>
					<Stack direction='horizontal' gap={2}>
						<Button
							size='sm'
							variant='light'
							className='border bi bi-arrow-repeat px-2 py-0'
							style={{ fontSize: '20px' }}
							onClick={updateTelegramBotUsers}
						/>
						{telegramBotUsers.length > 0 && (
							<>
								<InputGroup>
									<Form.Control
										size='sm'
										className='flex-fill'
										value={searchInputValue}
										placeholder={gettext('Введите имя')}
										onChange={e => setSearchInputValue(e.target.value)}
									/>
									{searchInputValue !== '' && (
										<Button
											size='sm'
											variant='light'
											className='border bi bi-x-lg px-2'
											style={{ WebkitTextStrokeWidth: '0.8px' }}
											onClick={handleCancelSearchButtonClick}
										/>
									)}
								</InputGroup>
								<Button size='sm' variant='dark' onClick={handleSearchButtonClick}>
									{gettext('Поиск')}
								</Button>
							</>
						)}
					</Stack>
					<ListGroup>
						{telegramBotUsers.length ? (
							sortedTelegramBotUsers.map(telegramBotUser => (
								<ListGroup.Item key={telegramBotUser.id} className='p-3'>
									<TelegramBotUser
										telegramBotUser={telegramBotUser}
										updateTelegramBotUsers={updateTelegramBotUsers}
									/>
								</ListGroup.Item>
							))
						) : (
							<ListGroup.Item className='text-center p-3'>
								{gettext('Вашего Telegram бота ещё никто не активировал')}
							</ListGroup.Item>
						)}
					</ListGroup>
				</Card.Body>
			</Card>
		</>
	);
}

export default App;