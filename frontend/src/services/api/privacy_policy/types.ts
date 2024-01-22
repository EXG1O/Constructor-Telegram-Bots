export interface PrivacyPolicySection {
	id: number;
	title: string;
	text: string;
}

export namespace APIResponse {
	export namespace PrivacyPolicySectionsAPI {
		export type Get = PrivacyPolicySection[];
	}
}