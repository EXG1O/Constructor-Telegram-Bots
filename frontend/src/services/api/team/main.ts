import { makeRequest } from 'services/api/base';
import { TeamMember } from './types';

const rootURL = '/api/team/';

export namespace TeamMembersAPI {
	export const url = rootURL + 'members/';

	export const get = () => makeRequest<TeamMember[]>(url, 'GET');
}