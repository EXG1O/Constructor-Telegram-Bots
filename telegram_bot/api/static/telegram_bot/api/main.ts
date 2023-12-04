import { ApiResponse as BaseApiResponse, makeRequest } from 'global_modules/api';
import * as Types from './types';

declare const userApiToken: string;

namespace Base {
	export const url = '/api/telegram-bots/';
	export const headers: HeadersInit = {'Authorization': `Token ${userApiToken}`}
}

export namespace TelegramBotsApi {
	export const url = Base.url;

	export function get(): Promise<BaseApiResponse.Default<Types.TelegramBot[]>> {
		return makeRequest<Types.TelegramBot[]>(url, 'GET', Base.headers);
	}
}

export namespace TelegramBotApi {
	export const url = (telegramBotId: Types.TelegramBot['id']): string => `${TelegramBotsApi.url}${telegramBotId}/`;

	export function get(telegramBotId: Types.TelegramBot['id']): Promise<BaseApiResponse.Default<Types.TelegramBot>> {
		return makeRequest<Types.TelegramBot>(url(telegramBotId), 'GET', Base.headers);
	}
	export function create(data: Types.Data.TelegramBot.Create): Promise<BaseApiResponse.Default<Types.ApiResponse.TelegramBot.Create>> {
		return makeRequest<Types.ApiResponse.TelegramBot.Create>(TelegramBotsApi.url, 'POST', Base.headers, data);
	}
	export function update(
		telegramBotId: Types.TelegramBot['id'],
		data: Types.Data.TelegramBot.Update,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId), 'PATCH', Base.headers, data);
	}
	export function delete_(telegramBotId: Types.TelegramBot['id']): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId), 'DELETE', Base.headers);
	}

	export function start(telegramBotId: Types.TelegramBot['id']): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegramBotId)}start-or-stop/`, 'POST', Base.headers);
	}
	export const stop = start;

	export function updateDiagramCurrentScale(
		telegramBotId: Types.TelegramBot['id'],
		data: Types.Data.TelegramBot.UpdateDiagramCurrentScale,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegramBotId)}update-diagram-current-scale/`, 'PATCH', Base.headers, data);
	}
}

export namespace TelegramBotCommandsApi {
	export const url = (telegramBotId: Types.TelegramBot['id']): string => `${TelegramBotApi.url(telegramBotId)}commands/`;

