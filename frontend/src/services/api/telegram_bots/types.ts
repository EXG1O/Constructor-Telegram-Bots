import { APIResponse  as BaseApiResponse } from 'services/api/base';

export interface TelegramBot {
	id: number;
	username: string | null;
	api_token: string;
	is_private: boolean;
	is_running: boolean;
	is_stopped: boolean;
	added_date: string;
}

export interface TelegramBotCommandSettings {
	is_reply_to_user_message: boolean;
	is_delete_user_message: boolean;
	is_send_as_new_message: boolean;
}

export interface TelegramBotCommandCommand {
	text: string;
	description: string | null;
}

export interface TelegramBotCommandImage {
	id: number;
	name: string;
	size: number;
	url: string;
}

export type TelegramBotCommandFile = Omit<TelegramBotCommandImage, 'url'>;

export interface TelegramBotCommandMessageText {
	text: string;
}

export interface TelegramBotCommandKeyboardButton {
	id: number;
	row: number | null;
	text: string;
	url: string | null;
}

export interface TelegramBotCommandKeyboard {
	type: 'default' | 'inline' | 'payment';
	buttons: TelegramBotCommandKeyboardButton[];
}

export interface TelegramBotCommandApiRequest {
	url: string;
	method: 'get' | 'post' | 'put' | 'patch' | 'delete';
	headers: Record<string, any> | null;
	body: Record<string, any> | null;
}

export interface TelegramBotCommandDatabaseRecord {
	data: Record<string, any>;
}

export interface TelegramBotCommand {
	id: number;
	name: string;
	settings: TelegramBotCommandSettings;
	command: TelegramBotCommandCommand | null;
	images: TelegramBotCommandImage[];
	files: TelegramBotCommandFile[];
	message_text: TelegramBotCommandMessageText;
	keyboard: TelegramBotCommandKeyboard | null;
	api_request: TelegramBotCommandApiRequest | null;
	database_record: TelegramBotCommandDatabaseRecord | null;
}

export interface TelegramBotCommandKeyboardButtonDiagram extends TelegramBotCommandKeyboardButton {
	telegram_bot_command_id: number | null;
	start_diagram_connector: string | null;
	end_diagram_connector: string | null;
}

export interface TelegramBotCommandKeyboardDiagram extends Omit<TelegramBotCommandKeyboard, 'buttons'> {
	buttons: TelegramBotCommandKeyboardButtonDiagram[];
}

export interface TelegramBotCommandDiagram extends Pick<TelegramBotCommand, 'id' | 'name' | 'images' | 'files' | 'message_text'> {
	keyboard: TelegramBotCommandKeyboardDiagram | null;

	x: number;
	y: number;
}

export interface TelegramBotVariable {
	id: number;
	name: string;
	value: string;
	description: string;
}

export interface TelegramBotUser {
	id: number;
	telegram_id: number;
	full_name: string;
	is_allowed: boolean;
	is_blocked: boolean;
	activated_date: string;
}

export namespace Data {
	export namespace TelegramBotAPI {
		export interface Create {
			api_token: string;
			is_private: boolean;
		}
		export type Update = Partial<Create>;
	}

	export namespace TelegramBotCommandAPI {
		interface CreateTelegramBotCommandCommand extends Omit<TelegramBotCommandCommand, 'description'> {
			description?: NonNullable<TelegramBotCommandCommand['description']>;
		}

		interface CreateTelegramBotCommandKeyboardButton extends Omit<TelegramBotCommandKeyboardButton, 'id' | 'row' | 'url'> {
			row?: NonNullable<TelegramBotCommandKeyboardButton['row']>;
			url?: NonNullable<TelegramBotCommandKeyboardButton['url']>;
		}

		interface CreateTelegramBotCommandKeyboard extends Omit<TelegramBotCommandKeyboard, 'buttons'> {
			buttons: CreateTelegramBotCommandKeyboardButton[];
		}

		interface CreateTelegramBotCommandApiRequest extends Omit<TelegramBotCommandApiRequest, 'headers' | 'body'> {
			headers?: NonNullable<TelegramBotCommandApiRequest['headers']>;
			body?: NonNullable<TelegramBotCommandApiRequest['body']>;
		}

		export interface Create {
			name: TelegramBotCommand['name'];
			settings: TelegramBotCommand['settings'];
			command?: CreateTelegramBotCommandCommand;
			images?: File[],
			files?: File[],
			message_text: TelegramBotCommand['message_text'];
			keyboard?: CreateTelegramBotCommandKeyboard;
			api_request?: CreateTelegramBotCommandApiRequest;
			database_record?: NonNullable<TelegramBotCommand['database_record']>;
		}

		interface UpdateTelegramBotCommandKeyboardButton extends CreateTelegramBotCommandKeyboardButton {
			id?: TelegramBotCommandKeyboardButton['id'];
		}

		interface UpdateTelegramBotCommandKeyboard extends Omit<TelegramBotCommandKeyboard, 'buttons'> {
			buttons: UpdateTelegramBotCommandKeyboardButton[];
		}

		export interface Update extends Omit<Create, 'images' | 'files' | 'keyboard'> {
			images?: (File | number)[];
			files?: (File | number)[];
			keyboard?: UpdateTelegramBotCommandKeyboard | null;
		}
	}

	export namespace TelegramBotCommandDiagramAPI {
		export interface Connect {
			telegram_bot_command_keyboard_button_id: number;
			telegram_bot_command_id: number;
			start_diagram_connector: string;
			end_diagram_connector: string;
		}
		export type Disconnect = Pick<Connect, 'telegram_bot_command_keyboard_button_id'>;

		export interface UpdatePosition {
			x: number;
			y: number;
		}
	}

	export namespace TelegramBotVariableAPI {
		export type Create = Omit<TelegramBotVariable, 'id'>;
		export type Update = Create;
	}
}

export namespace APIResponse {
	export namespace TelegramBotsAPI {
		export type Get = TelegramBot[];
	}

	export namespace TelegramBotAPI {
		export interface Get extends TelegramBot {
			memory_limit: number;
			used_memory: number;
			remaining_memory: number;
		}
		export interface Create extends BaseApiResponse.Success {
			telegram_bot: TelegramBot;
		}
		export type Update = Create;

		export type Start = {};
		export type Stop = Start;
	}

	export namespace TelegramBotCommandsAPI {
		export type Get = TelegramBotCommand[];
	}

	export namespace TelegramBotCommandAPI {
		export type Get = TelegramBotCommand;
	}

	export namespace TelegramBotCommandsDiagramAPI {
		export type Get = TelegramBotCommandDiagram[];
	}

	export namespace TelegramBotCommandDiagramAPI {
		export type Get = {};
	}

	export namespace TelegramBotVariablesAPI {
		export namespace Get {
			export type Default = TelegramBotVariable[];
			export interface Pagination {
				count: number;
				next: string | null;
				previous: string | null;
				results: TelegramBotVariable[];
			}
		}
	}

	export namespace TelegramBotVariableAPI {
		export type Get = TelegramBotVariable;
		export interface Create extends BaseApiResponse.Success {
			telegram_bot_variable: TelegramBotVariable;
		}
		export type Update = Create;
	}

	export namespace TelegramBotUserAPI {
		export type Get = TelegramBotUser;
	}

	export namespace TelegramBotUsersAPI {
		export namespace Get {
			export type Default = TelegramBotUser[];
			export interface Pagination {
				count: number;
				next: string | null;
				previous: string | null;
				results: TelegramBotUser[];
			}
		}
	}
}