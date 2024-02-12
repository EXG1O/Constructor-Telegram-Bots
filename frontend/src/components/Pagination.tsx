import React, { ReactElement, ReactNode, memo, useEffect, useState } from 'react';

import _Pagination, { PaginationProps as _PaginationProps } from 'react-bootstrap/Pagination';

export interface PaginationProps extends Omit<_PaginationProps, 'children'> {
	itemCount: number;
	itemLimit: number;
	itemOffset: number;
	onPageChange: (newItemOffset: number) => void;
}

function Pagination({ itemCount, itemLimit, itemOffset, onPageChange, ...props }: PaginationProps): ReactElement<PaginationProps> {
	const [items, setItems] = useState<ReactNode[]>([]);

	useEffect(() => {
		const pageCount: number = Math.ceil(itemCount / itemLimit);
		const activePageNum: number = Math.ceil(itemOffset / itemLimit) + 1;

		setItems(
			pageCount > 1 ? (
				Array.from({ length: pageCount }, (_, num) => {
					num++;

					if (
						pageCount <= 7 ||
						num === 1 || num === pageCount ||
						num <= 5 && activePageNum <= 5 && activePageNum !== 5 ||
						num >= pageCount - 4 && activePageNum >= pageCount - 4 && activePageNum !== pageCount - 4 ||
						num >= activePageNum - 1 && num <= activePageNum + 1
					) {
						return (
							<_Pagination.Item
								key={num}
								as='span'
								{...(
									activePageNum === num ? {
										active: true,
									} : {
										onClick: () => onPageChange((num - 1) * itemLimit),
									}
								)}
								style={{ cursor: 'pointer' }}
							>
								{num}
							</_Pagination.Item>
						);
					} else if (num === 2 || num === pageCount - 2) {
						return (
							<_Pagination.Ellipsis
								key={num}
								style={{
									cursor: 'default',
									pointerEvents: 'none',
								}}
							/>
						);
					}
				})
			) : []
		);
	}, [itemCount, itemLimit, itemOffset]);

	return (
		items.length ? (
			<_Pagination {...props}>
				{items}
			</_Pagination>
		) : <></>
	);
}

export default memo(Pagination);