	export function get(telegramBotId: Types.TelegramBot['id']): Promise<BaseApiResponse.Default<Types.TelegramBotCommand[]>>  {
		return makeRequest<Types.TelegramBotCommand[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace TelegramBotCommandApi {
	export const url = (
		telegramBotId: Types.TelegramBot['id'],
		telegramBotCommandId: Types.TelegramBotCommand['id'],
	): string => `${TelegramBotCommandsApi.url(telegramBotId)}${telegramBotCommandId}/`;

	export function get(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotCommandId: Types.TelegramBotCommand['id'],
	): Promise<BaseApiResponse.Default<Types.TelegramBotCommand>> {
		return makeRequest<Types.TelegramBotCommand>(url(telegramBotId, telegramBotCommandId), 'GET', Base.headers);
	}
	export function create(
		telegramBotId: Types.TelegramBot['id'],
		data: Types.Data.TelegramBotCommand.Create,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest<BaseApiResponse.Success>(TelegramBotCommandsApi.url(telegramBotId), 'POST', Base.headers, formData);
	}
	export function update(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotCommandId: Types.TelegramBotCommand['id'],
		data: Types.Data.TelegramBotCommand.Update,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId), 'PATCH', Base.headers, formData);
	}
	export function delete_(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotCommandId: Types.TelegramBotCommand['id'],
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId), 'DELETE', Base.headers);
	}

	export function updatePosition(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotCommandId: Types.TelegramBotCommand['id'],
		data: Types.Data.TelegramBotCommand.UpdatePosition,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegramBotId, telegramBotCommandId)}update-position/`, 'PATCH', Base.headers, data);
	}
}

export namespace TelegramBotCommandKeyboardButtonApi {
	export const url = (
		telegramBotId: Types.TelegramBot['id'],
		telegramBotCommandId: Types.TelegramBotCommand['id'],
		telegramBotCommandKeyboardButtonId: Types.TelegramBotCommandKeyboardButton['id'],
	): string => `${TelegramBotCommandApi.url(telegramBotId, telegramBotCommandId)}keyboard-buttons/${telegramBotCommandKeyboardButtonId}/telegram-bot-command/`;

	export function connect(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotCommandId: Types.TelegramBotCommand['id'],
		telegramBotCommandKeyboardButtonId: Types.TelegramBotCommandKeyboardButton['id'],
		data: Types.Data.TelegramBotCommandKeyboardButton.Connect,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId, telegramBotCommandKeyboardButtonId), 'POST', Base.headers, data);
	}
	export function disconnect(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotCommandId: Types.TelegramBotCommand['id'],
		telegramBotCommandKeyboardButtonId: Types.TelegramBotCommandKeyboardButton['id'],
		data: Types.Data.TelegramBotCommandKeyboardButton.Disconnect,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId, telegramBotCommandKeyboardButtonId), 'DELETE', Base.headers, data);
	}
}

export namespace TelegramBotUsersApi {
	export const url = (telegramBotId: Types.TelegramBot['id']): string => `${TelegramBotApi.url(telegramBotId)}users/`;

	export function get(telegramBotId: Types.TelegramBot['id']): Promise<BaseApiResponse.Default<Types.TelegramBotUser[]>> {
		return makeRequest<Types.TelegramBotUser[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace TelegramBotUserApi {
	export const url = (
		telegramBotId: Types.TelegramBot['id'],
		telegramBotUserId: Types.TelegramBotUser['id'],
	): string => `${TelegramBotUsersApi.url(telegramBotId)}${telegramBotUserId}/`;

	export function delete_(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotUserId: Types.TelegramBotUser['id'],
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotUserId), 'DELETE', Base.headers);
	}
}

export namespace TelegramBotAllowedUserApi {
	export const url = (
		telegramBotId: Types.TelegramBot['id'],
		telegramBotUserId: Types.TelegramBotUser['id'],
	): string => `${TelegramBotUserApi.url(telegramBotId, telegramBotUserId)}allowed-user/`;

	export function set(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotUserId: Types.TelegramBotUser['id'],
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotUserId), 'POST', Base.headers);
	}
	export function unset(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotUserId: Types.TelegramBotUser['id'],
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotUserId), 'DELETE', Base.headers);
	}
}

export namespace TelegramBotDatabaseRecordsApi {
	export const url = (telegramBotId: Types.TelegramBot['id']): string => `${TelegramBotApi.url(telegramBotId)}database/records/`;

	export function get(telegramBotId: Types.TelegramBot['id']): Promise<BaseApiResponse.Default<Types.TelegramBotDatabaseRecord[]>> {
		return makeRequest<Types.TelegramBotDatabaseRecord[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace TelegramBotDatabaseRecordApi {
	export const url = (
		telegramBotId: Types.TelegramBot['id'],
		telegramBotDatabaseRecordId: Types.TelegramBotDatabaseRecord['_id'],
	): string => `${TelegramBotDatabaseRecordsApi.url(telegramBotId)}${telegramBotDatabaseRecordId}/`;

	export function create(
		telegramBotId: Types.TelegramBot['id'],
		data: Types.Data.TelegramBotDatabaseRecord.Create,
	): Promise<BaseApiResponse.Default<Types.ApiResponse.TelegramBotDatabaseRecord.Create>> {
		return makeRequest<Types.ApiResponse.TelegramBotDatabaseRecord.Create>(TelegramBotDatabaseRecordsApi.url(telegramBotId), 'POST', Base.headers, data);
	}
	export function update(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotDatabaseRecordId: Types.TelegramBotDatabaseRecord['_id'],
		data: Types.Data.TelegramBotDatabaseRecord.Update,
	): Promise<BaseApiResponse.Default<Types.ApiResponse.TelegramBotDatabaseRecord.Update>> {
		return makeRequest<Types.ApiResponse.TelegramBotDatabaseRecord.Update>(url(telegramBotId, telegramBotDatabaseRecordId), 'PATCH', Base.headers, data);
	}
	export function delete_(
		telegramBotId: Types.TelegramBot['id'],
		telegramBotDatabaseRecordId: Types.TelegramBotDatabaseRecord['_id'],
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotDatabaseRecordId), 'DELETE', Base.headers);
	}
}