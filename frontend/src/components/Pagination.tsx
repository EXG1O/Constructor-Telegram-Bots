import React, { ElementType, HTMLAttributes, ReactElement, ReactNode, useEffect, useState } from 'react';
import classNames from 'classnames';

import RBPagination, { PaginationProps as RBPaginationProps } from 'react-bootstrap/Pagination';

export interface PaginationProps extends Omit<RBPaginationProps, 'children'> {
	itemCount: number;
	itemLimit: number;
	itemOffset: number;
	onPageChange: (newItemOffset: number) => void;
}

export interface PaginationItemProps<As extends ElementType = ElementType> extends HTMLAttributes<As> {
	as?: As;
	active?: boolean;
}

export function PaginationItem({ as: Component = 'button', active, children, ...props }: PaginationItemProps): ReactElement<PaginationItemProps> {
	return (
		<li className={classNames('page-item', active ? 'active' : undefined)}>
			<Component {...props} className={classNames('page-link', props.className)}>
				{children}
			</Component>
		</li>
	);
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
							<PaginationItem
								key={num}
								{...(
									activePageNum === num ? {
										active: true,
									} : {
										onClick: () => onPageChange((num - 1) * itemLimit),
									}
								)}
							>
								{num}
							</PaginationItem>
						);
					} else if (num === 2 || num === pageCount - 2) {
						return (
							<PaginationItem
								key={num}
								as='span'
								style={{ cursor: 'default' }}
							>
								...
							</PaginationItem>
						);
					}
				})
			) : []
		);
	}, [itemCount, itemLimit, itemOffset]);

	return (
		items.length ? (
			<RBPagination {...props}>
				{items}
			</RBPagination>
		) : <></>
	);
}

export default Object.assign(Pagination, { Item: PaginationItem });