import { ApiResponse as BaseApiResponse, makeRequest } from 'global_modules/api';
import { TelegramBot } from 'telegram_bot_api/types';
import { Plugin, PluginLog, ApiResponse, Data } from './types';

declare const userApiToken: string;

namespace Base {
	export const url = '/plugins/';
	export const headers: HeadersInit = {'Authorization': `Token ${userApiToken}`}
}

export namespace PluginsApi {
	export const url = (telegramBotId: TelegramBot['id']): string => `${Base.url}_/${telegramBotId}/`;

	export function get(telegramBotId: TelegramBot['id']): Promise<BaseApiResponse.Default<Plugin[]>> {
		return makeRequest<Plugin[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace PluginApi {
	export const url = (pluginId: Plugin['id']): string => `${Base.url}${pluginId}/`;

	export function create(telegramBotId: TelegramBot['id'], data: Data.Plugin.Create): Promise<BaseApiResponse.Default<ApiResponse.Plugin.Create>> {
		return makeRequest<ApiResponse.Plugin.Create>(PluginsApi.url(telegramBotId), 'POST', Base.headers, data);
	}
	export function update(pluginId: Plugin['id'], data: Data.Plugin.Update): Promise<BaseApiResponse.Default<ApiResponse.Plugin.Update>> {
		return makeRequest<ApiResponse.Plugin.Update>(url(pluginId), 'PATCH', Base.headers, data);
	}
	export function delete_(pluginId: Plugin['id']): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(pluginId), 'DELETE', Base.headers);
	}
}

export namespace PluginsLogsApi {
	export const url = (telegramBotId: TelegramBot['id']): string => `${PluginsApi.url(telegramBotId)}logs/`;

	export function get(telegramBotId: TelegramBot['id']): Promise<BaseApiResponse.Default<PluginLog[]>> {
		return makeRequest<PluginLog[]>(url(telegramBotId), 'GET', Base.headers);
	}
}