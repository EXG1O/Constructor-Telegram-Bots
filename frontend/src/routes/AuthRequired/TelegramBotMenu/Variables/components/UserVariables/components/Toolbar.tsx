import React, { ReactElement, HTMLAttributes, memo, useCallback } from 'react';
import classNames from 'classnames';

import Search, { defaultValue as searchDefaultValue } from 'components/Search';
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
		<div {...props} className={classNames('row row-cols-md-auto g-2', className)}>
			<div>
				<AddVariableButton className='w-100' />
			</div>
			<Search
				size='sm'
				className='flex-fill'
				onSearch={useCallback(value => updateVariables(undefined, undefined, value), [])}
				onClear={useCallback(() => updateVariables(undefined, undefined, searchDefaultValue), [])}
			/>
			<Pagination
				itemCount={paginationData.count}
				itemLimit={paginationData.limit}
				itemOffset={paginationData.offset}
				size='sm'
				className='justify-content-center ps-1'
				onPageChange={useCallback(newOffset => updateVariables(undefined, newOffset), [updateVariables])}
			/>
		</div>
	);
}

export default memo(Toolbar);