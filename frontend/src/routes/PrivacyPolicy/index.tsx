import React, { ReactElement } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import './index.scss';

import Container from 'react-bootstrap/Container';

import { PrivacyPolicySectionsAPI } from 'services/api/privacy_policy/main';
import { APIResponse } from 'services/api/privacy_policy/types';

export interface LoaderData {
	sections: APIResponse.PrivacyPolicySectionsAPI.Get;
}

export async function loader(): Promise<LoaderData> {
	const response = await PrivacyPolicySectionsAPI.get();

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return { sections: response.json };
}

function PrivacyPolicy(): ReactElement {
	const { sections } = useRouteLoaderData('privacy-policy') as LoaderData;

	return (
		<Container as='main' className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
			{sections.map(section => (
				<div key={section.id} className='privacy-policy-section'>
					<h3 className='mb-1'>{section.title}</h3>
					<div dangerouslySetInnerHTML={{ __html: section.text }} />
				</div>
			))}
		</Container>
	);
}

export default PrivacyPolicy;