import React, { ReactElement, MouseEvent, memo, useCallback, useState } from 'react';

import Button, { ButtonProps } from 'react-bootstrap/Button';

import LoginModal from './LoginModal';

export type LoginButtonProps = Omit<ButtonProps, 'as' | 'href' | 'target' | 'variant' | 'children'>;

function LoginButton(props: LoginButtonProps): ReactElement<LoginButtonProps> {
	const [showLoginModal, setShowLoginModal] = useState<boolean>(false);

	function handleButtonClick(event: MouseEvent<HTMLButtonElement>): void {
		setShowLoginModal(true);
		props.onClick?.(event);
	}

	return (
		<>
			<LoginModal
				show={showLoginModal}
				onHide={useCallback(() => setShowLoginModal(false), [])}
			/>
			<Button
				{...props}
				as='a'
				href={`tg://resolve?domain=${process.env.TELEGRAM_BOT_USERNAME}&start=login`}
				variant='success'
				onClick={handleButtonClick}
			>
				<i className='bi bi-telegram me-1' />
				{gettext('Войти через Telegram')}
			</Button>
		</>
	);
}

export default memo(LoginButton);