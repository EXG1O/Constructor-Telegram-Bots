import React, { ReactElement, ReactNode, memo, useEffect, useState } from 'react';

import _Pagination, { PaginationProps as _PaginationProps } from 'react-bootstrap/Pagination';

export interface PaginationProps extends Omit<_PaginationProps, 'children'> {
	itemCount: number;
	itemLimit: number;
	itemOffset: number;
	onPageChange: (newItemOffset: number) => void;
}

function Pagination({
	itemCount,
	itemLimit,
	itemOffset,
	onPageChange,
	...props
}: PaginationProps): ReactElement<PaginationProps> {
	const [items, setItems] = useState<ReactNode[]>([]);

	useEffect(() => {
		const pageCount: number = Math.ceil(itemCount / itemLimit);
		const activePageNum: number = Math.ceil(itemOffset / itemLimit) + 1;

		setItems(
			pageCount > 1 ? (
				Array.from({ length: pageCount }, (_, pageNum) => {
					pageNum++;

					if (
						pageCount <= 7 ||
						pageNum === 1 || pageNum === pageCount ||
						pageNum <= 5 && activePageNum <= 5 && activePageNum !== 5 ||
						pageNum >= pageCount - 4 && activePageNum >= pageCount - 4 && activePageNum !== pageCount - 4 ||
						pageNum >= activePageNum - 1 && pageNum <= activePageNum + 1
					) {
						return (
							<_Pagination.Item
								key={pageNum}
								as='span'
								{...(
									activePageNum === pageNum ? {
										active: true,
									} : {
										onClick: () => onPageChange((pageNum - 1) * itemLimit),
									}
								)}
								style={{ cursor: 'pointer' }}
							>
								{pageNum}
							</_Pagination.Item>
						);
					} else if (pageNum === 2 || pageNum === pageCount - 2) {
						return (
							<_Pagination.Ellipsis
								key={pageNum}
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