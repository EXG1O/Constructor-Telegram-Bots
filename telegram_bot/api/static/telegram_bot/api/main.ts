import { ApiResponse as BaseApiResponse, makeRequest } from 'global_modules/api';
import { TelegramBot, TelegramBotCommandKeyboardButton, TelegramBotCommand, TelegramBotUser, TelegramBotDatabaseRecord, Data, ApiResponse } from './types';

declare const userApiToken: string;

namespace Base {
	export const url = '/api/telegram-bots/';
	export const headers: HeadersInit = {'Authorization': `Token ${userApiToken}`}
}

export namespace TelegramBotsApi {
	export const url = Base.url;

	export function get(): Promise<BaseApiResponse.Default<TelegramBot[]>> {
		return makeRequest<TelegramBot[]>(url, 'GET', Base.headers);
	}
}

export namespace TelegramBotApi {
	export const url = (telegramBotId: TelegramBot['id']): string => `${TelegramBotsApi.url}${telegramBotId}/`;

	export function get(telegramBotId: TelegramBot['id']): Promise<BaseApiResponse.Default<TelegramBot>> {
		return makeRequest<TelegramBot>(url(telegramBotId), 'GET', Base.headers);
	}
	export function create(data: Data.TelegramBot.Create): Promise<BaseApiResponse.Default<ApiResponse.TelegramBot.Create>> {
		return makeRequest<ApiResponse.TelegramBot.Create>(TelegramBotsApi.url, 'POST', Base.headers, data);
	}
	export function update(
		telegramBotId: TelegramBot['id'],
		data: Data.TelegramBot.Update,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId), 'PATCH', Base.headers, data);
	}
	export function delete_(telegramBotId: TelegramBot['id']): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId), 'DELETE', Base.headers);
	}

	export function start(telegramBotId: TelegramBot['id']): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegramBotId)}start-or-stop/`, 'POST', Base.headers);
	}
	export const stop = start;

	export function updateDiagramCurrentScale(
		telegramBotId: TelegramBot['id'],
		data: Data.TelegramBot.UpdateDiagramCurrentScale,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegramBotId)}update-diagram-current-scale/`, 'PATCH', Base.headers, data);
	}
}

export namespace TelegramBotCommandsApi {
	export const url = (telegramBotId: TelegramBot['id']): string => `${TelegramBotApi.url(telegramBotId)}commands/`;

