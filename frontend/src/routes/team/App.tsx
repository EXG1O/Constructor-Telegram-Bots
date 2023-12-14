import './App.css';

import React, { ReactNode } from 'react';
import { useLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Stack from 'react-bootstrap/Stack';

import { TeamMembersAPI } from 'services/api/team/main';
import { TeamMember } from 'services/api/team/types';

export interface LoaderData {
	teamMembers: TeamMember[];
}

export async function loader(): Promise<LoaderData> {
	const response = await TeamMembersAPI.get();

	return { teamMembers: response.ok ? response.json : [] };
}

function App(): ReactNode {
	const { teamMembers } = useLoaderData() as LoaderData;

	return (
		<main className='my-auto'>
			<Container className='text-center my-3 my-lg-4'>
				<Row xs={1} lg={5} className='justify-content-center g-3 g-lg-4'>
					{teamMembers.length ? (
						teamMembers.map(teamMember => (
							<Stack key={teamMember.id} className='align-items-center px-2'>
								<img className='border img-team-member' src={teamMember.image}></img>
								<a
									className='h5 link-dark link-underline-opacity-0 fw-semibold'
									href={`tg://resolve?domain=${teamMember.username}`}
								>
									@{teamMember.username}
								</a>
								<span>{teamMember.speciality}</span>
							</Stack>
						))
					) : (
						<></>
					)}
				</Row>
			</Container>
		</main>
	);
}

export default App;