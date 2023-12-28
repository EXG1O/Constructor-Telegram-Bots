export interface Donation {
	id: number;
	sum: number;
	telegram_url: string;
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
		export interface Get {
			count: string;
			next: string;
			previous: string;
			results: Donation[];
		}
	}
}