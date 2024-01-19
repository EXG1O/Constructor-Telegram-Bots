import React, { ElementType, HTMLAttributes, ReactElement, ReactNode, useEffect, useState } from 'react';
import classNames from 'classnames';

import RBPagination, { PaginationProps as RBPaginationProps } from 'react-bootstrap/Pagination';

export interface PaginationProps extends Omit<RBPaginationProps, 'children'> {
	count: number;
	limit: number;
	offset: number;
	onPageChange: (offset: number) => void;
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

function Pagination({ count, limit, offset, onPageChange, ...props }: PaginationProps): ReactElement<PaginationProps> {
	const [items, setItems] = useState<ReactNode[]>([]);

	useEffect(() => {
		const pagesCount: number = Math.ceil(count / limit);
		const activePageNum: number = Math.ceil(offset / limit) + 1;

		setItems(
			pagesCount > 1 ? (
				Array.from({ length: pagesCount }, (_, num) => {
					num++;

					if (
						pagesCount <= 7 ||
						num === 1 || num === pagesCount ||
						num <= 5 && activePageNum <= 5 && activePageNum !== 5 ||
						num >= pagesCount - 4 && activePageNum >= pagesCount - 4 && activePageNum !== pagesCount - 4 ||
						num >= activePageNum - 1 && num <= activePageNum + 1
					) {
						return (
							<PaginationItem
								key={num}
								{...(
									activePageNum === num ? {
										active: true,
									} : {
										onClick: () => onPageChange((num - 1) * limit),
									}
								)}
							>
								{num}
							</PaginationItem>
						);
					} else if (num === 2 || num === pagesCount - 2) {
						return (
							<PaginationItem key={num} as='span' style={{ cursor: 'default' }}>
								...
							</PaginationItem>
						);
					}
				})
			) : []
		);
	}, [count, limit, offset]);

	return (
		items.length ? (
			<RBPagination {...props}>
				{items}
			</RBPagination>
		) : <></>
	);
}

export default Object.assign(Pagination, { Item: PaginationItem });