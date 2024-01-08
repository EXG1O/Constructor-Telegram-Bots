import React, { ReactElement } from 'react';
import { Outlet, useNavigation } from 'react-router-dom';
import Cookies from 'js-cookie';

import Header from 'components/Header';
import Footer from 'components/Footer';
import Loading from 'components/Loading';

import ToastProvider from 'services/providers/ToastProvider';

import { UserAPI } from 'services/api/users/main';
import { User } from 'services/api/users/types';

export interface LoaderData {
	user: User | null;
}

export async function loader(): Promise<LoaderData> {
	const authToken = Cookies.get('auth-token');

	if (authToken !== undefined) {
		try {
			const response = await UserAPI.get();

			if (response.ok) {
				return { user: response.json };
			} else {
				Cookies.remove('auth-token');
			}
		} catch {};
	}

	return { user: null };
}

function Root(): ReactElement {
	const navigation = useNavigation();

	return (
		<ToastProvider>
			<Header />
			{navigation.state === 'loading' ? (
				<Loading size='xl' className='m-auto' />
			) : (
				<Outlet />
			)}
			<Footer />
		</ToastProvider>
	);
}

export default Root;