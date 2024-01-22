import { makeRequest } from 'services/api/base';
import { APIResponse } from './types';

const rootUrl = '/api/privacy-policy/';

export namespace PrivacyPolicySectionsAPI {
	const url = rootUrl + 'sections/';

	export const get = () => makeRequest<APIResponse.PrivacyPolicySectionsAPI.Get>(url, 'GET');
}