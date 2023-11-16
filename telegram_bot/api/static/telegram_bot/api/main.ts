import {ObjectAsJson, ApiResponse as BaseApiResponse, makeRequest} from 'global_modules/api';
import {TelegramBot, TelegramBotCommand, TelegramBotUser, TelegramBotDatabeseRecord, Data, ApiResponse} from './types';

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
	export const url = (telegram_bot_id: number): string => `${TelegramBotsApi.url}${telegram_bot_id}/`;

	export function get(telegram_bot_id: number): Promise<BaseApiResponse.Default<TelegramBot>> {
		return makeRequest<TelegramBot>(url(telegram_bot_id), 'GET', Base.headers);
	}
	export function create(data: Data.TelegramBot.Create): Promise<BaseApiResponse.Default<ApiResponse.TelegramBot.Create>> {
		return makeRequest<ApiResponse.TelegramBot.Create>(TelegramBotsApi.url, 'POST', Base.headers, data);
	}
	export function update(
		telegram_bot_id: number,
		data: Data.TelegramBot.Update,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegram_bot_id), 'PATCH', Base.headers, data);
	}
	export function delete_(telegram_bot_id: number): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegram_bot_id), 'DELETE', Base.headers);
	}

	export function start(telegram_bot_id: number): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegram_bot_id)}start-or-stop/`, 'POST', Base.headers);
	}
	export const stop = start;

	export function updateDiagramCurrentScale(
		telegram_bot_id: number,
		data: Data.TelegramBot.UpdateDiagramCurrentScale,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegram_bot_id)}update-diagram-current-scale/`, 'PATCH', Base.headers, data);
	}
}

export namespace TelegramBotCommandsApi {
	export const url = (telegram_bot_id: number): string => `${TelegramBotApi.url(telegram_bot_id)}commands/`;

	export function get(telegram_bot_id: number): Promise<BaseApiResponse.Default<TelegramBotCommand[]>>  {
		return makeRequest<TelegramBotCommand[]>(url(telegram_bot_id), 'GET', Base.headers);
	}
}

export namespace TelegramBotCommandApi {
	export const url = (
		telegram_bot_id: number,
		telegram_bot_command_id: number,
	): string => `${TelegramBotCommandsApi.url(telegram_bot_id)}${telegram_bot_command_id}/`;

	export function get(
		telegram_bot_id: number,
		telegram_bot_command_id: number,
	): Promise<BaseApiResponse.Default<TelegramBotCommand>> {
		return makeRequest<TelegramBotCommand>(url(telegram_bot_id, telegram_bot_command_id), 'GET', Base.headers);
	}
	export function create(
		telegram_bot_id: number,
		data: Data.TelegramBotCommand.Create,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest<BaseApiResponse.Success>(TelegramBotCommandsApi.url(telegram_bot_id), 'POST', Base.headers, formData);
	}
	export function update(
		telegram_bot_id: number,
		telegram_bot_command_id: number,
		data: Data.TelegramBotCommand.Update,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		const formData = new FormData();
		formData.append('image', data.image);
		formData.append('data', JSON.stringify(data.data));

		return makeRequest<BaseApiResponse.Success>(url(telegram_bot_id, telegram_bot_command_id), 'PATCH', Base.headers, formData);
	}
	export function delete_(
		telegram_bot_id: number,
		telegram_bot_command_id: number,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegram_bot_id, telegram_bot_command_id), 'DELETE', Base.headers);
	}

	export function updatePosition(
		telegram_bot_id: number,
		telegram_bot_command_id: number,
		data: Data.TelegramBotCommand.UpdatePosition,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(`${url(telegram_bot_id, telegram_bot_command_id)}update-position/`, 'PATCH', Base.headers, data);
	}
}

export namespace TelegramBotCommandKeyboardButtonApi {
	export const url = (
		telegram_bot_id: number,
		telegram_bot_command_id: number,
		telegram_bot_command_keyboard_button_id: number,
	): string => `${TelegramBotCommandApi.url(telegram_bot_id, telegram_bot_command_id)}keyboard-buttons/${telegram_bot_command_keyboard_button_id}/telegram-bot-command/`;

