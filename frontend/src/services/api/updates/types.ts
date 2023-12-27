export interface Update {
	id: number;
	image: string;
	version: string;
	description: string;
	added_date: string;
}

export namespace Data {
	export namespace UpdatesAPI {
		export interface Get {
			offset?: number;
			limit?: number;
		}
	}
}