	export function get(telegramBotId: TelegramBot['id']): Promise<BaseApiResponse.Default<TelegramBotCommand[]>>  {
		return makeRequest<TelegramBotCommand[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace TelegramBotCommandApi {
	export const url = (
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
	): string => `${TelegramBotCommandsApi.url(telegramBotId)}${telegramBotCommandId}/`;

	export function get(
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
	): Promise<BaseApiResponse.Default<TelegramBotCommand>> {
		return makeRequest<TelegramBotCommand>(url(telegramBotId, telegramBotCommandId), 'GET', Base.headers);
	}
	export function create(
		telegramBotId: TelegramBot['id'],
		data: Data.TelegramBotCommand.Create,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest<BaseApiResponse.Success>(TelegramBotCommandsApi.url(telegramBotId), 'POST', Base.headers, formData);
	}
	export function update(
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
		data: Data.TelegramBotCommand.Update,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId), 'PATCH', Base.headers, formData);
	}
	export function delete_(
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId), 'DELETE', Base.headers);
	}

	export function updatePosition(
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
		data: Data.TelegramBotCommand.UpdatePosition,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegramBotId, telegramBotCommandId)}update-position/`, 'PATCH', Base.headers, data);
	}
}

export namespace TelegramBotCommandKeyboardButtonApi {
	export const url = (
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
		telegramBotCommandKeyboardButtonId: TelegramBotCommandKeyboardButton['id'],
	): string => `${TelegramBotCommandApi.url(telegramBotId, telegramBotCommandId)}keyboard-buttons/${telegramBotCommandKeyboardButtonId}/telegram-bot-command/`;

	export function connect(
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
		telegramBotCommandKeyboardButtonId: TelegramBotCommandKeyboardButton['id'],
		data: Data.TelegramBotCommandKeyboardButton.Connect,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId, telegramBotCommandKeyboardButtonId), 'POST', Base.headers, data);
	}
	export function disconnect(
		telegramBotId: TelegramBot['id'],
		telegramBotCommandId: TelegramBotCommand['id'],
		telegramBotCommandKeyboardButtonId: TelegramBotCommandKeyboardButton['id'],
		data: Data.TelegramBotCommandKeyboardButton.Disconnect,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId, telegramBotCommandKeyboardButtonId), 'DELETE', Base.headers, data);
	}
}

export namespace TelegramBotUsersApi {
	export const url = (telegramBotId: TelegramBot['id']): string => `${TelegramBotApi.url(telegramBotId)}users/`;

	export function get(telegramBotId: TelegramBot['id']): Promise<BaseApiResponse.Default<TelegramBotUser[]>> {
		return makeRequest<TelegramBotUser[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace TelegramBotUserApi {
	export const url = (
		telegramBotId: TelegramBot['id'],
		telegramBotUserId: TelegramBotUser['id'],
	): string => `${TelegramBotUsersApi.url(telegramBotId)}${telegramBotUserId}/`;

	export function delete_(
		telegramBotId: TelegramBot['id'],
		telegramBotUserId: TelegramBotUser['id'],
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotUserId), 'DELETE', Base.headers);
	}
}

export namespace TelegramBotAllowedUserApi {
	export const url = (
		telegramBotId: TelegramBot['id'],
		telegramBotUserId: TelegramBotUser['id'],
	): string => `${TelegramBotUserApi.url(telegramBotId, telegramBotUserId)}allowed-user/`;

	export function set(
		telegramBotId: TelegramBot['id'],
		telegramBotUserId: TelegramBotUser['id'],
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotUserId), 'POST', Base.headers);
	}
	export function unset(
		telegramBotId: TelegramBot['id'],
		telegramBotUserId: TelegramBotUser['id'],
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotUserId), 'DELETE', Base.headers);
	}
}

export namespace TelegramBotDatabaseRecordsApi {
	export const url = (telegramBotId: TelegramBot['id']): string => `${TelegramBotApi.url(telegramBotId)}database/records/`;

	export function get(telegramBotId: TelegramBot['id']): Promise<BaseApiResponse.Default<TelegramBotDatabaseRecord[]>> {
		return makeRequest<TelegramBotDatabaseRecord[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace TelegramBotDatabaseRecordApi {
	export const url = (
		telegramBotId: TelegramBot['id'],
		telegramBotDatabaseRecordId: TelegramBotDatabaseRecord['_id'],
	): string => `${TelegramBotDatabaseRecordsApi.url(telegramBotId)}${telegramBotDatabaseRecordId}/`;

	export function create(
		telegramBotId: TelegramBot['id'],
		data: Data.TelegramBotDatabaseRecord.Create,
	): Promise<BaseApiResponse.Default<ApiResponse.TelegramBotDatabaseRecord.Create>> {
		return makeRequest<ApiResponse.TelegramBotDatabaseRecord.Create>(TelegramBotDatabaseRecordsApi.url(telegramBotId), 'POST', Base.headers, data);
	}
	export function update(
		telegramBotId: TelegramBot['id'],
		telegramBotDatabaseRecordId: TelegramBotDatabaseRecord['_id'],
		data: Data.TelegramBotDatabaseRecord.Update,
	): Promise<BaseApiResponse.Default<ApiResponse.TelegramBotDatabaseRecord.Update>> {
		return makeRequest<ApiResponse.TelegramBotDatabaseRecord.Update>(url(telegramBotId, telegramBotDatabaseRecordId), 'PATCH', Base.headers, data);
	}
	export function delete_(
		telegramBotId: TelegramBot['id'],
		telegramBotDatabaseRecordId: TelegramBotDatabaseRecord['_id'],
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotDatabaseRecordId), 'DELETE', Base.headers);
	}
}