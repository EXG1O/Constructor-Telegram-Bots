import React, { ReactElement, memo, useCallback, useEffect, useMemo, useState } from 'react';

import Card, { CardProps } from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';

import MethodToggle, { Value as MethodValue } from './components/MethodToggle';
import Headers, { Data as HeadersData } from './components/Headers';
import Body, { Value as BodyData } from './components/Body';
import Test from './components/Test';

export interface Data {
	url: string;
	method: MethodValue;
	headers?: HeadersData;
	body?: BodyData;
}

export interface APIRequestProps extends Omit<CardProps, 'onChange' | 'children'>  {
	initialData?: Data;
	onChange: (data: Data) => void;
}

function APIRequest({ initialData, onChange, ...props }: APIRequestProps): ReactElement<APIRequestProps> {
	const [url, setURL] = useState<Data['url']>(initialData?.url ?? '');
	const [method, setMethod] = useState<MethodValue>(initialData?.method ?? 'get');
	const [headers, setHeaders] = useState<HeadersData | undefined>(initialData?.headers);
	const [body, setBody] = useState<BodyData | undefined>(initialData?.body);

	const [showHeaders, setShowHeaders] = useState<boolean>(Boolean(initialData?.headers));
	const [showBody, setShowBody] = useState<boolean>(Boolean(initialData?.body));

	useEffect(() => onChange({ url, method, headers, body }), [url, method, headers, body]);

	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('API-запрос')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				<Form.Control
					value={url}
					placeholder={gettext('Введите URL-адрес')}
					onChange={e => setURL(e.target.value)}
				/>
				<MethodToggle
					value={method}
					onChange={useCallback((value: MethodValue) => setMethod(value), [])}
				/>
				<Headers
					show={showHeaders}
					data={headers}
					onShow={useCallback(() => setShowHeaders(true), [])}
					onHide={useCallback(() => setShowHeaders(false), [])}
					onChange={useCallback(data => setHeaders(data), [])}
				/>
				<Body
					show={showBody}
					value={body}
					onShow={useCallback(() => setShowBody(true), [])}
					onHide={useCallback(() => setShowBody(false), [])}
					onChange={useCallback(value => setBody(value), [])}
				/>
				<Test
					url={url}
					data={useMemo(() => ({
						method,
						headers: headers?.map(header => [header.key, header.value]),
						body,
					}), [url, method, headers, body])}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(APIRequest);