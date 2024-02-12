import React, { ReactElement } from 'react';
import { json } from 'react-router-dom';

import Container from 'react-bootstrap/Container';

import Title from 'components/Title';
import Header from './components/Header';
import Stats from './components/Stats';
import Donations from './components/Donations';

import { DonationsAPI } from 'services/api/donations/main';
import { APIResponse } from 'services/api/donations/types';

export interface LoaderData {
	donations: APIResponse.DonationsAPI.Get.Pagination;
}

export async function loader(): Promise<LoaderData> {
	const response = await DonationsAPI.get(20);

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return { donations: response.json };
}

function Home(): ReactElement {
	return (
		<Title title={gettext('Бесплатный конструктор Telegram ботов')}>
			<main className='my-auto'>
				<Container className='vstack justify-content-center align-items-center text-center gap-3 my-3 my-lg-4'>
					<Header />
					<Stats />
					<Donations />
				</Container>
			</main>
		</Title>
	);
}

export default Home;