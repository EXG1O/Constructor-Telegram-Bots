import React, { ReactElement } from 'react';
import { Outlet, json, useNavigation } from 'react-router-dom';
import Cookies from 'js-cookie';

import Header from 'components/Header';
import Footer from 'components/Footer';
import Loading from 'components/Loading';

import ToastProvider from 'services/providers/ToastProvider';

import { UserAPI } from 'services/api/users/main';
import { User } from 'services/api/users/types';

import { LanguagesAPI } from 'services/api/languages/main';
import { APIResponse } from 'services/api/languages/types';

export interface Languages {
	current: string;
	available: APIResponse.LanguagesAPI.Get;
}

export interface LoaderData {
	user: User | null;
	languages: Languages;
}

export async function loader(): Promise<LoaderData> {
	const authToken = Cookies.get('auth-token');
	let user: LoaderData['user'] = null;

	if (authToken !== undefined) {
		try {
			const response = await UserAPI.get();

			if (response.ok) {
				user = response.json;
			} else {
				Cookies.remove('auth-token');
			}
		} catch {};
	}

	const response = await LanguagesAPI.get();

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return {
		user,
		languages: {
			current: Cookies.get('lang') ?? 'ru',
			available: response.json,
		},
	}
}

function Root(): ReactElement {
	const navigation = useNavigation();

	return (
		<ToastProvider>
			<Header />
			{navigation.state === 'loading' ? (
				<Loading size='lg' className='m-auto' />
			) : (
				<Outlet />
			)}
			<Footer />
		</ToastProvider>
	);
}

export default Root;