import React, { ReactElement, useEffect } from 'react';
import { Params, json } from 'react-router-dom';
import ClipboardJS from 'clipboard';

import Title from 'components/Title';

import SystemVariables from './components/SystemVariables';
import UserVariables from './components/UserVariables';

import useToast from 'services/hooks/useToast';

import { TelegramBotVariablesAPI } from 'services/api/telegram_bots/main';
import { APIResponse } from 'services/api/telegram_bots/types';

export interface UserVariablesPaginationData extends Omit<APIResponse.TelegramBotVariablesAPI.Get.Pagination, 'next' | 'previous'> {
	limit: number;
	offset: number;
}

export interface LoaderData {
	userVariablesPaginationData: UserVariablesPaginationData;
}

export async function loader({ params }: { params: Params<'telegramBotID'> }): Promise<LoaderData | Response> {
	const telegramBotID: number = parseInt(params.telegramBotID!);
	const [limit, offset] = [10, 0];

	const response = await TelegramBotVariablesAPI.get(telegramBotID, limit, offset);

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return {
		userVariablesPaginationData: {
			count: response.json.count,
			limit,
			offset,
			results: response.json.results,
		},
	}
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
			level: 'error',
		}));
	}, []);

	return (
		<Title title={gettext('Переменные')}>
			<SystemVariables />
			<UserVariables />
		</Title>
	);
}

export default Variables;