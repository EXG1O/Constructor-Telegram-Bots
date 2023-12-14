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

export namespace Data {
	export namespace DonationsAPI {
		export interface Get {
			offset?: number;
			limit?: number;
		}
	}
}