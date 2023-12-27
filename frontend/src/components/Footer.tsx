import React, { ReactNode, AnchorHTMLAttributes } from 'react';
import { Link } from 'react-router-dom';
import classNames from 'classnames';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

export type FooterLinkProps = AnchorHTMLAttributes<HTMLAnchorElement>;

const projectLinks: FooterLinkProps[] = [
	{ href: 'https://github.com/EXG1O/Constructor-Telegram-Bots', children: 'GitHub' },
	{ href: 'https://github.com/EXG1O/Constructor-Telegram-Bots/blob/master/LICENSE.md', children: 'License' },
];
const founderLinks: FooterLinkProps[] = [
	{ href: 'mailto:helper.exg1o@gmail.com', children: 'helper.exg1o@gmail.com' },
	{ href: 'https://github.com/EXG1O', children: 'GitHub' },
	{ href: 'tg://resolve?domain=exg1o', children: 'Telegram' },
	{ href: 'tg://resolve?domain=exg1o_channel', children: 'Telegram Channel' },
];

export function FooterLink(props: FooterLinkProps): ReactNode {
	return <a target='_blank' {...props} className={classNames('link-secondary link-underline-opacity-0', props.className)} />;
}

function Footer(): ReactNode {
	return (
		<footer className='text-bg-dark'>
			<Container>
				<Row className='justify-content-center text-center py-2'>
					<Col xs={12} lg={2} className='vstack'>
						<h5 className='mb-0'>{gettext('Проект')}</h5>
						{projectLinks.map((props, index) => (
							<FooterLink key={index} {...props} />
						))}
					</Col>
					<Col xs={12} lg={3} className='vstack my-1 my-lg-0'>
						<h5 className='mb-0'>{gettext('Контакты Основателя')}</h5>
						{founderLinks.map((props, index) => (
							<FooterLink key={index} {...props} />
						))}
					</Col>
					<Col xs={12} lg={2} className='vstack'>
						<h5 className='mb-0'>{gettext('Другое')}</h5>
						<Link className='link-secondary link-underline-opacity-0' to='/privacy-policy/'>Privacy Policy</Link>
					</Col>
					<Col as='hr' xs={11} lg={7} className='text-white-50 my-2' />
					<span>&copy; 2023 exg1o</span>
				</Row>
			</Container>
		</footer>
	);
}

export default Footer;