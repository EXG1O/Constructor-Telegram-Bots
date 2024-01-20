import { makeRequest } from 'services/api/base';
import { APIResponse } from './types';

const rootURL = '/api/team/';

export namespace TeamMembersAPI {
	export const url = rootURL + 'members/';

	export const get = () => makeRequest<APIResponse.TeamMembersAPI.Get>(url, 'GET');
}