import React, { ReactElement, useEffect } from 'react';
import { Params, json } from 'react-router-dom';
import ClipboardJS from 'clipboard';

import SystemVariables from './components/SystemVariables';
import UserVariables from './components/UserVariables';

import useToast from 'services/hooks/useToast';

import { TelegramBotVariablesAPI } from 'services/api/telegram_bots/main';
import { TelegramBotVariable } from 'services/api/telegram_bots/types';

export interface LoaderData {
	telegramBotVariables: TelegramBotVariable[];
}

export async function loader({ params }: { params: Params<'telegramBotID'> }): Promise<LoaderData | Response> {
	const { telegramBotID } = params;

	const response = await TelegramBotVariablesAPI.get(parseInt(telegramBotID!));

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return { telegramBotVariables: response.json };
}

function Variables(): ReactElement {
	const { createMessageToast } = useToast();

	useEffect(() => {
		const clipboard = new ClipboardJS('.btn-clipboard');

		clipboard.on('success', () => createMessageToast({
			message: gettext('Вы успешно скопировали переменную в буфер обмена.'),
			level: 'success',
		}));
		clipboard.on('error', () => createMessageToast({
			message: gettext('При попытки скопировать переменную в буфер обмена, непредвиденная ошибка!'),
			level: 'danger',
		}));
	}, []);

	return (
		<>
			<SystemVariables />
			<UserVariables />
		</>
	);
}

export default Variables;