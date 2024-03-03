import { makeRequest } from 'services/api/base';
import { APIResponse } from './types';

const rootURL = '/api/team/';

export namespace MembersAPI {
	export const url = rootURL + 'members/';

	export const get = () => makeRequest<APIResponse.MembersAPI.Get>(url, 'GET');
}