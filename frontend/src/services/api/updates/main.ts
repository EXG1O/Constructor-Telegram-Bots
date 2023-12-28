import { makeRequest } from 'services/api/base';
import { APIResponse } from './types';

const rootURL = '/api/updates/';

export namespace TeamMembersAPI {
	export const get = (limit?: number, offset?: number) => (
		makeRequest<APIResponse.UpdatesAPI.Get>(`${rootURL}?limit=${limit ?? 0}&offset=${offset ?? 0}`, 'GET')
	);
}