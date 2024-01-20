import { makeRequest } from 'services/api/base';
import { APIResponse } from './types';

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

	export const get = () => makeRequest<APIResponse.DonationSectionsAPI.Get>(url, 'GET');
}

export namespace DonationButtonsAPI {
	export const url = rootURL + 'buttons/';

	export const get = () => makeRequest<APIResponse.DonationButtonsAPI.Get>(url, 'GET');
}
