import './App.css';

import React, { ReactNode } from 'react';
import { useLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';

import Header from './components/Header';
import Stats from './components/Stats';
import Donations from './components/Donations';

import { Donation } from 'services/api/donations/types';
import { DonationsAPI } from 'services/api/donations/main';

export interface LoaderData {
	donations: Donation[];
}

export async function loader(): Promise<LoaderData> {
	const response = await DonationsAPI.get({ limit: 50 });

	return { donations: (response.ok) ? response.json : [] };
}

function App(): ReactNode {
	const { donations } = useLoaderData() as LoaderData;

	return (
		<main className='my-auto'>
			<Container className='vstack align-items-center text-center gap-3 gap-lg-4 my-3 my-lg-4'>
				<Header />
				<Stats />
				<Donations donations={donations} />
			</Container>
		</main>
	);
}

export default App;