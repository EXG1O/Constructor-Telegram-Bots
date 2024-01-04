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

	if (!response.ok) {
		throw new Response(gettext('Сервер вернул код ошибки!'), { status: response.status });
	}

	const response_ = await DonationButtonsAPI.get();

	if (!response_.ok) {
		throw new Response(gettext('Сервер вернул код ошибки!'), { status: response.status });
	}

	return { sections: response.json, buttons: response_.json };
}

function Index(): ReactNode {
	const { sections, buttons } = useLoaderData() as LoaderData;

	return (
		<main className='my-auto'>
			<Container className='my-3 my-lg-4'>
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
		</main>
	);
}

export default Index;