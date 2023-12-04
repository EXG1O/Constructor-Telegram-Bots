import { ApiResponse as BaseApiResponse, makeRequest } from 'global_modules/api';
import { TelegramBot as TelegramBotType } from 'telegram_bot_api/types';
import * as Types from './types';

declare const userApiToken: string;

namespace Base {
	export const url = '/plugins/';
	export const headers: HeadersInit = {'Authorization': `Token ${userApiToken}`}
}

export namespace PluginsApi {
	export const url = (telegramBotId: TelegramBotType['id']): string => `${Base.url}_/${telegramBotId}/`;

	export function get(telegramBotId: TelegramBotType['id']): Promise<BaseApiResponse.Default<Types.Plugin[]>> {
		return makeRequest<Types.Plugin[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace PluginApi {
	export const url = (pluginId: Types.Plugin['id']): string => `${Base.url}${pluginId}/`;

	export function create(telegramBotId: TelegramBotType['id'], data: Types.Data.Plugin.Create): Promise<BaseApiResponse.Default<Types.ApiResponse.Plugin.Create>> {
		return makeRequest<Types.ApiResponse.Plugin.Create>(PluginsApi.url(telegramBotId), 'POST', Base.headers, data);
	}
	export function update(pluginId: Types.Plugin['id'], data: Types.Data.Plugin.Update): Promise<BaseApiResponse.Default<Types.ApiResponse.Plugin.Update>> {
		return makeRequest<Types.ApiResponse.Plugin.Update>(url(pluginId), 'PATCH', Base.headers, data);
	}
	export function delete_(pluginId: Types.Plugin['id']): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(pluginId), 'DELETE', Base.headers);
	}
}

export namespace PluginsLogsApi {
	export const url = (telegramBotId: TelegramBotType['id']): string => `${PluginsApi.url(telegramBotId)}logs/`;

	export function get(telegramBotId: TelegramBotType['id']): Promise<BaseApiResponse.Default<Types.PluginLog[]>> {
		return makeRequest<Types.PluginLog[]>(url(telegramBotId), 'GET', Base.headers);
	}
}