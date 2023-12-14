import React, { ReactNode } from 'react';

import Button from 'react-bootstrap/Button';

export interface TableCellProps {
	header: ReactNode;
	data: string;
}

function TableCell({ header, data }: TableCellProps): ReactNode {
	return (
		<tr>
			<th>{header}:</th>
			<td>
				<div className="d-flex gap-2">
					<span className="flex-fill">{data}</span>
					<Button
						variant='secondary'
						className='btn-clipboard border bi bi-clipboard px-2 py-0'
						data-clipboard-text={data}
					/>
				</div>
			</td>
		</tr>
	);
}

export default TableCell;