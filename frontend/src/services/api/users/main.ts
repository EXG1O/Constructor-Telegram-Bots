import { makeRequest } from 'services/api/base';
import { Data, APIResponse } from './types';

const rootURL = '/api/users/';

export namespace UserAPI {
	export const url = rootURL + '_/';

	export const get = () => makeRequest<APIResponse.UserAPI.Get>(url, 'GET');
	export const login = (data: Data.UserAPI.Login) => makeRequest(url + 'login/', 'POST', undefined, data);
	export const logout = () => makeRequest(url + 'logout/', 'POST');
}