import { ObjectAsJSON, APIResponse  as BaseApiResponse } from 'services/api/base';

export interface TelegramBot {
	id: number;
	username: string | null;
	api_token: string;
	is_private: boolean;
	is_running: boolean;
	is_stopped: boolean;
	commands_count: number;
	users_count: number;
	added_date: string;
}

interface TelegramBotCommandCommand {
	text: string;
	is_show_in_menu: boolean;
	description: string | null;
}

interface TelegramBotCommandMessageText {
	text: string;
}

export interface TelegramBotCommandKeyboardButton {
	id: number;
	row: number | null;
	text: string;
	url: string | null;

	telegram_bot_command_id: number | null;
	start_diagram_connector: number | null;
	end_diagram_connector: number | null;
}

interface TelegramBotCommandKeyboard {
	mode: 'default' | 'inline' | 'payment';
	buttons: TelegramBotCommandKeyboardButton[];
}

interface TelegramBotCommandApiRequest {
	url: string;
	method: 'get' | 'post' | 'put' | 'patch' | 'delete';
	headers: ObjectAsJSON | null;
	data: ObjectAsJSON | null;
}

export interface TelegramBotCommand {
	id: number;
	name: string;
	command: TelegramBotCommandCommand | null;
	image: string | null;
	message_text: TelegramBotCommandMessageText;
	keyboard: TelegramBotCommandKeyboard | null;
	api_request: TelegramBotCommandApiRequest | null;
	database_record: ObjectAsJSON | null;

	x: number;
	y: number;
}

export interface TelegramBotUser {
	id: number;
	user_id: number;
	full_name: string;
	is_allowed: boolean;
	activated_date: string;
}

export interface TelegramBotDatabaseRecord extends ObjectAsJSON {
	_id: number;
}

export namespace Data {
	export namespace TelegramBotAPI {
		export interface Create {
			api_token: TelegramBot['api_token'];
			is_private: TelegramBot['is_private'];
		}
		export interface Update {
			api_token?: TelegramBot['api_token'];
			is_private?: TelegramBot['is_private'];
		}

		export interface UpdateDiagramCurrentScale {
			diagram_current_scale: number;
		}
	}

	export namespace TelegramBotCommandAPI {
		type CreateTelegramBotCommandKeyboardButton = Omit<TelegramBotCommandKeyboardButton, 'id' | 'telegram_bot_command_id' | 'start_diagram_connector' | 'end_diagram_connector'>;

		interface CreateTelegramBotCommandKeyboard extends Omit<TelegramBotCommandKeyboard, 'buttons'> {
			buttons: CreateTelegramBotCommandKeyboardButton[];
		}

		interface CreateTelegramBotCommand extends Omit<TelegramBotCommand, 'id' | 'image' | 'keyboard' | 'x' | 'y'> {
			keyboard: CreateTelegramBotCommandKeyboard | null;
		}

		export interface Create {
			image: Blob;
			data: CreateTelegramBotCommand;
		}

		type UpdateTelegramBotCommandKeyboardButton = Omit<TelegramBotCommandKeyboardButton, 'telegram_bot_command_id' | 'start_diagram_connector' | 'end_diagram_connector'>;

		interface UpdateTelegramBotCommandKeyboard extends Omit<TelegramBotCommandKeyboard, 'buttons'> {
			buttons: UpdateTelegramBotCommandKeyboardButton[];
		}

		interface UpdateTelegramBotCommand extends Omit<TelegramBotCommand, | 'image' | 'keyboard' | 'x' | 'y'> {
			keyboard: UpdateTelegramBotCommandKeyboard | null;
		}

		export interface Update {
			image: Blob;
			data: UpdateTelegramBotCommand;
		}

		export interface UpdatePosition {
			x: number;
			y: number;
		}
	}

	export namespace TelegramBotCommandKeyboardButtonAPI {
		export type Connect = Omit<TelegramBotCommandKeyboardButton, 'id' | 'row' | 'text' | 'url'>;
		export type Disconnect = Connect;
	}

	export namespace TelegramBotDatabaseRecordAPI {
		export interface Create {
			record: Omit<TelegramBotDatabaseRecord, '_id'>;
		}
		export type Update = Create;
	}
}

export namespace APIResponse {
	export namespace TelegramBotAPI {
		export interface Create extends BaseApiResponse.Success {
			telegram_bot: TelegramBot;
		}
	}

	export namespace TelegramBotDatabaseRecordAPI {
		export interface Create extends BaseApiResponse.Success {
			record: TelegramBotDatabaseRecord;
		}
		export type Update = Create;
	}
}