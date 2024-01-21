import { makeRequest } from 'services/api/base';
import { APIResponse } from './types';

const rootURL = '/api/updates/';

export namespace UpdatesAPI {
	export const get = <Limit extends number | undefined>(limit?: Limit, offset?: number) => (
		makeRequest<
			Limit extends number ?
			APIResponse.UpdatesAPI.Get.Pagination :
			APIResponse.UpdatesAPI.Get.Default
		>(rootURL + `?limit=${limit ?? 0}&offset=${offset ?? 0}`, 'GET')
	);
}