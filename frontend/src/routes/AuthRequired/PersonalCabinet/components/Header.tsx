import React, { ReactElement, useState } from 'react';

import Button from 'react-bootstrap/Button';

import AddTelegramBotModal from './AddTelegramBotModal';

function Header(): ReactElement {
	const [showAddTelegramBotModal, setShowAddTelegramBotModal] = useState<boolean>(false);

	return (
		<>
			<AddTelegramBotModal
				show={showAddTelegramBotModal}
				onHide={(() => setShowAddTelegramBotModal(false))}
			/>
			<div className='d-flex flex-wrap justify-content-between gap-2'>
				<h1 className='flex-grow-1 flex-lg-grow-0 fw-semibold text-center mb-0'>
					{gettext('Добавленные Telegram боты')}
				</h1>
				<Button
					variant='dark'
					className='flex-grow-1 flex-lg-grow-0 align-self-center'
					onClick={() => setShowAddTelegramBotModal(true)}
				>
					<i className='bi bi-plus-lg me-1' style={{ WebkitTextStroke: '1px' }}></i>
					{gettext('Добавить Telegram бота')}
				</Button>
			</div>
		</>
	);
}

export default Header;