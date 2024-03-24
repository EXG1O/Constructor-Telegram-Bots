import React, { ReactElement, HTMLAttributes, memo } from 'react';
import classNames from 'classnames';

import Pagination from 'components/Pagination';

import AddVariableButton from './AddVariableButton';

import useVariables from '../hooks/useVariables';

import { UserVariablesPaginationData } from '../../..';

export interface ToolbarProps extends Omit<HTMLAttributes<HTMLDivElement>, 'children'> {
	paginationData: Omit<UserVariablesPaginationData, 'results'>;
}

function Toolbar({ paginationData, className, ...props }: ToolbarProps): ReactElement<ToolbarProps> {
	const { updateVariables } = useVariables();

	return (
		<div {...props} className={classNames('d-flex flex-wrap justify-content-between gap-2', className)}>
			<AddVariableButton />
			<Pagination
				itemCount={paginationData.count}
				itemLimit={paginationData.limit}
				itemOffset={paginationData.offset}
				size='sm'
				className='justify-content-center'
				onPageChange={newOffset => updateVariables(undefined, newOffset)}
			/>
		</div>
	);
}

export default memo(Toolbar);