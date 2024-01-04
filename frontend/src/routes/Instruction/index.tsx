import React, { ReactNode } from 'react';
import { useLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';

import { InstructionSectionsAPI } from 'services/api/instruction/main';
import { InstructionSection } from 'services/api/instruction/types';

export interface LoaderData {
	sections: InstructionSection[];
}

export async function loader(): Promise<LoaderData> {
	const response = await InstructionSectionsAPI.get();

	return { sections: response.ok ? response.json : [] };
}

function Instruction(): ReactNode {
	const { sections } = useLoaderData() as LoaderData;

	return (
		<main className='my-auto'>
			<Container className='my-3 my-lg-4'>
				{sections.map(section => (
					<div key={section.id}>
						<h3 className='mb-1'>{section.title}</h3>
						<div dangerouslySetInnerHTML={{ __html: section.text }} />
					</div>
				))}
			</Container>
		</main>
	);
}

export default Instruction;