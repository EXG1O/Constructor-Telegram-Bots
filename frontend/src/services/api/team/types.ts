export interface TeamMember {
	id: number;
	image: string;
	username: string;
	speciality: string;
	joined_date: string;
}

export namespace APIResponse {
	export namespace TeamMembersAPI {
		export type Get = TeamMember[];
	}
}