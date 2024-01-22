export interface PrivacyPolicySection {
	id: number;
	title: string;
	text: string;
}

export namespace APIResponse {
	export namespace PrivacyPolicySectionsAPI {
		export interface Get {
			last_update_date: string | null;
			results: PrivacyPolicySection[];
		}
	}
}