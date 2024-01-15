import React, { ReactElement } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import { LinkContainer } from 'react-router-bootstrap';
import Stack from 'react-bootstrap/Stack';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';

import { LoaderData as HomeLoaderData } from '..';

function Donations(): ReactElement {
	const { donations } = useRouteLoaderData('home') as HomeLoaderData;

	return (
		<Stack gap={2} className='donations align-self-center'>
			<h3 className='mb-0'>{gettext('Список пожертвований')}</h3>
			<div className='border rounded'>
				<Table
					responsive
					striped
					borderless
					className='overflow-hidden align-middle rounded mb-0'
				>
					<thead className='border-bottom'>
						<tr>
							<th scope='col' style={{ width: '30%' }}>{gettext('Сумма')}</th>
							<th scope='col' style={{ width: '40%' }}>Telegram</th>
							<th scope='col' style={{ width: '30%' }}>{gettext('Дата')}</th>
						</tr>
					</thead>
					<tbody>
						{donations.count ? (
							donations.results.map(donation => (
								<tr key={donation.id}>
									<td>{donation.sum}€</td>
									<td>
										<a
											className='link-dark link-underline-opacity-0'
											href={donation.telegram_url}
											target='_blank'
										>
											{donation.telegram_url}
										</a>
									</td>
									<td>{donation.date}</td>
								</tr>
							))
						) : (
							<tr>
								<td colSpan={3}>{gettext('Ещё не было сделано пожертвований')}</td>
							</tr>
						)}
					</tbody>
				</Table>
			</div>
			<LinkContainer to='/donation/'>
				<Button
					variant='success'
					className='align-self-center'
				>
					{gettext('Поддержать разработчика')}
				</Button>
			</LinkContainer>
		</Stack>
	);
}

export default Donations;