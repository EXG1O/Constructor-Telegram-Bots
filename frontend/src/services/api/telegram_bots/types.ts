import { ObjectAsJSON, APIResponse  as BaseApiResponse } from 'services/api/base';

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
	headers: ObjectAsJSON | null;
	body: ObjectAsJSON | null;
}

export interface TelegramBotCommand {
	id: number;
	name: string;
	command: TelegramBotCommandCommand | null;
	image: string | null;
	message_text: TelegramBotCommandMessageText;
	keyboard: TelegramBotCommandKeyboard | null;
	api_request: TelegramBotCommandApiRequest | null;
}

export interface TelegramBotCommandKeyboardButtonDiagram extends TelegramBotCommandKeyboardButton {
	telegram_bot_command_id: number | null;
	start_diagram_connector: string | null;
	end_diagram_connector: string | null;
}

export interface TelegramBotCommandKeyboardDiagram extends Omit<TelegramBotCommandKeyboard, 'buttons'> {
	buttons: TelegramBotCommandKeyboardButtonDiagram[];
}

export interface TelegramBotCommandDiagram extends Omit<TelegramBotCommand, 'command' | 'keyboard' | 'api_request'> {
	keyboard: TelegramBotCommandKeyboardDiagram | null;

	x: number;
	y: number;
}

export interface TelegramBotUser {
	id: number;
	telegram_id: number;
	full_name: string;
	is_allowed: boolean;
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
			command?: CreateTelegramBotCommandCommand;
			message_text: TelegramBotCommand['message_text'];
			keyboard?: CreateTelegramBotCommandKeyboard;
			api_request?: CreateTelegramBotCommandApiRequest;
		}

		interface UpdateTelegramBotCommandKeyboardButton extends CreateTelegramBotCommandKeyboardButton {
			id?: TelegramBotCommandKeyboardButton['id'];
		}

		interface UpdateTelegramBotCommandKeyboard extends Omit<TelegramBotCommandKeyboard, 'buttons'> {
			buttons: UpdateTelegramBotCommandKeyboardButton[];
		}

		export interface Update extends Omit<Create, 'keyboard'> {
			keyboard?: UpdateTelegramBotCommandKeyboard;
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