import React, { ReactNode } from 'react';
import { useLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import Button from 'react-bootstrap/Button';

import { DonationSectionsAPI, DonationButtonsAPI } from 'services/api/donations/main';
import { DonationSection, DonationButton } from 'services/api/donations/types';

export interface LoaderData {
	sections: DonationSection[],
	buttons: DonationButton[],
}

export async function loader(): Promise<LoaderData> {
	const response = await DonationSectionsAPI.get();
	const response_ = await DonationButtonsAPI.get();

	return {
		sections: response.ok ? response.json : [],
		buttons: response_.ok ? response_.json : [],
	}
}

function Index(): ReactNode {
	const { sections, buttons } = useLoaderData() as LoaderData;

	return (
		<main className='my-auto'>
			<Container className='my-3 my-lg-4'>
				{sections.map(section => (
					<div key={section.id}>
						<h3 className='mb-1'>{section.title}</h3>
						{section.text}
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
		</main>
	);
}

export default Index;