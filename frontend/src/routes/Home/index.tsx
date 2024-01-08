import './index.css';

import React, { ReactElement } from 'react';
import { json } from 'react-router-dom';

import Container from 'react-bootstrap/Container';

import Header from './components/Header';
import Stats from './components/Stats';
import Donations from './components/Donations';

import { DonationsAPI } from 'services/api/donations/main';
import { APIResponse } from 'services/api/donations/types';

export interface LoaderData {
	donations: APIResponse.DonationsAPI.Get;
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
		<main className='my-auto'>
			<Container className='vstack align-items-center text-center gap-3 gap-lg-4 my-3 my-lg-4'>
				<Header />
				<Stats />
				<Donations />
			</Container>
		</main>
	);
}

export default Home;