import React, { ReactElement, useState } from 'react';
import { json, useRouteLoaderData } from 'react-router-dom';

import './index.scss';

import Container from 'react-bootstrap/Container';

import Loading from 'components/Loading';
import Pagination from 'components/Pagination';

import useToast from 'services/hooks/useToast';

import { UpdatesAPI } from 'services/api/updates/main';
import { APIResponse } from 'services/api/updates/types';

export interface UpdatesPaginationData extends Omit<APIResponse.UpdatesAPI.Get.Pagination, 'next' | 'previous'> {
	limit: number;
	offset: number;
}

export interface LoaderData {
	updatesPaginationData: UpdatesPaginationData;
}

export async function loader(): Promise<LoaderData> {
	const [limit, offset] = [3, 0]

	const response = await UpdatesAPI.get(limit, offset);

	if (!response.ok) {
		throw json(response.json, { status: response.status });
	}

	return {
		updatesPaginationData: {
			count: response.json.count,
			limit,
			offset,
			results: response.json.results,
		}
	}
}

function Updates(): ReactElement {
	const { updatesPaginationData: initialPaginationData } = useRouteLoaderData('updates') as LoaderData;

	const { createMessageToast } = useToast();

	const [paginationData, setPaginationData] = useState<UpdatesPaginationData>(initialPaginationData);
	const [loading, setLoading] = useState<boolean>(false);

	async function updateUpdates(limit?: number, offset?: number): Promise<void> {
		setLoading(true);

		limit ??= paginationData.limit;
		offset ??= paginationData.offset;

		const response = await UpdatesAPI.get(limit, offset);

		if (response.ok) {
			setPaginationData({
				count: response.json.count,
				limit,
				offset,
				results: response.json.results,
			});
			setLoading(false);
		} else {
			createMessageToast({ message: response.json.message, level: response.json.level });
		}
	}

	return (
		<Container as='main' className='vstack gap-3 gap-lg-4 my-3 my-lg-4'>
			{!loading ? (
				paginationData.results.map(update => (
					<div
						key={update.id}
						className='update-block border rounded p-3'
						dangerouslySetInnerHTML={{ __html: update.description }}
					/>
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
	);
}

export default Updates;