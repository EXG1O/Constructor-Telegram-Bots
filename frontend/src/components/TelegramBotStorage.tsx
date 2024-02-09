import React, { ReactElement, memo } from 'react';

import ProgressBar from 'react-bootstrap/ProgressBar';

import { TelegramBot } from 'services/api/telegram_bots/types';

export interface TelegramBotStorageProps {
	telegramBot: TelegramBot;
	usedStorageSize?: number;
}

function TelegramBotStorage({ telegramBot, usedStorageSize = telegramBot.used_storage_size}: TelegramBotStorageProps): ReactElement<TelegramBotStorageProps> {
	return (
		<div className='d-flex gap-2' style={{ fontSize: '12px' }}>
			<span>{`${(usedStorageSize / 1024 ** 2).toFixed(2)} MB`}</span>
			<ProgressBar
				variant='dark'
				now={usedStorageSize}
				max={telegramBot.storage_size}
				className='flex-fill align-self-center'
			/>
			<span>{`${(telegramBot.storage_size / 1024 ** 2).toFixed(2)} MB`}</span>
		</div>
	);
}

export default memo(TelegramBotStorage);