export interface User {
	id: number;
	telegram_id: number;
	first_name: string;
	last_name: string;
	is_staff: boolean;
	joined_date: string;
}

export namespace Data {
	export namespace UserAPI {
		export interface Login {
			user_id: number;
			confirm_code: string;
		}
	}
}