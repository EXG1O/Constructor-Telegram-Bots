import React, { ReactElement, useCallback, useState } from 'react';

import Button from 'react-bootstrap/Button';

import TelegramBotAdditionModal from './TelegramBotAdditionModal';

function Header(): ReactElement {
	const [showTelegramBotAdditionModal, setShowTelegramBotAdditionModal] = useState<boolean>(false);

	return (
		<>
			<TelegramBotAdditionModal
				show={showTelegramBotAdditionModal}
				onHide={useCallback(() => setShowTelegramBotAdditionModal(false), [])}
			/>
			<div className='d-flex flex-wrap justify-content-between gap-2'>
				<h1 className='flex-grow-1 flex-lg-grow-0 fw-semibold text-center mb-0'>
					{gettext('Добавленные Telegram боты')}
				</h1>
				<Button
					variant='dark'
					className='flex-grow-1 flex-lg-grow-0 align-self-center'
					onClick={() => setShowTelegramBotAdditionModal(true)}
				>
					<i
						className='bi bi-plus-lg me-1'
						style={{ WebkitTextStroke: '1px' }}
					/>
					{gettext('Добавить Telegram бота')}
				</Button>
			</div>
		</>
	);
}

export default Header;