import React, { ReactElement } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';

import Title from 'components/Title';

import Member from './components/Member';

import { MembersAPI } from 'services/api/team/main';
import { APIResponse } from 'services/api/team/types';

export interface LoaderData {
	members: APIResponse.MembersAPI.Get;
}

export async function loader(): Promise<LoaderData> {
	const response = await MembersAPI.get();

	if (!response.ok) {
		throw json(response.json, response.status);
	}

	return { members: response.json };
}

const title: string = gettext('Команда');

function Team(): ReactElement {
	const { members } = useRouteLoaderData('team') as LoaderData;

	return (
		<Title title={title}>
			<main className='my-auto'>
				<Container className='vstack text-center gap-3 gap-lg-4'>
					<h1 className='fw-semibold mb-0'>{title}</h1>
					<Row xs={1} lg={6} className='justify-content-center g-3 g-lg-4'>
						{members.map(member => (
							<Member key={member.id} member={member} />
						))}
					</Row>
				</Container>
			</main>
		</Title>
	);
}

export default Team;