	export function connect(
		telegram_bot_id: number,
		telegram_bot_command_id: number,
		telegram_bot_command_keyboard_button_id: number,
		data: Data.TelegramBotCommandKeyboardButton.Connect,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegram_bot_id, telegram_bot_command_id, telegram_bot_command_keyboard_button_id), 'POST', Base.headers, data);
	}
	export function disconnect(
		telegram_bot_id: number,
		telegram_bot_command_id: number,
		telegram_bot_command_keyboard_button_id: number,
		data: Data.TelegramBotCommandKeyboardButton.Disconnect,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegram_bot_id, telegram_bot_command_id, telegram_bot_command_keyboard_button_id), 'DELETE', Base.headers, data);
	}
}

export namespace TelegramBotUsersApi {
	export const url = (telegram_bot_id: number): string => `${TelegramBotApi.url(telegram_bot_id)}users/`;

	export function get(telegram_bot_id: number): Promise<BaseApiResponse.Default<TelegramBotUser[]>> {
		return makeRequest<TelegramBotUser[]>(url(telegram_bot_id), 'GET', Base.headers);
	}
}

export namespace TelegramBotUserApi {
	export const url = (
		telegram_bot_id: number,
		telegram_bot_user_id: number,
	): string => `${TelegramBotUsersApi.url(telegram_bot_id)}${telegram_bot_user_id}/`;

	export function delete_(
		telegram_bot_id: number,
		telegram_bot_user_id: number,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegram_bot_id, telegram_bot_user_id), 'DELETE', Base.headers);
	}
}

export namespace TelegramBotAllowedUserApi {
	export const url = (
		telegram_bot_id: number,
		telegram_bot_user_id: number,
	): string => `${TelegramBotUserApi.url(telegram_bot_id, telegram_bot_user_id)}allowed-user/`;

	export function set(
		telegram_bot_id: number,
		telegram_bot_user_id: number,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegram_bot_id, telegram_bot_user_id), 'POST', Base.headers);
	}
	export function unset(
		telegram_bot_id: number,
		telegram_bot_user_id: number,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegram_bot_id, telegram_bot_user_id), 'DELETE', Base.headers);
	}
}

export namespace TelegramBotDatabeseRecordsApi {
	export const url = (telegram_bot_id: number): string => `${TelegramBotApi.url(telegram_bot_id)}database/records/`;

	export function get(telegram_bot_id: number): Promise<BaseApiResponse.Default<TelegramBotDatabeseRecord[]>> {
		return makeRequest<TelegramBotDatabeseRecord[]>(url(telegram_bot_id), 'GET', Base.headers);
	}
}

export namespace TelegramBotDatabeseRecordApi {
	export const url = (
		telegram_bot_id: number,
		telegram_bot_databese_record_id: number,
	): string => `${TelegramBotDatabeseRecordsApi.url(telegram_bot_id)}${telegram_bot_databese_record_id}/`;

	export function create(
		telegram_bot_id: number,
		data: ObjectAsJson,
	): Promise<BaseApiResponse.Default<ApiResponse.TelegramBotDatabeseRecord.Create>> {
		return makeRequest<ApiResponse.TelegramBotDatabeseRecord.Create>(TelegramBotDatabeseRecordsApi.url(telegram_bot_id), 'POST', Base.headers, data);
	}
	export function update(
		telegram_bot_id: number,
		telegram_bot_databese_record_id: number,
		data: ObjectAsJson,
	): Promise<BaseApiResponse.Default<ApiResponse.TelegramBotDatabeseRecord.Update>> {
		return makeRequest<ApiResponse.TelegramBotDatabeseRecord.Update>(url(telegram_bot_id, telegram_bot_databese_record_id), 'PATCH', Base.headers, data);
	}
	export function delete_(
		telegram_bot_id: number,
		telegram_bot_databese_record_id: number,
	): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(telegram_bot_id, telegram_bot_databese_record_id), 'DELETE', Base.headers);
	}
}