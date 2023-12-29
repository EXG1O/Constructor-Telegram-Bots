import React, { ReactElement, useCallback, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { LinkContainer } from 'react-router-bootstrap';
import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Dropdown from 'react-bootstrap/Dropdown';
import Button from 'react-bootstrap/Button';

import LoginViaTelegramModal from './LoginViaTelegramModal';
import AskConfirmModal from './AskConfirmModal';

import useUser from 'services/hooks/useUser';

import { UserAPI } from 'services/api/users/main';

function Header(): ReactElement {
	const navigate = useNavigate();
	const user = useUser();

	const [showLoginViaTelegramModal, setShowLoginViaTelegramModal] = useState<boolean>(false);
	const [showLogoutModal, setShowLogoutModal] = useState<boolean>(false);

	const handleConfirmLogoutButtonClick = useCallback(async (): Promise<void> => {
		setShowLogoutModal(false);

		await UserAPI.logout();

		navigate('/');
	}, []);

	return (
		<>
			{user ? (
				<AskConfirmModal
					show={showLogoutModal}
					title={gettext('Выход из аккаунта')}
					onHide={useCallback(() => setShowLogoutModal(false), [])}
					onConfirmButtonClick={handleConfirmLogoutButtonClick}
				>
					{gettext('Вы точно хотите выйти из аккаунта?')}
				</AskConfirmModal>
			) : (
				<LoginViaTelegramModal
					show={showLoginViaTelegramModal}
					onHide={useCallback(() => setShowLoginViaTelegramModal(false), [])}
				/>
			)}
			<Navbar expand='xxl' variant='dark' className='bg-dark'>
				<Container>
					<LinkContainer to='/' activeClassName=''>
						<Navbar.Brand>Constructor Telegram Bots</Navbar.Brand>
					</LinkContainer>
					<Navbar.Toggle aria-controls='header'></Navbar.Toggle>
					<Navbar.Collapse className='justify-content-between' id='header'>
						<Nav variant='underline' className='gap-0'>
							<LinkContainer to='/'>
								<Nav.Link className='pb-1'>{gettext('Главная')}</Nav.Link>
							</LinkContainer>
							<LinkContainer to='/team/'>
								<Nav.Link className='pb-1'>{gettext('Команда')}</Nav.Link>
							</LinkContainer>
							<LinkContainer to='/updates/'>
								<Nav.Link className='pb-1'>{gettext('Обновления')}</Nav.Link>
							</LinkContainer>
							<LinkContainer to='/instruction/'>
								<Nav.Link className='pb-1'>{gettext('Инструкция')}</Nav.Link>
							</LinkContainer>
							<LinkContainer to='/donation/'>
								<Nav.Link className='pb-1'>{gettext('Пожертвование')}</Nav.Link>
							</LinkContainer>
						</Nav>
						<hr className='d-xxl-none text-white-50 mt-0 mb-2'></hr>
						<div className='d-flex flex-wrap gap-2'>
							{user ? (
								<Dropdown>
									<Dropdown.Toggle
										bsPrefix=' '
										variant='light'
										style={{ minWidth: 125 }}
									>
										{user.first_name}
									</Dropdown.Toggle>
									<Dropdown.Menu>
										{user.is_staff && (
											<Dropdown.Item href='/admin/'>{gettext('Админ панель')}</Dropdown.Item>
										)}
										<LinkContainer to='/personal-cabinet/'>
											<Dropdown.Item>{gettext('Личный кабинет')}</Dropdown.Item>
										</LinkContainer>
										<Dropdown.Item>{gettext('Настройки')}</Dropdown.Item>
										<Dropdown.Divider />
										<Dropdown.Item
											as='button'
											onClick={() => setShowLogoutModal(true)}
										>
											{gettext('Выйти')}
										</Dropdown.Item>
									</Dropdown.Menu>
								</Dropdown>
							) : (
								<Button
									as='a'
									variant='success'
									className='flex-fill'
									href=''
									onClick={() => setShowLoginViaTelegramModal(true)}
								>
									<i className='bi bi-telegram me-1'></i>
									{gettext('Войти через Telegram')}
								</Button>
							)}
						</div>
					</Navbar.Collapse>
				</Container>
			</Navbar>
		</>
	);
}

export default Header;