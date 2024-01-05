export namespace APIResponse {
	export interface Base<Ok extends boolean, Json extends Record<string, any>> extends Omit<Response, 'ok' | 'json'> {
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

export async function makeRequest<SuccessAPIResponse extends Record<string, any> = APIResponse.Success, ErrorAPIResponse extends Record<string, any> = APIResponse.Error>(
	url: string,
	method: 'GET' | 'POST' | 'PATCH' | 'DELETE',
	headers?: HeadersInit,
	data?: Record<string, any> | FormData,
): Promise<APIResponse.Base<true, SuccessAPIResponse> | APIResponse.Base<false, ErrorAPIResponse>> {
	let requestInit: RequestInit = { method };

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