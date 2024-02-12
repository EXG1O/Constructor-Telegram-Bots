import React, { ReactElement } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

import Section from './components/Section';
import Title from 'components/Title';

import { DonationSectionsAPI, DonationButtonsAPI } from 'services/api/donations/main';
import { APIResponse } from 'services/api/donations/types';

export interface LoaderData {
	sections: APIResponse.DonationSectionsAPI.Get,
	buttons: APIResponse.DonationButtonsAPI.Get,
}

export async function loader(): Promise<LoaderData> {
	const responses = [
		await DonationSectionsAPI.get(),
		await DonationButtonsAPI.get(),
	];

	for (const response of responses) {
		if (!response.ok) {
			throw json(response.json, { status: response.status });
		}
	}

	return {
		sections: responses[0].json as APIResponse.DonationSectionsAPI.Get,
		buttons: responses[1].json as APIResponse.DonationButtonsAPI.Get,
	}
}

const title: string = gettext('Пожертвование');

function Index(): ReactElement {
	const { sections, buttons } = useRouteLoaderData('donation-index') as LoaderData;

	return (
		<Title title={title}>
			<Container as='main' className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
				<h1 className='fw-semibold text-center mb-0'>{title}</h1>
				{sections.map(section => (
					<Section key={section.id} section={section} />
				))}
				<div className='d-flex gap-2 mt-auto'>
					{buttons.map(button => (
						<Button
							key={button.id}
							as='a'
							href={button.url}
							target='_blank'
							variant='dark'
							className='flex-fill'
						>
							{button.text}
						</Button>
					))}
				</div>
			</Container>
		</Title>
	);
}

export default Index;