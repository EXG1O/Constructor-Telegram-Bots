import React, { ReactElement, HTMLAttributes, memo } from 'react';
import classNames from 'classnames';

import Table from 'react-bootstrap/Table';

import VariableDisplay from './VariableDisplay';

import useVariables from '../hooks/useVariables';

export type VariableListProps = Omit<HTMLAttributes<HTMLDivElement>, 'children'>;

function VariableList({ className, ...props }: VariableListProps): ReactElement<VariableListProps> {
	const { variables } = useVariables();

	return (
		variables.length ? (
			<div {...props} className={classNames('border rounded', className)}>
				<Table
					responsive
					striped
					borderless
					className='overflow-hidden align-middle rounded mb-0'
				>
					<tbody>
						{variables.map(variable => (
							<VariableDisplay key={variable.id} variable={variable} />
						))}
					</tbody>
				</Table>
			</div>
		) : (
			<div className='border rounded text-center px-3 py-2'>
				{gettext('Вы ещё не добавили переменные')}
			</div>
		)
	);
}

export default memo(VariableList);