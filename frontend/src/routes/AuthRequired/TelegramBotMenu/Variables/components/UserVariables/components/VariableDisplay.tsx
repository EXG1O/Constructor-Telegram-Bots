import React, { ReactElement, memo } from 'react';

import EditVariableButton from './EditVariableButton';
import DeleteVariableButton from './DeleteVariableButton';

import { Variable } from 'services/api/telegram_bots/types';

export interface VariableDisplayProps {
	variable: Variable;
}

function VariableDisplay({ variable }: VariableDisplayProps): ReactElement<VariableDisplayProps> {
	return(
		<tr>
			<td className='w-50'>
				<div className='d-flex gap-2'>
					<i
						className='btn-clipboard bi bi-clipboard'
						data-clipboard-text={`{{ ${variable.name} }}`}
						style={{ cursor: 'pointer' }}
					/>
					<span className='flex-fill text-info-emphasis'>
						{variable.name}
					</span>
				</div>
			</td>
			<td>
				<div className='d-flex gap-2'>
					<span className='flex-fill text-nowrap'>
						{variable.description}
					</span>
					<div className='d-flex gap-1'>
						<EditVariableButton variable={variable} className='my-auto' />
						<DeleteVariableButton variable={variable} className='my-auto' />
					</div>
				</div>
			</td>
		</tr>
	);
}

export default memo(VariableDisplay);