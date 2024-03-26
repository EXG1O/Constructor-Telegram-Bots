import React, { ReactElement, useState } from 'react';
import { useRouteLoaderData } from 'react-router-dom';

import Container from 'react-bootstrap/Container';

import Title from 'components/Title';
import Loading from 'components/Loading';
import Pagination from 'components/Pagination';

import Update from './components/Update';

import useToast from 'services/hooks/useToast';

import { UpdatesAPI } from 'services/api/updates/main';
import { APIResponse } from 'services/api/updates/types';

export interface UpdatesPaginationData extends APIResponse.UpdatesAPI.Get.Pagination {
	limit: number;
	offset: number;
}

export interface LoaderData {
	updatesPaginationData: UpdatesPaginationData;
}

export async function loader(): Promise<LoaderData> {
	const [limit, offset] = [3, 0];

	const response = await UpdatesAPI.get(limit, offset);

	if (!response.ok) {
		throw Error('Failed to fetch data!');
	}

	return { updatesPaginationData: { ...response.json, limit, offset } };
}

const title: string = gettext('Обновления');

function Updates(): ReactElement {
	const { updatesPaginationData: initialPaginationData } = useRouteLoaderData('updates') as LoaderData;

	const { createMessageToast } = useToast();

	const [paginationData, setPaginationData] = useState<UpdatesPaginationData>(initialPaginationData);
	const [loading, setLoading] = useState<boolean>(false);

	async function updateUpdates(
		limit: number = paginationData.limit,
		offset: number = paginationData.offset,
	): Promise<void> {
		setLoading(true);

		const response = await UpdatesAPI.get(limit, offset);

		if (response.ok) {
			setPaginationData({ ...response.json, limit, offset });
		} else {
			createMessageToast({
				message: gettext('Не удалось получить список обновлений!'),
				level: 'error',
			});
		}

		setLoading(false);
	}

	return (
		<Title title={title}>
			<Container as='main' className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
				<h1 className='fw-semibold text-center mb-0'>{title}</h1>
				{!loading ? (
					paginationData.results.map(update => (
						<Update key={update.id} update={update} />
					))
				) : (
					<Loading size='lg' className='m-auto' />
				)}
				<Pagination
					itemCount={paginationData.count}
					itemLimit={paginationData.limit}
					itemOffset={paginationData.offset}
					className='align-self-center'
					onPageChange={newItemOffset => updateUpdates(undefined, newItemOffset)}
				/>
			</Container>
		</Title>
	);
}

export default Updates;