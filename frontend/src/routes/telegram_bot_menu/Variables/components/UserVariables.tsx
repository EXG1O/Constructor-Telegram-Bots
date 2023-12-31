import React, { ReactElement, useState } from 'react';

import Card from 'react-bootstrap/Card';
import Table from 'react-bootstrap/Table';
import Spinner from 'react-bootstrap/Spinner';

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
					<Spinner
						animation='border'
						className='align-self-center'
						style={{
							width: '2.5rem',
							height: '2.5rem',
							borderWidth: '0.35rem',
						}}
					/>
				)}
			</Card.Body>
		</Card>
	);
}

export default UserVariables;