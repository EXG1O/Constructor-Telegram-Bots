export interface Member {
	id: number;
	image: string;
	username: string;
	speciality: string;
	joined_date: string;
}

export namespace APIResponse {
	export namespace MembersAPI {
		export type Get = Member[];
	}
}