import { APIResponse  as BaseApiResponse } from 'services/api/base';

export interface TelegramBot {
	id: number;
	username: string | null;
	api_token: string;
	storage_size: number;
	used_storage_size: number;
	remaining_storage_size: number;
	is_private: boolean;
	is_enabled: boolean;
	is_loading: boolean;
	added_date: string;
}

type HandlePositions = 'left' | 'right';

export interface Connection {
	id: number;
	source_object_type: 'command' | 'command_keyboard_button' | 'condition' | 'background_task';
	source_object_id: number;
	source_handle_position: HandlePositions;
	target_object_type: 'command' | 'condition';
	target_object_id: number;
	target_handle_position: HandlePositions;
}

export interface APIRequest {
	url: string;
	method: 'get' | 'post' | 'put' | 'patch' | 'delete';
	headers: Record<string, any> | null;
	body: Record<string, any> | null;
}

export interface CommandSettings {
	is_reply_to_user_message: boolean;
	is_delete_user_message: boolean;
	is_send_as_new_message: boolean;
}

export interface CommandTrigger {
	text: string;
	description: string | null;
}

export interface CommandImage {
	id: number;
	name: string;
	size: number;
	url: string;
}

export type CommandFile = CommandImage;

export interface CommandMessage {
	text: string;
}

export interface CommandKeyboardButton {
	id: number;
	row: number | null;
	text: string;
	url: string | null;
}

export interface CommandKeyboard {
	type: 'default' | 'inline' | 'payment';
	buttons: CommandKeyboardButton[];
}

export type CommandAPIRequest = APIRequest;

export interface CommandDatabaseRecord {
	data: Record<string, any>;
}

export interface Command {
	id: number;
	name: string;
	settings: CommandSettings;
	trigger: CommandTrigger | null;
	images: CommandImage[];
	files: CommandFile[];
	message: CommandMessage;
	keyboard: CommandKeyboard | null;
	api_request: CommandAPIRequest | null;
	database_record: CommandDatabaseRecord | null;
}

export interface ConditionPart {
	id: number;
	type: '+' | '-';
	first_value: string;
	operator: '==' | '!=' | '>' | '>=' | '<' | '<=';
	second_value: string;
	next_part_operator: '&&' | '||' | null;
}

export interface Condition {
	id: number;
	name: string;
	parts: ConditionPart[];
}

export type BackgroundTaskAPIRequest = APIRequest;

export interface BackgroundTask {
	id: number;
	name: string;
	interval: 1 | 3 | 7 | 14 | 28;
	api_request: BackgroundTaskAPIRequest | null;
}

export interface DiagramBlock {
	x: number;
	y: number;
	source_connections: Connection[];
	target_connections: Connection[];
}

export interface DiagramCommandKeyboardButton extends CommandKeyboardButton {
	source_connections: Connection[];
}

export interface DiagramCommandKeyboard extends Omit<CommandKeyboard, 'buttons'> {
	buttons: DiagramCommandKeyboardButton[];
}

export interface DiagramCommand extends Pick<Command, 'id' | 'name' | 'images' | 'files' | 'message'>, DiagramBlock {
	keyboard: DiagramCommandKeyboard | null;
}

export type DiagramCondition = Omit<Condition, 'parts'> & DiagramBlock;

export type DiagramBackgroundTask = Omit<BackgroundTask, 'api_request'> & Omit<DiagramBlock, 'source_connections'>;

export interface Variable {
	id: number;
	name: string;
	value: string;
	description: string;
}

export interface User {
	id: number;
	telegram_id: number;
	full_name: string;
	is_allowed: boolean;
	is_blocked: boolean;
	activated_date: string;
}

export namespace Data {
	export namespace TelegramBotsAPI {
		export type Create = Pick<TelegramBot, 'api_token' | 'is_private'>;
	}

	export namespace TelegramBotAPI {
		export type Update = Partial<TelegramBotsAPI.Create>;
	}

	export namespace ConnectionsAPI {
		export type Create = Omit<Connection, 'id'>;
	}

	export namespace CommandsAPI {
		interface CreateCommandTrigger extends Omit<CommandTrigger, 'description'> {
			description?: NonNullable<CommandTrigger['description']>;
		}

		export interface CreateCommandKeyboardButton extends Omit<CommandKeyboardButton, 'id' | 'row' | 'url'> {
			row?: NonNullable<CommandKeyboardButton['row']>;
			url?: NonNullable<CommandKeyboardButton['url']>;
		}

		interface CreateCommandKeyboard extends Omit<CommandKeyboard, 'buttons'> {
			buttons: CreateCommandKeyboardButton[];
		}

		interface CreateCommandAPIRequest extends Omit<CommandAPIRequest, 'headers' | 'body'> {
			headers?: NonNullable<CommandAPIRequest['headers']>;
			body?: NonNullable<CommandAPIRequest['body']>;
		}

