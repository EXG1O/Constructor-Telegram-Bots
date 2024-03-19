import React, { ReactElement, HTMLAttributes, memo, useCallback, useState } from 'react';
import classNames from 'classnames';

import AddButton from 'components/AddButton';

import TelegramBotAdditionModal from './TelegramBotAdditionModal';

export type HeaderProps = HTMLAttributes<HTMLDivElement>;

function Header(props: HeaderProps): ReactElement<HeaderProps> {
	const [showTelegramBotAdditionModal, setShowTelegramBotAdditionModal] = useState<boolean>(false);

	return (
		<>
			<TelegramBotAdditionModal
				show={showTelegramBotAdditionModal}
				onHide={useCallback(() => setShowTelegramBotAdditionModal(false), [])}
			/>
			<div {...props} className={classNames('d-flex flex-wrap justify-content-between gap-2', props.className)}>
				<h1 className='flex-grow-1 flex-lg-grow-0 fw-semibold text-center mb-0'>
					{gettext('Добавленные Telegram боты')}
				</h1>
				<AddButton
					variant='dark'
					className='flex-grow-1 flex-lg-grow-0 align-self-center'
					onClick={useCallback(() => setShowTelegramBotAdditionModal(true), [])}
				>
					{gettext('Добавить Telegram бота')}
				</AddButton>
			</div>
		</>
	);
}

export default memo(Header);