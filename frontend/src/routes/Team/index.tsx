import React, { ReactElement } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import './index.css';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import { TeamMembersAPI } from 'services/api/team/main';
import { APIResponse } from 'services/api/team/types';

export interface LoaderData {
	members: APIResponse.TeamMembersAPI.Get;
}

export async function loader(): Promise<LoaderData> {
	const response = await TeamMembersAPI.get();

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return { members: response.json };
}

function Team(): ReactElement {
	const { members } = useRouteLoaderData('team') as LoaderData;

	return (
		<main className='my-auto'>
			<Container className='text-center my-3 my-lg-4'>
				<Row xs={1} lg={5} className='justify-content-center g-3 g-lg-4'>
					{members.map(member => (
						<div key={member.id} className='d-flex flex-column align-items-center'>
							<img src={member.image} className='img-team-member mb-1' />
							<a
								className='h5 link-dark link-underline-opacity-0 fw-semibold mb-0'
								href={`tg://resolve?domain=${member.username}`}
							>
								{member.username}
							</a>
							<span>{member.speciality}</span>
						</div>
					))}
				</Row>
			</Container>
		</main>
	);
}

export default Team;