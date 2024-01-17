export interface Update {
	id: number;
	image: string;
	version: string;
	description: string;
	added_date: string;
}

export namespace APIResponse {
	export namespace UpdatesAPI {
		export namespace Get {
			export type Default = Update[];
			export interface Pagination {
				count: number;
				next: string | null;
				previous: string | null;
				results: Update[];
			}
		}
	}
}