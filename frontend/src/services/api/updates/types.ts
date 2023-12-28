export interface Update {
	id: number;
	image: string;
	version: string;
	description: string;
	added_date: string;
}

export namespace APIResponse {
	export namespace UpdatesAPI {
		export interface Get {
			count: string;
			next: string;
			previous: string;
			results: Update[];
		}
	}
}