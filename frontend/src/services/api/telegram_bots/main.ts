import { headersWithAuthToken, makeRequest } from 'services/api/base';
import { TelegramBot, TelegramBotCommand, TelegramBotCommandKeyboardButton, TelegramBotUser, Data, APIResponse } from './types';

const rootURL = '/api/telegram-bots/';

export namespace TelegramBotsAPI {
	export const get = () => makeRequest<TelegramBot[]>(rootURL, 'GET', headersWithAuthToken());
}

export namespace TelegramBotAPI {
	export const url = (telegramBotId: TelegramBot['id']): string => rootURL + `${telegramBotId}/`;

	export const get = (telegramBotId: TelegramBot['id']) => makeRequest<TelegramBot>(url(telegramBotId), 'GET', headersWithAuthToken());
	export const create = (data: Data.TelegramBotAPI.Create) => makeRequest<APIResponse.TelegramBotAPI.Create>(rootURL, 'POST', headersWithAuthToken(), data);
	export const update = (telegramBotId: TelegramBot['id'], data: Data.TelegramBotAPI.Update) => makeRequest<APIResponse.TelegramBotAPI.Update>(url(telegramBotId), 'PATCH', headersWithAuthToken(), data);
	export const delete_ = (telegramBotId: TelegramBot['id']) => makeRequest(url(telegramBotId), 'DELETE', headersWithAuthToken());

	export const start = (telegramBotId: TelegramBot['id']) => makeRequest(url(telegramBotId) +'start-or-stop/', 'POST', headersWithAuthToken());
	export const stop = start;
	
	export const updateDiagramCurrentScale = (
		telegramBotId: TelegramBot['id'],
		data: Data.TelegramBotAPI.UpdateDiagramCurrentScale,
	) => makeRequest(url(telegramBotId) + 'update-diagram-current-scale/', 'PATCH', headersWithAuthToken(), data);
}

export namespace TelegramBotCommandsAPI {
	export const url = (telegramBotId: TelegramBot['id']): string => TelegramBotAPI.url(telegramBotId) + 'commands/';

	export const get = (telegramBotId: TelegramBot['id']) => makeRequest<TelegramBotCommand[]>(url(telegramBotId), 'GET', headersWithAuthToken());
}

export namespace TelegramBotCommandAPI {
	export const url = (
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
	): string => TelegramBotCommandsAPI.url(telegramBotId) + `${telegramBotCommandId}/`;

	export const get = (
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
	) => makeRequest<TelegramBotCommand>(url(telegramBotId, telegramBotCommandId), 'GET', headersWithAuthToken());
	export function create(telegramBotId: TelegramBot['id'], data: Data.TelegramBotCommandAPI.Create) {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest(TelegramBotCommandsAPI.url(telegramBotId), 'POST', headersWithAuthToken(), formData);
	}
	export function update(
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
		data: Data.TelegramBotCommandAPI.Update,
	) {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest(TelegramBotCommandAPI.url(telegramBotId, telegramBotCommandId), 'PATCH', headersWithAuthToken(), formData);
	}
	export const delete_ = (
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
	) => makeRequest(url(telegramBotId, telegramBotCommandId), 'DELETE', headersWithAuthToken());

	export const updatePosition = (
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
		data: Data.TelegramBotCommandAPI.UpdatePosition,
	) => makeRequest(`${url(telegramBotId, telegramBotCommandId)}update-position/`, 'PATCH', headersWithAuthToken(), data);
}

export namespace TelegramBotCommandKeyboardButtonAPI {
	export const url = (
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
		telegramBotCommandKeyboardButtonId: TelegramBotCommandKeyboardButton['id'],
	): string => TelegramBotCommandAPI.url(telegramBotId, telegramBotCommandId) + `keyboard-buttons/${telegramBotCommandKeyboardButtonId}/telegram-bot-command/`;

	export const connect = (
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
		telegramBotCommandKeyboardButtonId: TelegramBotCommandKeyboardButton['id'],
		data: Data.TelegramBotCommandKeyboardButtonAPI.Connect,
	) => makeRequest(url(telegramBotId, telegramBotCommandId, telegramBotCommandKeyboardButtonId), 'POST', headersWithAuthToken(), data);
	export const disconnect = (
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
		telegramBotCommandKeyboardButtonId: TelegramBotCommandKeyboardButton['id'],
		data: Data.TelegramBotCommandKeyboardButtonAPI.Disconnect,
	) => makeRequest(url(telegramBotId, telegramBotCommandId, telegramBotCommandKeyboardButtonId), 'DELETE', headersWithAuthToken(), data);
}

export namespace TelegramBotUsersAPI {
	export const url = (telegramBotId: TelegramBot['id']): string => TelegramBotAPI.url(telegramBotId) + 'users/';

	export const get = (telegramBotId: TelegramBot['id']) => makeRequest<TelegramBotUser[]>(url(telegramBotId), 'GET', headersWithAuthToken());
}

export namespace TelegramBotUserAPI {
	export const url = (
		telegramBotId: TelegramBot['id'],
		telegramBotUserId: TelegramBotUser['id'],
	): string => `${TelegramBotUsersAPI.url(telegramBotId)}${telegramBotUserId}/`;

	export const delete_ = (
		telegramBotId: TelegramBot['id'],
		telegramBotUserId: TelegramBotUser['id'],
	) => makeRequest(url(telegramBotId, telegramBotUserId), 'DELETE', headersWithAuthToken());
}

export namespace TelegramBotAllowedUserAPI {
	export const url = (
		telegramBotId: TelegramBot['id'],
		telegramBotUserId: TelegramBotUser['id'],
	): string => `${TelegramBotUserAPI.url(telegramBotId, telegramBotUserId)}allowed-user/`;

	export const set = (
		telegramBotId: TelegramBot['id'],
		telegramBotUserId: TelegramBotUser['id'],
	) => makeRequest(url(telegramBotId, telegramBotUserId), 'POST', headersWithAuthToken());
	export const unset = (
		telegramBotId: TelegramBot['id'],
		telegramBotUserId: TelegramBotUser['id'],
	) => makeRequest(url(telegramBotId, telegramBotUserId), 'DELETE', headersWithAuthToken());
}