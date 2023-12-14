import { makeRequest } from 'services/api/base';
import { InstructionSection } from './types';

const rootUrl = '/api/instruction/';

export namespace InstructionSectionsAPI {
	const url = rootUrl + 'sections/';

	export const get = () => makeRequest<InstructionSection[]>(url, 'GET');
}