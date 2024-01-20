export interface InstructionSection {
	id: number;
	title: string;
	text: string;
}

export namespace APIResponse {
	export namespace InstructionSectionsAPI {
		export type Get = InstructionSection[];
	}
}