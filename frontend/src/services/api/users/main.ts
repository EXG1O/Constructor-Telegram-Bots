import { headersWithAuthToken, makeRequest } from 'services/api/base';
import { User, Data } from './types';

const rootURL = '/api/';

export namespace UsersAPI {
	export const url = rootURL + 'users/';

	export const get = () => makeRequest(url, 'GET');
}

export namespace UserAPI {
	export const url = rootURL + 'user/';

	export const get = () => makeRequest<User>(url, 'GET', headersWithAuthToken());
	export const login = (data: Data.UserAPI.Login) => makeRequest(url + 'login/', 'POST', undefined, data);
	export const logout = () => makeRequest(url + 'logout/', 'POST', headersWithAuthToken());
	export const delete_ = () => makeRequest(url, 'DELETE', headersWithAuthToken());
}