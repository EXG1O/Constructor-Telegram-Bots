import { APIResponse as BaseAPIResponse } from 'services/api/base';

export interface Plugin {
	id: number;
	name: string;
	code: string;
	is_checked: boolean;
	added_date: string;
}

export interface PluginLog {
	id: number;
	plugin_name: string;
	message: string;
	level: 'success' | 'info' | 'danger';
}

export namespace Data {
	export namespace PluginAPI {
		export interface Create {
			name: Plugin['name'],
			code: Plugin['code'];
		}
		export type Update = Omit<Create, 'name'>;
	}
}

export namespace APIResponse {
	export namespace PluginAPI {
		export interface Create extends BaseAPIResponse.Success {
			plugin: Plugin;
		}
		export type Update = Create;
	}
}