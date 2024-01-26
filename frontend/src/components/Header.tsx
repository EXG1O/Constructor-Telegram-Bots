import React, { ReactElement, ReactNode, useCallback, useState } from 'react';
import { Link, LinkProps, useLocation, useNavigate, useRouteLoaderData } from 'react-router-dom';
import classNames from 'classnames';

import Container from 'react-bootstrap/Container';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Dropdown from 'react-bootstrap/Dropdown';
import Button from 'react-bootstrap/Button';

import LoginModal from './LoginModal';
import AskConfirmModal from './AskConfirmModal';

import useToast from 'services/hooks/useToast';

import { LoaderData as RootLoaderData } from 'routes/Root';

import { UserAPI } from 'services/api/users/main';
import { LanguagesAPI } from 'services/api/languages/main';

export interface HeaderLinkProps extends LinkProps {
	children: ReactNode;
}

const headerLinks: HeaderLinkProps[] = [
	{ to: '/', children: gettext('Главная') },
	{ to: '/team/', children: gettext('Команда') },
	{ to: '/updates/', children: gettext('Обновления') },
	{ to: '/instruction/', children: gettext('Инструкция') },
	{ to: '/donation/', children: gettext('Пожертвование') },
];

function Header(): ReactElement {
	const location = useLocation();
	const navigate = useNavigate();
	const { user, languages } = useRouteLoaderData('root') as RootLoaderData;

	const { createMessageToast } = useToast();

	const [showLoginModal, setShowLoginModal] = useState<boolean>(false);
	const [showLogoutModal, setShowLogoutModal] = useState<boolean>(false);
	const [loadingLogoutModal, setLoadingLogoutModal] = useState<boolean>(false);

	const handleConfirmLogout = useCallback(async () => {
		setLoadingLogoutModal(true);

		const response = await UserAPI.logout();

		if (response.ok) {
			setShowLogoutModal(false);
			navigate('/');
		}

		setLoadingLogoutModal(false);
		createMessageToast({ message: response.json.message, level: response.json.level });
	}, []);

	async function setLanguage(langCode: string): Promise<void> {
		const response = await LanguagesAPI.set({ lang_code: langCode });

		if (response.ok) {
			window.location.href = location.pathname;
		} else {
			createMessageToast({ message: response.json.message, level: response.json.level });
		}
	}

	return (
		<>
			{user ? (
				<AskConfirmModal
					show={showLogoutModal}
					loading={loadingLogoutModal}
					title={gettext('Выход из аккаунта')}
					onConfirm={handleConfirmLogout}
					onHide={useCallback(() => setShowLogoutModal(false), [])}
				>
					{gettext('Вы точно хотите выйти из аккаунта?')}
				</AskConfirmModal>
			) : (
				<LoginModal
					show={showLoginModal}
					onHide={useCallback(() => setShowLoginModal(false), [])}
				/>
			)}
			<Navbar expand='xxl' variant='dark' className='bg-dark'>
				<Container>
					<Navbar.Brand>Constructor Telegram Bots</Navbar.Brand>
					<Navbar.Toggle aria-controls='header' />
					<Navbar.Collapse className='justify-content-between' id='header'>
						<Nav variant='underline' className='gap-0'>
							{headerLinks.map((props, index) => (
								<Link
									key={index}
									{...props}
									className={
										classNames(
											'nav-link pb-1',
											location.pathname === props.to ? 'active' : undefined,
											props.className,
										)
									}
								/>
							))}
						</Nav>
						<hr className='d-xxl-none text-white-50 mt-0 mb-2'></hr>
						<div className='d-flex flex-wrap gap-2'>
							<Dropdown>
								<Dropdown.Toggle
									bsPrefix=' '
									variant='primary'
								>
									{languages.current.toUpperCase()}
								</Dropdown.Toggle>
								<Dropdown.Menu className='text-center'>
									{Object.entries(languages.available).map((language, index) => (
										<Dropdown.Item
											key={index}
											onClick={() => setLanguage(language[0])}
										>
											{language[1]}
										</Dropdown.Item>
									))}
								</Dropdown.Menu>
							</Dropdown>
							{user ? (
								<Dropdown>
									<Dropdown.Toggle
										bsPrefix=' '
										variant='light'
										style={{ minWidth: '125px' }}
									>
										{user.first_name}
									</Dropdown.Toggle>
									<Dropdown.Menu>
										{user.is_staff && (
											<Dropdown.Item href='/admin/'>
												{gettext('Админ панель')}
											</Dropdown.Item>
										)}
										<Dropdown.Item
											onClick={() => navigate('/personal-cabinet/')}
										>
											{gettext('Личный кабинет')}
										</Dropdown.Item>
										<Dropdown.Item>
											{gettext('Настройки')}
										</Dropdown.Item>
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
									href={`https://t.me/${process.env.TELEGRAM_BOT_USERNAME}?start=login`}
									target='_blank'
									variant='success'
									className='flex-fill'
									onClick={() => setShowLoginModal(true)}
								>
									<i className='bi bi-telegram me-1' />
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