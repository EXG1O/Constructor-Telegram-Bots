import { headersWithAuthToken, makeRequest } from 'services/api/base';
import { TelegramBot, TelegramBotCommand, TelegramBotCommandKeyboardButton, TelegramBotCommandDiagram, TelegramBotUser, Data, APIResponse } from './types';

const rootURL = '/api/telegram-bots/';

export namespace TelegramBotsAPI {
	export const get = () => makeRequest<TelegramBot[]>(rootURL, 'GET', headersWithAuthToken());
}

export namespace TelegramBotAPI {
	export const url = (telegramBotID: TelegramBot['id']) => rootURL + `${telegramBotID}/`;

	export const get = (telegramBotID: TelegramBot['id']) => makeRequest<TelegramBot>(url(telegramBotID), 'GET', headersWithAuthToken());
	export const create = (data: Data.TelegramBotAPI.Create) => makeRequest<APIResponse.TelegramBotAPI.Create>(rootURL, 'POST', headersWithAuthToken(), data);
	export const update = (telegramBotID: TelegramBot['id'], data: Data.TelegramBotAPI.Update) => makeRequest<APIResponse.TelegramBotAPI.Update>(url(telegramBotID), 'PATCH', headersWithAuthToken(), data);
	export const delete_ = (telegramBotID: TelegramBot['id']) => makeRequest(url(telegramBotID), 'DELETE', headersWithAuthToken());

	export const start = (telegramBotID: TelegramBot['id']) => makeRequest(url(telegramBotID) +'start-or-stop/', 'POST', headersWithAuthToken());
	export const stop = start;
}

export namespace TelegramBotCommandsAPI {
	export const url = (telegramBotID: TelegramBot['id']) => TelegramBotAPI.url(telegramBotID) + 'commands/';

	export const get = (telegramBotID: TelegramBot['id']) => makeRequest<TelegramBotCommand[]>(url(telegramBotID), 'GET', headersWithAuthToken());
}

export namespace TelegramBotCommandAPI {
	export const url = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
	) => TelegramBotCommandsAPI.url(telegramBotID) + `${telegramBotCommandID}/`;

	export const get = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
	) => makeRequest<TelegramBotCommand>(url(telegramBotID, telegramBotCommandID), 'GET', headersWithAuthToken());
	export function create(telegramBotID: TelegramBot['id'], data: Data.TelegramBotCommandAPI.Create) {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest(TelegramBotCommandsAPI.url(telegramBotID), 'POST', headersWithAuthToken(), formData);
	}
	export function update(
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
		data: Data.TelegramBotCommandAPI.Update,
	) {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest(TelegramBotCommandAPI.url(telegramBotID, telegramBotCommandID), 'PATCH', headersWithAuthToken(), formData);
	}
	export const delete_ = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
	) => makeRequest(url(telegramBotID, telegramBotCommandID), 'DELETE', headersWithAuthToken());
}

export namespace TelegramBotCommandsDiagramAPI {
	export const url = (telegramBotID: TelegramBot['id']) => TelegramBotAPI.url(telegramBotID) + 'diagram/commands/';

	export const get = (telegramBotID: TelegramBot['id']) => makeRequest<TelegramBotCommandDiagram[]>(url(telegramBotID), 'GET', headersWithAuthToken());
}

export namespace TelegramBotCommandDiagramAPI {
	export const url = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
	) => TelegramBotCommandsDiagramAPI.url(telegramBotID) + telegramBotCommandID + '/';

	export const connect = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
		data: Data.TelegramBotCommandDiagramAPI.Connect,
	) => makeRequest(url(telegramBotID, telegramBotCommandID), 'POST', headersWithAuthToken(), data);
	export const disconnect = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
		data: Data.TelegramBotCommandDiagramAPI.Disconnect,
	) => makeRequest(url(telegramBotID, telegramBotCommandID), 'DELETE', headersWithAuthToken(), data);

	export const updatePosition = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
		data: Data.TelegramBotCommandDiagramAPI.UpdatePosition,
	) => makeRequest(url(telegramBotID, telegramBotCommandID), 'PATCH', headersWithAuthToken(), data);
}

export namespace TelegramBotUsersAPI {
	export const url = (telegramBotID: TelegramBot['id']) => TelegramBotAPI.url(telegramBotID) + 'users/';

	export const get = (telegramBotID: TelegramBot['id']) => makeRequest<TelegramBotUser[]>(url(telegramBotID), 'GET', headersWithAuthToken());
}

export namespace TelegramBotUserAPI {
	export const url = (
		telegramBotID: TelegramBot['id'],
		telegramBotUserID: TelegramBotUser['id'],
	) => `${TelegramBotUsersAPI.url(telegramBotID)}${telegramBotUserID}/`;

	export const get = (
		telegramBotID: TelegramBot['id'],
		telegramBotUserID: TelegramBotUser['id'],
	) => makeRequest<TelegramBotUser>(url(telegramBotID, telegramBotUserID), 'GET', headersWithAuthToken());
	export const delete_ = (
		telegramBotID: TelegramBot['id'],
		telegramBotUserID: TelegramBotUser['id'],
	) => makeRequest(url(telegramBotID, telegramBotUserID), 'DELETE', headersWithAuthToken());
}

export namespace TelegramBotAllowedUserAPI {
	export const url = (
		telegramBotID: TelegramBot['id'],
		telegramBotUserID: TelegramBotUser['id'],
	) => `${TelegramBotUserAPI.url(telegramBotID, telegramBotUserID)}allowed-user/`;

	export const set = (
		telegramBotID: TelegramBot['id'],
		telegramBotUserID: TelegramBotUser['id'],
	) => makeRequest(url(telegramBotID, telegramBotUserID), 'POST', headersWithAuthToken());
	export const unset = (
		telegramBotID: TelegramBot['id'],
		telegramBotUserID: TelegramBotUser['id'],
	) => makeRequest(url(telegramBotID, telegramBotUserID), 'DELETE', headersWithAuthToken());
}