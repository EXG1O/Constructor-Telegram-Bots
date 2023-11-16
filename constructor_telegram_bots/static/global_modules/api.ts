export type ObjectAsJson = Record<string, any>;

export namespace ApiResponse {
	export interface Base<Ok extends boolean, Json extends ObjectAsJson> extends Omit<Response, 'ok' | 'json'> {
		ok: Ok;
		json: Json;
	}
	export interface Success {
		message: string | null;
		level: 'success' | 'primary';
	}
	export interface Error {
		code: string;
		name: string | null;
		message: string;
		level: 'danger';
	}

	export type Default<Json extends ObjectAsJson> = Base<true, Json> | Base<false, Success>;
}

export async function makeRequest<ApiResponseJson extends ObjectAsJson>(
	url: string,
	method: 'POST' | 'PATCH' | 'DELETE' | 'GET',
	headers?: HeadersInit,
	data?: ObjectAsJson | FormData,
): Promise<ApiResponse.Default<ApiResponseJson>> {
	let requestInit: RequestInit = {
		method: method,
	}

	if (data) {
		if (data instanceof FormData) {
			requestInit = Object.assign(requestInit, {
				body: data,
			});
		} else {
			requestInit = Object.assign(requestInit, {
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify(data),
			});
		}
	}

	if (requestInit.headers || headers) {
		requestInit = Object.assign(requestInit, {
			headers: Object.assign({}, (requestInit.headers || {}), (headers || {})),
		});
	}

	const response = await fetch(url, requestInit);

	return {...response, json: await response.json()}
}