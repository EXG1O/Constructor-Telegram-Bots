import React, { ReactNode } from 'react';

import Button from 'react-bootstrap/Button';

export interface TableCellProps {
	header: ReactNode;
	data: ReactNode;
}

function TableCell({ header, data }: TableCellProps): ReactNode {
	return (
		<tr>
			<th>
				<div className='d-flex gap-2'>
					<Button
						variant='light'
						className='btn-clipboard bi bi-clipboard border px-2 py-0 my-auto'
						data-clipboard-text={data}
					/>
					<span className='flex-fill'>{header}:</span>
				</div>
			</th>
			<td>{data}</td>
		</tr>
	);
}

export default TableCell;