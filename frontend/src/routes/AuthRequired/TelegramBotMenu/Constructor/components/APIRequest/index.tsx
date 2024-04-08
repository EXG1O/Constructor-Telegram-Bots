import React, { ReactElement, memo, useMemo, useState, useCallback } from 'react';

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
	data?: Data;
	onChange: (data: Data) => void;
}

export const defaultData: Data = { url: '', method: 'get' };

function APIRequest({ data = defaultData, onChange, ...props }: APIRequestProps): ReactElement<APIRequestProps> {
	const [showHeaders, setShowHeaders] = useState<boolean>(Boolean(data.headers));
	const [showBody, setShowBody] = useState<boolean>(Boolean(data.body));

	return (
		<Card {...props}>
			<Card.Header as='h6' className='text-center'>
				{gettext('API-запрос')}
			</Card.Header>
			<Card.Body className='vstack gap-2 p-2'>
				<Form.Control
					value={data.url}
					placeholder={gettext('Введите URL-адрес')}
					onChange={e => onChange({ ...data, url: e.target.value })}
				/>
				<MethodToggle
					value={data.method}
					onChange={useCallback((method: MethodValue) => onChange({ ...data, method }), [])}
				/>
				<Headers
					show={showHeaders}
					data={data.headers}
					onShow={useCallback(() => setShowHeaders(true), [])}
					onHide={useCallback(() => setShowHeaders(false), [])}
					onChange={useCallback(headers => onChange({ ...data, headers }), [])}
				/>
				<Body
					show={showBody}
					value={data.body}
					onShow={useCallback(() => setShowBody(true), [])}
					onHide={useCallback(() => setShowBody(false), [])}
					onChange={useCallback(body => onChange({ ...data, body }), [])}
				/>
				<Test
					url={data.url}
					data={useMemo(() => ({
						method: data.method,
						headers: data.headers?.map(header => [header.key, header.value]),
						body: data.body,
					}), [data])}
				/>
			</Card.Body>
		</Card>
	);
}

export default memo(APIRequest);