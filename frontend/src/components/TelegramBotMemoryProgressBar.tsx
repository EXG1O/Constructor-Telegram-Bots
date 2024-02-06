import React, { ReactElement, memo } from 'react';

import ProgressBar from 'react-bootstrap/ProgressBar';

import { TelegramBot } from 'services/api/telegram_bots/types';

export interface TelegramBotMemoryProgressBarProps {
	telegramBot: TelegramBot;
	usedMemory?: number;
}

function TelegramBotMemoryProgressBar({
	telegramBot,
	usedMemory = telegramBot.used_memory,
}: TelegramBotMemoryProgressBarProps): ReactElement<TelegramBotMemoryProgressBarProps> {
	return (
		<div className='d-flex gap-2' style={{ fontSize: '12px' }}>
			<span>{`${(usedMemory / 1024 ** 2).toFixed(2)} MB`}</span>
			<ProgressBar
				variant='dark'
				now={usedMemory}
				max={telegramBot.memory_limit}
				className='flex-fill align-self-center'
			/>
			<span>{`${(telegramBot.memory_limit / 1024 ** 2).toFixed(2)} MB`}</span>
		</div>
	);
}

export default memo(TelegramBotMemoryProgressBar);