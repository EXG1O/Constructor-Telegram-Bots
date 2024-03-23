import React, { ReactElement, HTMLAttributes, memo } from 'react';
import classNames from 'classnames';

import Pagination, { PaginationProps } from 'components/Pagination';

import AddVariableButton, { AddVariableButtonProps } from './AddVariableButton';

import { UserVariablesPaginationData } from '../../..';

export interface ToolbarProps extends Omit<HTMLAttributes<HTMLDivElement>, 'children'>, Pick<PaginationProps, 'onPageChange'> {
	paginationData: Omit<UserVariablesPaginationData, 'results'>;
	onVariableCreated: AddVariableButtonProps['onCreated'];
}

function Toolbar({ paginationData, className, onVariableCreated, onPageChange, ...props }: ToolbarProps): ReactElement<ToolbarProps> {
	return (
		<div {...props} className={classNames('d-flex flex-wrap justify-content-between gap-2', className)}>
			<AddVariableButton onCreated={onVariableCreated} />
			<Pagination
				itemCount={paginationData.count}
				itemLimit={paginationData.limit}
				itemOffset={paginationData.offset}
				size='sm'
				className='justify-content-center'
				onPageChange={onPageChange}
			/>
		</div>
	);
}

export default memo(Toolbar);