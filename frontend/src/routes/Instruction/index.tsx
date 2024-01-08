import React, { ReactElement } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';

import { InstructionSectionsAPI } from 'services/api/instruction/main';
import { InstructionSection } from 'services/api/instruction/types';

export interface LoaderData {
	sections: InstructionSection[];
}

export async function loader(): Promise<LoaderData> {
	const response = await InstructionSectionsAPI.get();

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return { sections: response.json };
}

function Instruction(): ReactElement {
	const { sections } = useRouteLoaderData('instruction') as LoaderData;

	return (
		<Container as='main' className='h-100 my-3 my-lg-4'>
			{sections.map(section => (
				<div key={section.id}>
					<h3 className='mb-1'>{section.title}</h3>
					<div dangerouslySetInnerHTML={{ __html: section.text }} />
				</div>
			))}
		</Container>
	);
}

export default Instruction;