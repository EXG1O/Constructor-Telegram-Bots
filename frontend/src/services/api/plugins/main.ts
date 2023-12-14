import { makeRequest } from 'services/api/base';
import { TelegramBot } from 'services/api/telegram_bots/types';
import { Plugin, PluginLog, Data, APIResponse } from './types';

const rootURL = '/plugins/';

export namespace PluginsAPI {
	export const url = (telegramBotId: TelegramBot['id']): string => rootURL + `_/${telegramBotId}/`;

	export const get = (telegramBotId: TelegramBot['id']) => makeRequest<Plugin[]>(url(telegramBotId), 'GET');
}

export namespace PluginAPI {
	export const url = (pluginId: Plugin['id']): string => rootURL + `${pluginId}/`;

	export const create = (
		telegramBotId: TelegramBot['id'],
		data: Data.PluginAPI.Create,
	) => makeRequest<APIResponse.PluginAPI.Create>(PluginsAPI.url(telegramBotId), 'POST', undefined, data);
	export const update = (
		pluginId: Plugin['id'],
		data: Data.PluginAPI.Update,
	) => makeRequest<APIResponse.PluginAPI.Update>(url(pluginId), 'PATCH', undefined, data);
	export const delete_ = (pluginId: Plugin['id']) => makeRequest(url(pluginId), 'DELETE');
}

export namespace PluginsLogsAPI {
	export const url = (telegramBotId: TelegramBot['id']): string => PluginsAPI.url(telegramBotId) + 'logs/';

	export const get = (telegramBotId: TelegramBot['id']) => makeRequest<PluginLog[]>(url(telegramBotId), 'GET');
}