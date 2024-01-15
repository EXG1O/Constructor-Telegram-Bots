import React, { ReactElement } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import './index.css';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Stack from 'react-bootstrap/Stack';

import { TeamMembersAPI } from 'services/api/team/main';
import { TeamMember } from 'services/api/team/types';

export interface LoaderData {
	members: TeamMember[];
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
						<Stack key={member.id} gap={1} className='align-items-center'>
							<img src={member.image} className='img-team-member' />
							<a
								className='h5 link-dark link-underline-opacity-0 fw-semibold mb-0'
								href={`tg://resolve?domain=${member.username}`}
							>
								@{member.username}
							</a>
							<span>{member.speciality}</span>
						</Stack>
					))}
				</Row>
			</Container>
		</main>
	);
}

export default Team;