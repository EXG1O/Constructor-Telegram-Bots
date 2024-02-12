import React, { ReactElement, ReactNode, AnchorHTMLAttributes } from 'react';
import classNames from 'classnames';

export interface DefaultLinkProps extends AnchorHTMLAttributes<HTMLAnchorElement> {
	href: string;
	children: ReactNode;
}

function DefaultLink(props: DefaultLinkProps): ReactElement<DefaultLinkProps> {
	return (
		<a
			target='_blank'
			{...props}
			className={
				classNames(
					'link-secondary link-underline-opacity-0',
					props.className,
				)
			}
		/>
	);
}

export default DefaultLink;