import React, { ReactElement, ReactNode, HTMLAttributes } from 'react';
import classNames from 'classnames';

import Col from 'react-bootstrap/Col';

import DefaultLink, { DefaultLinkProps as _DefaultLinkProps } from './DefaultLink';
import ReactLink, { ReactLinkProps as _ReactLinkProps } from './ReactLink';

interface DefaultLinkProps extends _DefaultLinkProps {
	type: 'default';
}

interface ReactLinkProps extends _ReactLinkProps {
	type: 'react';
}

type Link = DefaultLinkProps | ReactLinkProps;

export interface LinksBlockProps extends Omit<HTMLAttributes<HTMLDivElement>, 'title'> {
	title: ReactNode;
	links: Link[];
}

function LinksBlock({ title, links, className, ...props }: LinksBlockProps): ReactElement<LinksBlockProps> {
	return (
		<Col {...props} className={classNames('vstack', className)}>
			<h5 className='mb-0'>{title}</h5>
			{links.map((props, index) => {
				if (props.type === 'default') {
					return <DefaultLink key={index} {...props} />;
				} else if (props.type === 'react') {
					return <ReactLink key={index} {...props} />;
				}
			})}
		</Col>
	);
}

export default LinksBlock;