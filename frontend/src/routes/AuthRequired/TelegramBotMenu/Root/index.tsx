import React, { ReactNode } from 'react';
import { Outlet } from 'react-router-dom';

import Container from 'react-bootstrap/Container';

import Header from './components/Header';

import TelegramBotProvider from 'services/providers/TelegramBotProvider';

function Root(): ReactNode {
	return (
		<TelegramBotProvider>
			<Container as='main' className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
				<Header />
				<Outlet />
			</Container>
		</TelegramBotProvider>
	);
}

export default Root;