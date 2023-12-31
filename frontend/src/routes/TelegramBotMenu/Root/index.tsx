import React, { ReactNode } from 'react';
import { Outlet } from 'react-router-dom';

import Container from 'react-bootstrap/Container';

import Header from './components/Header';

import AuthRequiredProvider from 'services/providers/AuthRequiredProvider';
import TelegramBotProvider from 'services/providers/TelegramBotProvider';

function Root(): ReactNode {
	return (
		<AuthRequiredProvider>
			<TelegramBotProvider>
				<main className='mb-auto'>
					<Container className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
						<Header />
						<Outlet />
					</Container>
				</main>
			</TelegramBotProvider>
		</AuthRequiredProvider>
	);
}

export default Root;