		export interface Create {
			name: Command['name'];
			settings: Command['settings'];
			trigger?: CreateCommandTrigger;
			images?: File[],
			files?: File[],
			message: Command['message'];
			keyboard?: CreateCommandKeyboard;
			api_request?: CreateCommandAPIRequest;
			database_record?: NonNullable<Command['database_record']>;
		}
	}

	export namespace CommandAPI {
		interface UpdateCommandKeyboardButton extends CommandsAPI.CreateCommandKeyboardButton {
			id?: CommandKeyboardButton['id'];
		}

		interface UpdateCommandKeyboard extends Omit<CommandKeyboard, 'buttons'> {
			buttons: UpdateCommandKeyboardButton[];
		}

		export interface Update extends Omit<CommandsAPI.Create, 'images' | 'files' | 'keyboard'> {
			images?: (File | number)[];
			files?: (File | number)[];
			keyboard?: UpdateCommandKeyboard;
		}
	}

	export namespace ConditionsAPI {
		type CreateConditionPart = Omit<ConditionPart, 'id'>;

		export interface Create extends Omit<Condition, 'id' | 'parts'> {
			parts: CreateConditionPart[];
		}
	}

	export namespace ConditionAPI {
		export type Update = ConditionsAPI.Create;
	}

	export namespace BackgroundTasksAPI {
		type CreateBackgroundTaskAPIRequest = Omit<BackgroundTaskAPIRequest, 'id'>;

		export interface Create extends Omit<BackgroundTask, 'id' | 'api_request'> {
			api_request: CreateBackgroundTaskAPIRequest[];
		}
	}

	export namespace BackgroundTaskAPI {
		export type Update = BackgroundTasksAPI.Create;
	}

	export namespace DiagramCommandAPI {
		export interface Update {
			x?: number;
			y?: number;
		}
	}

	export namespace DiagramConditionAPI {
		export interface Update {
			x?: number;
			y?: number;
		}
	}

	export namespace DiagramBackgroundTaskAPI {
		export interface Update {
			x?: number;
			y?: number;
		}
	}

	export namespace VariableAPI {
		export type Create = Omit<Variable, 'id'>;
		export type Update = Create;
	}
}

export namespace APIResponse {
	export namespace StatsAPI {
		interface TelegramBotsStats {
			total: number;
			enabled: number;
		}

		interface UsersStats {
			total: number;
		}

		export interface Get {
			telegram_bots: TelegramBotsStats;
			users: UsersStats;
		}
	}

	export namespace TelegramBotsAPI {
		export type Get = TelegramBot[];
		export interface Create extends BaseApiResponse.Success {
			telegram_bot: TelegramBot;
		}
	}

	export namespace TelegramBotAPI {
		export type Get = TelegramBot;
		export type Update = TelegramBotsAPI.Create;

		export type Start = {};
		export type Restart = Start;
		export type Stop = Start;
	}

	export namespace ConnectionsAPI {
		export interface Create extends BaseApiResponse.Success {
			connection: Connection;
		}
	}

	export namespace CommandsAPI {
		export type Get = Command[];
		export interface Create extends BaseApiResponse.Success {
			command: Command;
		}
	}

	export namespace CommandAPI {
		export type Get = Command;
		export type Update = CommandsAPI.Create;
	}

	export namespace ConditionsAPI {
		export type Get = Condition[];
		export interface Create extends BaseApiResponse.Success {
			condition: Condition;
		}
	}

	export namespace ConditionAPI {
		export type Get = Condition;
		export type Update = ConditionsAPI.Create;
	}

	export namespace BackgroundTasksAPI {
		export type Get = BackgroundTask[];
		export interface Create extends BaseApiResponse.Success {
			background_task: BackgroundTask;
		}
	}

	export namespace BackgroundTaskAPI {
		export type Get = BackgroundTask;
		export type Update = BackgroundTasksAPI.Create;
	}

	export namespace DiagramCommandsAPI {
		export type Get = DiagramCommand[];
	}

	export namespace DiagramCommandAPI {
		export type Get = {};
	}

	export namespace DiagramConditionsAPI {
		export type Get = DiagramCondition[];
	}

	export namespace DiagramConditionAPI {
		export type Get = {};
	}

	export namespace DiagramBackgroundTasksAPI {
		export type Get = DiagramBackgroundTask[];
	}

	export namespace DiagramBackgroundTaskAPI {
		export type Get = {};
	}

	export namespace VariablesAPI {
		export namespace Get {
			export type Default = Variable[];
			export interface Pagination {
				count: number;
				next: string | null;
				previous: string | null;
				results: Variable[];
			}
		}
	}

	export namespace VariableAPI {
		export type Get = Variable;
		export interface Create extends BaseApiResponse.Success {
			variable: Variable;
		}
		export type Update = Create;
	}

	export namespace UserAPI {
		export type Get = User;
	}

	export namespace UsersAPI {
		export namespace Get {
			export type Default = User[];
			export interface Pagination {
				count: number;
				next: string | null;
				previous: string | null;
				results: User[];
			}
		}
	}
}