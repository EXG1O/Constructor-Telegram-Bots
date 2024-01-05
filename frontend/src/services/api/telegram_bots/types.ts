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

export interface TelegramBotCommandCommand {
	text: string;
	description: string | null;
}

export interface TelegramBotCommandImage {
	url: string;
}

export type TelegramBotCommandFile = TelegramBotCommandImage;

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
	command: TelegramBotCommandCommand | null;
	images: TelegramBotCommandImage[] | null;
	files: TelegramBotCommandFile[] | null;
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

export interface TelegramBotCommandDiagram extends Pick<TelegramBotCommand, 'id' | 'name' | 'message_text'> {
	keyboard: TelegramBotCommandKeyboardDiagram | null;

	x: number;
	y: number;
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
		export interface CreateTelegramBotCommandCommand extends Omit<TelegramBotCommandCommand, 'description'> {
			description?: TelegramBotCommandCommand['description'];
		}

		interface CreateTelegramBotCommandKeyboardButton extends Omit<TelegramBotCommandKeyboardButton, 'id' | 'row' | 'url'> {
			row?: TelegramBotCommandKeyboardButton['row'];
			url?: TelegramBotCommandKeyboardButton['url'];
		}

		interface CreateTelegramBotCommandKeyboard extends Omit<TelegramBotCommandKeyboard, 'buttons'> {
			buttons: CreateTelegramBotCommandKeyboardButton[];
		}

		interface CreateTelegramBotCommandApiRequest extends Omit<TelegramBotCommandApiRequest, 'headers' | 'body'> {
			headers?: TelegramBotCommandApiRequest['headers'];
			body?: TelegramBotCommandApiRequest['body'];
		}

		export interface Create {
			name: TelegramBotCommand['name'];
			command?: CreateTelegramBotCommandCommand | null;
			images?: File[],
			files?: File[],
			message_text: TelegramBotCommand['message_text'];
			keyboard?: CreateTelegramBotCommandKeyboard | null;
			api_request?: CreateTelegramBotCommandApiRequest | null;
			database_record?: TelegramBotCommand['database_record'];
		}

		interface UpdateTelegramBotCommandKeyboardButton extends CreateTelegramBotCommandKeyboardButton {
			id?: TelegramBotCommandKeyboardButton['id'];
		}

		interface UpdateTelegramBotCommandKeyboard extends Omit<TelegramBotCommandKeyboard, 'buttons'> {
			buttons: UpdateTelegramBotCommandKeyboardButton[];
		}

		export interface Update extends Omit<Create, 'keyboard'> {
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
}

export namespace APIResponse {
	export namespace TelegramBotAPI {
		export interface Create extends BaseApiResponse.Success {
			telegram_bot: TelegramBot;
		}
		export type Update = Create;
	}
}