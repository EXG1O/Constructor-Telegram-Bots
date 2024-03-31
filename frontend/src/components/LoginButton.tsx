import React, { ReactElement, MouseEvent, memo, useCallback, useState } from 'react';

import Button, { ButtonProps } from 'react-bootstrap/Button';

import LoginModal from './LoginModal';

export type LoginButtonProps = Omit<ButtonProps, 'as' | 'href' | 'target' | 'children'>;

function LoginButton({ onClick, ...props }: LoginButtonProps): ReactElement<LoginButtonProps> {
	const [showModal, setShowModal] = useState<boolean>(false);

	function handleButtonClick(event: MouseEvent<HTMLButtonElement>): void {
		setShowModal(true);
		onClick?.(event);
	}

	return (
		<>
			<LoginModal
				show={showModal}
				onHide={useCallback(() => setShowModal(false), [])}
			/>
			<Button
				{...props}
				as='a'
				href={`tg://resolve?domain=${process.env.TELEGRAM_BOT_USERNAME}&start=login`}
				onClick={handleButtonClick}
			>
				<i className='bi bi-telegram me-1' />
				{gettext('Войти через Telegram')}
			</Button>
		</>
	);
}

export default memo(LoginButton);