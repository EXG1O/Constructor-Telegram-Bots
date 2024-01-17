import { makeRequest } from 'services/api/base';
import { DonationSection, DonationButton, APIResponse } from './types';

const rootURL = '/api/donations/';

export namespace DonationsAPI {
	export const get = <Limit extends number | undefined>(limit: Limit, offset?: number) => (
		makeRequest<
			Limit extends number ?
			APIResponse.DonationsAPI.Get.Pagination :
			APIResponse.DonationsAPI.Get.Default
		>(rootURL + `?limit=${limit ?? 0}&offset=${offset ?? 0}`, 'GET')
	);
}

export namespace DonationSectionsAPI {
	export const url = rootURL + 'sections/';

	export const get = () => makeRequest<DonationSection[]>(url, 'GET');
}

export namespace DonationButtonsAPI {
	export const url = rootURL + 'buttons/';

	export const get = () => makeRequest<DonationButton[]>(url, 'GET');
}
