import React, { ReactNode } from 'react';

import { LinkContainer } from 'react-router-bootstrap';
import Stack from 'react-bootstrap/Stack';
import Table from 'react-bootstrap/Table';
import Button from 'react-bootstrap/Button';

import { Donation } from 'services/api/donations/types';

interface DonationsProps {
	donations: Donation[];
}

function Donations({ donations }: DonationsProps): ReactNode {
	return (
		<Stack className='donations align-self-center' gap={2}>
			<h3 className='mb-0'>{gettext('Список пожертвований')}</h3>
			<div className='bg-light border rounded'>
				<Table variant='light' className='overflow-hidden border-bottom rounded align-middle mb-0'>
					<thead>
						<tr>
							<th className='sum' scope='col'>{gettext('Сумма')}</th>
							<th scope='col'>Telegram</th>
							<th className='date' scope='col'>{gettext('Дата')}</th>
						</tr>
					</thead>
					<tbody className='table-group-divider'>
						{donations.length ? (
							donations.map(donation => (
								<tr key={donation.id}>
									<td className='sum'>{donation.sum}€</td>
									<td>
										<a
											className='link-dark link-underline-opacity-0 text-break'
											href={donation.telegram_url}
											target='_blank'
										>
											{donation.telegram_url}
										</a>
									</td>
									<td className='date'>{donation.date}</td>
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
				<Button variant='success' className='align-self-center'>{gettext('Поддержать разработчика')}</Button>
			</LinkContainer>
		</Stack>
	);
}

export default Donations;