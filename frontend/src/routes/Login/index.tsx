import React, { ReactElement, useEffect } from 'react';
import { Params, NavigateOptions, useNavigate, useRouteLoaderData } from 'react-router-dom';

import Loading from 'components/Loading';

import useToast from 'services/hooks/useToast';

import { UserAPI } from 'services/api/users/main';

type Levels = 'success' | 'info' | 'error';

export interface LoaderData {
	message: string;
	level: Levels;
}

export async function loader({ params }: { params: Params<'userID' | 'confirmCode'> }): Promise<LoaderData> {
	const { userID, confirmCode } = params;

	let message: string;
	let level: Levels;

	if (userID && confirmCode) {
		const response = await UserAPI.login({
			user_id: Number.parseInt(userID),
			confirm_code: confirmCode,
		});

		message = response.json.message;
		level = response.json.level;
	} else {
		message = gettext('Неправильный URL-адрес!');
		level = 'error';
	}

	return { message, level };
}

function Login(): ReactElement {
	const navigate = useNavigate();
	const { message, level } = useRouteLoaderData('login') as LoaderData;

	const { createMessageToast } = useToast();

	useEffect(() => {
		const options: NavigateOptions = { replace: true };

		createMessageToast({ message, level });

		if (level === 'success') {
			navigate('/personal-cabinet/', options);
		} else {
			navigate('/', options);
		}
	}, []);

	return <Loading size='lg' className='m-auto' />;
}

export default Login;