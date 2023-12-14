import { makeRequest } from 'services/api/base';
import { Update, Data } from './types';

const rootURL = '/api/team/';

export namespace TeamMembersAPI {
	export const get = (data: Data.UpdatesAPI.Get) => makeRequest<Update[]>(rootURL, 'POST', undefined, data);
}