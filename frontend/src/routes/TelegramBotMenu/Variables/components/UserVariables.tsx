import React, { ReactElement, useState } from 'react';

import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';

import Loading from 'components/Loading';

function UserVariables(): ReactElement {
	const [variables, setVariables] = useState(undefined);

	return (
		<Card className='border'>
			<Card.Header as='h5' className='border-bottom text-center'>
				{gettext('Пользовательские переменные')}
			</Card.Header>
			<Card.Body className='vstack gap-2'>
				{variables !== undefined ? (
					<div className='border rounded'>
						<Table responsive borderless striped className='overflow-hidden rounded mb-0'>
							<tbody></tbody>
						</Table>
					</div>
				) : (
					<Loading size='md' className='align-self-center' />
				)}
			</Card.Body>
		</Card>
	);
}

export default UserVariables;