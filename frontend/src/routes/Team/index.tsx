import './index.css';

import React, { ReactElement } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Stack from 'react-bootstrap/Stack';

import { RouteError } from 'routes/ErrorBoundary';

import { TeamMembersAPI } from 'services/api/team/main';
import { TeamMember } from 'services/api/team/types';

export interface LoaderData {
	members: TeamMember[];
}

export async function loader(): Promise<LoaderData> {
	const response = await TeamMembersAPI.get();

	if (!response.ok) {
		throw json<RouteError['data']>(response.json, { status: response.status });
	}

	return { members: response.json };
}

function Team(): ReactElement {
	const { members } = useRouteLoaderData('team') as LoaderData;

	return (
		<main className='my-auto'>
			<Container className='text-center my-3 my-lg-4'>
				<Row xs={1} lg={5} className='justify-content-center g-3 g-lg-4'>
					{members.length ? (
						members.map(member => (
							<Stack key={member.id} className='align-items-center px-2'>
								<img className='border img-team-member' src={member.image}></img>
								<a
									className='h5 link-dark link-underline-opacity-0 fw-semibold'
									href={`tg://resolve?domain=${member.username}`}
								>
									@{member.username}
								</a>
								<span>{member.speciality}</span>
							</Stack>
						))
					) : undefined}
				</Row>
			</Container>
		</main>
	);
}

export default Team;