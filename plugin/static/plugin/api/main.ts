import { ApiResponse as BaseApiResponse, makeRequest } from 'global_modules/api';
import { Plugin, PluginLog, ApiResponse, Data } from './types';

declare const userApiToken: string;

namespace Base {
	export const url = '/plugins/';
	export const headers: HeadersInit = {
		'Authorization': `Token ${userApiToken}`,
	}
}

export namespace PluginsApi {
	export const url = (telegramBotId: number): string => `${Base.url}_/${telegramBotId}/`;

	export function get(telegramBotId: number): Promise<BaseApiResponse.Default<Plugin[]>> {
		return makeRequest<Plugin[]>(url(telegramBotId), 'GET', Base.headers);
	}
}

export namespace PluginApi {
	export const url = (pluginId: number): string => `${Base.url}${pluginId}/`;

	export function create(telegramBotId: number, data: Data.Plugin.Create): Promise<BaseApiResponse.Default<ApiResponse.Plugin.Create>> {
		return makeRequest<ApiResponse.Plugin.Create>(PluginsApi.url(telegramBotId), 'POST', Base.headers, data);
	}
	export function update(pluginId: number, data: Data.Plugin.Update): Promise<BaseApiResponse.Default<ApiResponse.Plugin.Update>> {
		return makeRequest<ApiResponse.Plugin.Update>(url(pluginId), 'PATCH', Base.headers, data);
	}
	export function delete_(pluginId: number): Promise<BaseApiResponse.Default<BaseApiResponse.Success>> {
		return makeRequest<BaseApiResponse.Success>(url(pluginId), 'DELETE', Base.headers);
	}
}

export namespace PluginsLogsApi {
	export const url = (telegramBotId: number): string => `${PluginsApi.url(telegramBotId)}logs/`;

	export function get(telegramBotId: number): Promise<BaseApiResponse.Default<PluginLog[]>> {
		return makeRequest<PluginLog[]>(url(telegramBotId), 'GET', Base.headers);
	}
}