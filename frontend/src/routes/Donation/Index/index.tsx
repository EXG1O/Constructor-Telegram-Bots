import React, { ReactElement } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

import { RouteError } from 'routes/ErrorBoundary';

import { DonationSectionsAPI, DonationButtonsAPI } from 'services/api/donations/main';
import { DonationSection, DonationButton } from 'services/api/donations/types';

export interface LoaderData {
	sections: DonationSection[],
	buttons: DonationButton[],
}

export async function loader(): Promise<LoaderData> {
	const responses = [
		await DonationSectionsAPI.get(),
		await DonationButtonsAPI.get(),
	];

	for (const response of responses) {
		if (!response.ok) {
			throw json<RouteError['data']>(response.json, { status: response.status });
		}
	}

	return {
		sections: responses[0].json as DonationSection[],
		buttons: responses[1].json as DonationButton[],
	}
}

function Index(): ReactElement {
	const { sections, buttons } = useRouteLoaderData('donation-index') as LoaderData;

	return (
		<Container as='main' className='h-100 my-3 my-lg-4'>
			{sections.map(section => (
				<div key={section.id}>
					<h3 className='mb-1'>{section.title}</h3>
					<div dangerouslySetInnerHTML={{ __html: section.text }}></div>
				</div>
			))}
			<div className='d-flex gap-2'>
				{buttons.map(button => (
					<Button
						key={button.id}
						as='a'
						variant='dark'
						className='flex-fill'
						href={button.url}
						target='_blank'
					>
						{button.text}
					</Button>
				))}
			</div>
		</Container>
	);
}

export default Index;