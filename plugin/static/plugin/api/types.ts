import { ApiResponse  as BaseApiResponse } from 'global_modules/api';

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
	export namespace Plugin {
		export interface Create {
			name: string,
			code: string;
		}
		export type Update = Omit<Create, 'name'>;
	}
}

export namespace ApiResponse {
	export namespace Plugin {
		export interface Create extends BaseApiResponse.Success {
			plugin: Plugin;
		}
		export type Update = Create;
	}
}