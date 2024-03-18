import React, { ReactElement, ReactNode, memo } from 'react';
import { Link, LinkProps as _LinkProps, useLocation } from 'react-router-dom';
import classNames from 'classnames';

import Nav, { NavProps } from 'react-bootstrap/Nav';

export type LinksProps = Omit<NavProps, 'variant' | 'children'>;

export interface LinkProps extends _LinkProps {
	children: ReactNode;
}

const links: LinkProps[] = [
	{ to: '/', children: gettext('Главная') },
	{ to: '/team/', children: gettext('Команда') },
	{ to: '/updates/', children: gettext('Обновления') },
	{ to: '/instruction/', children: gettext('Инструкция') },
	{ to: '/donation/', children: gettext('Пожертвование') },
];

function Links(props: LinksProps): ReactElement<LinksProps> {
	const location = useLocation();

	return (
		<Nav
			{...props}
			variant='underline'
			className={classNames('gap-0', props.className)}
		>
			{links.map((props, index) => (
				<Link
					key={index}
					{...props}
					className={
						classNames(
							'nav-link pb-1',
							location.pathname === props.to ? 'active' : undefined,
							props.className,
						)
					}
				/>
			))}
		</Nav>
	);
}

export default memo(Links);