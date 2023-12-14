import { makeRequest } from 'services/api/base';
import { Donation, DonationSection, DonationButton, Data } from './types';

const rootURL = '/api/donations/';

export namespace DonationsAPI {
	export const get = (data: Data.DonationsAPI.Get) => makeRequest<Donation[]>(rootURL, 'POST', undefined, data);
}

export namespace DonationSectionsAPI {
	export const url = rootURL + 'sections/';

	export const get = () => makeRequest<DonationSection[]>(url, 'GET');
}

export namespace DonationButtonsAPI {
	export const url = rootURL + 'buttons/';

	export const get = () => makeRequest<DonationButton[]>(url, 'GET');
}
