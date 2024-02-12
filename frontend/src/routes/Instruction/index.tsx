import React, { ReactElement } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';

import { InstructionSectionsAPI } from 'services/api/instruction/main';
import { APIResponse } from 'services/api/instruction/types';
import Title from 'components/Title';
import Section from './components/Section';

export interface LoaderData {
	sections: APIResponse.InstructionSectionsAPI.Get;
}

export async function loader(): Promise<LoaderData> {
	const response = await InstructionSectionsAPI.get();

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return { sections: response.json };
}

const title: string = gettext('Инструкция');

function Instruction(): ReactElement {
	const { sections } = useRouteLoaderData('instruction') as LoaderData;

	return (
		<Title title={title}>
			<Container as='main' className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
				<h1 className='fw-semibold text-center mb-0'>{title}</h1>
				{sections.map(section => (
					<Section key={section.id} section={section} />
				))}
			</Container>
		</Title>
	);
}

export default Instruction;