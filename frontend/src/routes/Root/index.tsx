import React, { ReactNode } from 'react';
import { Outlet } from 'react-router-dom';

import Header from 'components/Header';
import Footer from 'components/Footer';

import UserProvider from 'services/providers/UserProvider';
import ToastProvider from 'services/providers/ToastProvider';

function Root(): ReactNode {
	return (
		<UserProvider>
			<ToastProvider>
				<Header />
				<Outlet />
				<Footer />
			</ToastProvider>
		</UserProvider>
	);
}

export default Root;