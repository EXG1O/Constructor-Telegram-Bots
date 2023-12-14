import Cookies from 'js-cookie';

export type ObjectAsJSON = Record<string, any>;

export namespace APIResponse {
	export interface Base<Ok extends boolean, Json extends ObjectAsJSON> extends Omit<Response, 'ok' | 'json'> {
		ok: Ok;
		json: Json;
	}

	export interface Success {
		message: string;
		level: 'success' | 'primary';
	}
	export interface Error {
		code: string;
		name: string | null;
		message: string;
		level: 'danger';
	}
}

export function headersWithAuthToken(): HeadersInit {
	const authToken = Cookies.get('auth-token');

	return { 'Authorization': `Token ${authToken}` };
}

export async function makeRequest<SuccessAPIResponse extends ObjectAsJSON = APIResponse.Success, ErrorAPIResponse extends ObjectAsJSON = APIResponse.Error>(
	url: string,
	method: 'GET' | 'POST' | 'PATCH' | 'DELETE',
	headers?: HeadersInit,
	data?: ObjectAsJSON | FormData,
): Promise<APIResponse.Base<true, SuccessAPIResponse> | APIResponse.Base<false, ErrorAPIResponse>> {
	let requestInit: RequestInit = { method: method };

	if (data !== undefined) {
		if (data instanceof FormData) {
			requestInit = Object.assign(requestInit, { body: data });
		} else {
			requestInit = Object.assign(requestInit, {
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(data),
			});
		}
	}

	const response = await fetch(url, Object.assign(requestInit, { headers: Object.assign(requestInit.headers || {}, headers || {}) }));

	return Object.assign(response, { json: await response.json() });
}