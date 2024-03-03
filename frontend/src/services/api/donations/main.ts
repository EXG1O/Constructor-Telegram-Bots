import { makeRequest } from 'services/api/base';
import { APIResponse } from './types';

const rootURL = '/api/donations/';

export namespace DonationsAPI {
	export const get = <Limit extends number | undefined>(
		limit?: Limit,
		offset?: number,
	) => makeRequest<
		Limit extends number ?
		APIResponse.DonationsAPI.Get.Pagination :
		APIResponse.DonationsAPI.Get.Default
	>(rootURL + `?limit=${limit ?? 0}&offset=${offset ?? 0}`, 'GET');
}

export namespace SectionsAPI {
	export const url = rootURL + 'sections/';

	export const get = () => makeRequest<APIResponse.SectionsAPI.Get>(url, 'GET');
}

export namespace ButtonsAPI {
	export const url = rootURL + 'buttons/';

	export const get = () => makeRequest<APIResponse.ButtonsAPI.Get>(url, 'GET');
}
