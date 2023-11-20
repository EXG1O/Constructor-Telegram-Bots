import { ObjectAsJson, ApiResponse as BaseApiResponse, makeRequest } from 'global_modules/api';
import { TelegramBot, TelegramBotCommand, TelegramBotUser, TelegramBotDatabeseRecord, Data, ApiResponse } from './types';

declare const userApiToken: string;

namespace Base {
	export const url = '/api/telegram-bots/';
	export const headers: HeadersInit = {
		Authorization: `Token ${userApiToken}`,
	}
}

export namespace TelegramBotsApi {
	export const url = Base.url;

	export function get(): Promise<BaseApiResponse.Default<TelegramBot[]>> {
		return makeRequest<TelegramBot[]>(url, 'GET', Base.headers);
	}
}

export namespace TelegramBotApi {
	export const url = (telegramBotId: number): string => `${TelegramBotsApi.url}${telegramBotId}/`;

	export function get(telegramBotId: number): Promise<BaseApiResponse.Default<TelegramBot>> {
		return makeRequest<TelegramBot>(url(telegramBotId), 'GET', Base.headers);
	}
	export function create(data: Data.TelegramBot.Create): Promise<BaseApiResponse.Default<ApiResponse.TelegramBot.Create>> {
		return makeRequest<ApiResponse.TelegramBot.Create>(TelegramBotsApi.url, 'POST', Base.headers, data);
	}
	export function update(
		telegramBotId: number,
		data: Data.TelegramBot.Update,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId), 'PATCH', Base.headers, data);
	}
	export function delete_(telegramBotId: number): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId), 'DELETE', Base.headers);
	}

	export function start(telegramBotId: number): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegramBotId)}start-or-stop/`, 'POST', Base.headers);
	}
	export const stop = start;

	export function updateDiagramCurrentScale(
		telegramBotId: number,
		data: Data.TelegramBot.UpdateDiagramCurrentScale,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegramBotId)}update-diagram-current-scale/`, 'PATCH', Base.headers, data);
	}
}

export namespace TelegramBotCommandsApi {
	export const url = (telegramBotId: number): string => `${TelegramBotApi.url(telegramBotId)}commands/`;

	export function get(telegramBotId: number): Promise<BaseApiResponse.Default<TelegramBotCommand[]>>  {
		return makeRequest<TelegramBotCommand[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace TelegramBotCommandApi {
	export const url = (
		telegramBotId: number,
		telegramBotCommandId: number,
	): string => `${TelegramBotCommandsApi.url(telegramBotId)}${telegramBotCommandId}/`;

	export function get(
		telegramBotId: number,
		telegramBotCommandId: number,
	): Promise<BaseApiResponse.Default<TelegramBotCommand>> {
		return makeRequest<TelegramBotCommand>(url(telegramBotId, telegramBotCommandId), 'GET', Base.headers);
	}
	export function create(
		telegramBotId: number,
		data: Data.TelegramBotCommand.Create,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest<BaseApiResponse.Success>(TelegramBotCommandsApi.url(telegramBotId), 'POST', Base.headers, formData);
	}
	export function update(
		telegramBotId: number,
		telegramBotCommandId: number,
		data: Data.TelegramBotCommand.Update,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId), 'PATCH', Base.headers, formData);
	}
	export function delete_(
		telegramBotId: number,
		telegramBotCommandId: number,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId), 'DELETE', Base.headers);
	}

	export function updatePosition(
		telegramBotId: number,
		telegramBotCommandId: number,
		data: Data.TelegramBotCommand.UpdatePosition,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegramBotId, telegramBotCommandId)}update-position/`, 'PATCH', Base.headers, data);
	}
}

export namespace TelegramBotCommandKeyboardButtonApi {
	export const url = (
		telegramBotId: number,
		telegramBotCommandId: number,
		telegramBotCommandKeyboardButtonId: number,
	): string => `${TelegramBotCommandApi.url(telegramBotId, telegramBotCommandId)}keyboard-buttons/${telegramBotCommandKeyboardButtonId}/telegram-bot-command/`;

	export function connect(
		telegramBotId: number,
		telegramBotCommandId: number,
		telegramBotCommandKeyboardButtonId: number,
		data: Data.TelegramBotCommandKeyboardButton.Connect,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId, telegramBotCommandKeyboardButtonId), 'POST', Base.headers, data);
	}
	export function disconnect(
		telegramBotId: number,
		telegramBotCommandId: number,
		telegramBotCommandKeyboardButtonId: number,
		data: Data.TelegramBotCommandKeyboardButton.Disconnect,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotCommandId, telegramBotCommandKeyboardButtonId), 'DELETE', Base.headers, data);
	}
}

export namespace TelegramBotUsersApi {
	export const url = (telegramBotId: number): string => `${TelegramBotApi.url(telegramBotId)}users/`;

	export function get(telegramBotId: number): Promise<BaseApiResponse.Default<TelegramBotUser[]>> {
		return makeRequest<TelegramBotUser[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace TelegramBotUserApi {
	export const url = (
		telegramBotId: number,
		telegramBotUserId: number,
	): string => `${TelegramBotUsersApi.url(telegramBotId)}${telegramBotUserId}/`;

	export function delete_(
		telegramBotId: number,
		telegramBotUserId: number,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotUserId), 'DELETE', Base.headers);
	}
}

export namespace TelegramBotAllowedUserApi {
	export const url = (
		telegramBotId: number,
		telegramBotUserId: number,
	): string => `${TelegramBotUserApi.url(telegramBotId, telegramBotUserId)}allowed-user/`;

	export function set(
		telegramBotId: number,
		telegramBotUserId: number,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotUserId), 'POST', Base.headers);
	}
	export function unset(
		telegramBotId: number,
		telegramBotUserId: number,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotUserId), 'DELETE', Base.headers);
	}
}

export namespace TelegramBotDatabeseRecordsApi {
	export const url = (telegramBotId: number): string => `${TelegramBotApi.url(telegramBotId)}database/records/`;

	export function get(telegramBotId: number): Promise<BaseApiResponse.Default<TelegramBotDatabeseRecord[]>> {
		return makeRequest<TelegramBotDatabeseRecord[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace TelegramBotDatabeseRecordApi {
	export const url = (
		telegramBotId: number,
		telegramBotDatabeseRecordId: number,
	): string => `${TelegramBotDatabeseRecordsApi.url(telegramBotId)}${telegramBotDatabeseRecordId}/`;

	export function create(
		telegramBotId: number,
		data: ObjectAsJson,
	): Promise<BaseApiResponse.Default<ApiResponse.TelegramBotDatabeseRecord.Create>> {
		return makeRequest<ApiResponse.TelegramBotDatabeseRecord.Create>(TelegramBotDatabeseRecordsApi.url(telegramBotId), 'POST', Base.headers, data);
	}
	export function update(
		telegramBotId: number,
		telegramBotDatabeseRecordId: number,
		data: ObjectAsJson,
	): Promise<BaseApiResponse.Default<ApiResponse.TelegramBotDatabeseRecord.Update>> {
		return makeRequest<ApiResponse.TelegramBotDatabeseRecord.Update>(url(telegramBotId, telegramBotDatabeseRecordId), 'PATCH', Base.headers, data);
	}
	export function delete_(
		telegramBotId: number,
		telegramBotDatabeseRecordId: number,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegramBotId, telegramBotDatabeseRecordId), 'DELETE', Base.headers);
	}
}