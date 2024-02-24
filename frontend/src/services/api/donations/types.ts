export interface Donation {
	id: number;
	sum: number;
	contact_link: string;
	date: string;
}

export interface DonationSection {
	id: number;
	title: string;
	text: string;
}

export interface DonationButton {
	id: number;
	text: string;
	url: string;
}

export namespace APIResponse {
	export namespace DonationsAPI {
		export namespace Get {
			export type Default = Donation[];
			export interface Pagination {
				count: number;
				next: string | null;
				previous: string | null;
				results: Donation[];
			}
		}
	}

	export namespace DonationSectionsAPI {
		export type Get = DonationSection[];
	}

	export namespace DonationButtonsAPI {
		export type Get = DonationButton[];
	}
}