import { makeRequest } from 'services/api/base';
import { APIResponse } from './types';

const rootUrl = '/api/instruction/';

export namespace InstructionSectionsAPI {
	const url = rootUrl + 'sections/';

	export const get = () => makeRequest<APIResponse.InstructionSectionsAPI.Get>(url, 'GET');
}