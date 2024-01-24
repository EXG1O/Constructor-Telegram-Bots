import React, { ReactElement } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import './index.scss';

import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

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

function Index(): ReactElement {
	const { sections, buttons } = useRouteLoaderData('donation-index') as LoaderData;

	return (
		<Container as='main' className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
			{sections.map(section => (
				<div key={section.id} className='donation-section'>
					<h3 className='mb-1'>{section.title}</h3>
					<div dangerouslySetInnerHTML={{ __html: section.text }} />
				</div>
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
	);
}

export default Index;