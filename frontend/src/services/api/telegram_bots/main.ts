import { makeRequest } from 'services/api/base';
import {
	TelegramBot,
	TelegramBotCommand,
	TelegramBotCommandDiagram,
	TelegramBotVariable,
	TelegramBotUser,
	Data,
	APIResponse,
} from './types';

const rootURL = '/api/telegram-bots/';

export namespace TelegramBotsAPI {
	export const get = () => makeRequest<TelegramBot[]>(rootURL, 'GET');
}

export namespace TelegramBotAPI {
	export const url = (telegramBotID: TelegramBot['id']) => rootURL + `${telegramBotID}/`;

	export const get = (telegramBotID: TelegramBot['id']) => makeRequest<TelegramBot>(url(telegramBotID), 'GET');
	export const create = (data: Data.TelegramBotAPI.Create) => makeRequest<APIResponse.TelegramBotAPI.Create>(rootURL, 'POST', undefined, data);
	export const update = (
		telegramBotID: TelegramBot['id'],
		data: Data.TelegramBotAPI.Update,
	) => makeRequest<APIResponse.TelegramBotAPI.Update>(url(telegramBotID), 'PATCH', undefined, data);
	export const _delete = (telegramBotID: TelegramBot['id']) => makeRequest(url(telegramBotID), 'DELETE');

	export const start = (telegramBotID: TelegramBot['id']) => makeRequest(url(telegramBotID) + '?action=start', 'POST');
	export const stop = (telegramBotID: TelegramBot['id']) => makeRequest(url(telegramBotID) + '?action=stop', 'POST');;
}

export namespace TelegramBotCommandsAPI {
	export const url = (telegramBotID: TelegramBot['id']) => TelegramBotAPI.url(telegramBotID) + 'commands/';

	export const get = (telegramBotID: TelegramBot['id']) => makeRequest<TelegramBotCommand[]>(url(telegramBotID), 'GET');
}

export namespace TelegramBotCommandAPI {
	export const url = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
	) => TelegramBotCommandsAPI.url(telegramBotID) + `${telegramBotCommandID}/`;

	export const get = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
	) => makeRequest<TelegramBotCommand>(url(telegramBotID, telegramBotCommandID), 'GET');
	export const create = (
		telegramBotID: TelegramBot['id'],
		data: Data.TelegramBotCommandAPI.Create,
	) => {
		const { images, files, ...data_ } = data;

		const formData = new FormData();
		images?.forEach((image, index) => formData.append(`image:${index}`, image, image.name));
		files?.forEach((file, index) => formData.append(`file:${index}`, file, file.name));
		formData.append('data', JSON.stringify(data_));

		return makeRequest(TelegramBotCommandsAPI.url(telegramBotID), 'POST', undefined, formData);
	}
	export const update = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
		data: Data.TelegramBotCommandAPI.Update,
	) => {
		const { images, files, ...data_ } = data;

		const formData = new FormData();
		images?.forEach((image, index) => {
			const name = `image:${index}`;

			if (typeof image === 'number') {
				formData.append(name, image.toString());
			} else {
				formData.append(name, image, image.name);
			}
		});
		files?.forEach((file, index) => {
			const name = `file:${index}`;

			if (typeof file === 'number') {
				formData.append(name, file.toString());
			} else {
				formData.append(name, file, file.name);
			}
		});
		formData.append('data', JSON.stringify(data_));

		return makeRequest(TelegramBotCommandAPI.url(telegramBotID, telegramBotCommandID), 'PATCH', undefined, formData);
	};
	export const _delete = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
	) => makeRequest(url(telegramBotID, telegramBotCommandID), 'DELETE');
}

export namespace TelegramBotCommandsDiagramAPI {
	export const url = (telegramBotID: TelegramBot['id']) => TelegramBotAPI.url(telegramBotID) + 'diagram/commands/';

	export const get = (telegramBotID: TelegramBot['id']) => makeRequest<TelegramBotCommandDiagram[]>(url(telegramBotID), 'GET');
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
	) => makeRequest(url(telegramBotID, telegramBotCommandID), 'POST', undefined, data);
	export const disconnect = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
		data: Data.TelegramBotCommandDiagramAPI.Disconnect,
	) => makeRequest(url(telegramBotID, telegramBotCommandID), 'DELETE', undefined, data);

	export const updatePosition = (
		telegramBotID: TelegramBot['id'],
		telegramBotCommandID: TelegramBotCommand['id'],
		data: Data.TelegramBotCommandDiagramAPI.UpdatePosition,
	) => makeRequest(url(telegramBotID, telegramBotCommandID), 'PATCH', undefined, data);
}

export namespace TelegramBotVariablesAPI {
	export const url = (telegramBotID: TelegramBot['id']) => TelegramBotAPI.url(telegramBotID) + 'variables/';

	export const get = (telegramBotID: TelegramBot['id']) => makeRequest<TelegramBotVariable[]>(url(telegramBotID), 'GET');
}

export namespace TelegramBotVariableAPI {
	export const url = (
		telegramBotID: TelegramBot['id'],
		telegramBotVariableID: TelegramBotVariable['id'],
	) => TelegramBotVariablesAPI.url(telegramBotID) + `${telegramBotVariableID}/`;

	export const get = (
		telegramBotID: TelegramBot['id'],
		telegramBotVariableID: TelegramBotVariable['id'],
	) => makeRequest<TelegramBotVariable>(url(telegramBotID, telegramBotVariableID), 'GET');
	export const create = (
		telegramBotID: TelegramBot['id'],
		data: Data.TelegramBotVariableAPI.Create,
	) => makeRequest<APIResponse.TelegramBotVariableAPI.Create>(TelegramBotVariablesAPI.url(telegramBotID), 'POST', undefined, data);
	export const update = (
		telegramBotID: TelegramBot['id'],
		telegramBotVariableID: TelegramBotVariable['id'],
		data: Data.TelegramBotVariableAPI.Update,
	) => makeRequest<APIResponse.TelegramBotVariableAPI.Update>(url(telegramBotID, telegramBotVariableID), 'PATCH', undefined, data);
	export const _delete = (
		telegramBotID: TelegramBot['id'],
		telegramBotVariableID: TelegramBotVariable['id'],
	) => makeRequest(url(telegramBotID, telegramBotVariableID), 'DELETE');
}

export namespace TelegramBotUsersAPI {
	export const url = (telegramBotID: TelegramBot['id']) => TelegramBotAPI.url(telegramBotID) + 'users/';

	export const get = (telegramBotID: TelegramBot['id']) => makeRequest<TelegramBotUser[]>(url(telegramBotID), 'GET');
}

export namespace TelegramBotUserAPI {
	export const url = (
		telegramBotID: TelegramBot['id'],
		telegramBotUserID: TelegramBotUser['id'],
	) => `${TelegramBotUsersAPI.url(telegramBotID)}${telegramBotUserID}/`;

	export const get = (
		telegramBotID: TelegramBot['id'],
		telegramBotUserID: TelegramBotUser['id'],
	) => makeRequest<TelegramBotUser>(url(telegramBotID, telegramBotUserID), 'GET');
	export const post = (
		telegramBotID: TelegramBot['id'],
		telegramBotUserID: TelegramBotUser['id'],
		action: 'allow' | 'unallow' | 'block' | 'unblock',
	) => makeRequest(url(telegramBotID, telegramBotUserID) + `?action=${action}`, 'POST');
	export const _delete = (
		telegramBotID: TelegramBot['id'],
		telegramBotUserID: TelegramBotUser['id'],
	) => makeRequest(url(telegramBotID, telegramBotUserID), 'DELETE');
}