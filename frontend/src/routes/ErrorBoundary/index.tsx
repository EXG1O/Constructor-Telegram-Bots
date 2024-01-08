import React, { ReactElement, useEffect } from 'react';
import { useRouteError } from 'react-router-dom';

import Loading from 'components/Loading';

import useToast from 'services/hooks/useToast';

import { APIResponse } from 'services/api/base';

export interface RouteError {
	data: Partial<APIResponse.Error>;
}

function ErrorBoundary(): ReactElement {
	const { createMessageToast } = useToast();
	const { data } = useRouteError() as RouteError;

	useEffect(() => createMessageToast({
		message: data.message ?? gettext('Произошла непредвиденная ошибка!'),
		level: 'danger',
	}), []);

	return <Loading size='xl' className='m-auto' />;
}

export default ErrorBoundary;