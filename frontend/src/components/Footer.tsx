import React, { ReactNode } from 'react';
import { Link } from 'react-router-dom';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

function Footer(): ReactNode {
	return (
		<footer className='text-bg-dark'>
			<Container>
				<Row className='justify-content-center text-center py-2'>
					<Col xs={12} lg={2} className='vstack'>
						<h5 className='mb-0'>{gettext('Проект')}</h5>
						<a className='link-secondary link-underline-opacity-0' href='https://github.com/EXG1O/Constructor-Telegram-Bots' target='_blank'>GitHub</a>
						<a className='link-secondary link-underline-opacity-0' href='https://github.com/EXG1O/Constructor-Telegram-Bots/blob/master/LICENSE.md' target='_blank'>License</a>
					</Col>
					<Col xs={12} lg={3} className='vstack my-1 my-lg-0'>
						<h5 className='mb-0'>{gettext('Контакты Основателя')}</h5>
						<a className='link-secondary link-underline-opacity-0' href='mailto:helper.exg1o@gmail.com' target='_blank'>helper.exg1o@gmail.com</a>
						<a className='link-secondary link-underline-opacity-0' href='https://github.com/EXG1O' target='_blank'>GitHub</a>
						<a className='link-secondary link-underline-opacity-0' href='tg://resolve?domain=exg1o' target='_blank'>Telegram</a>
						<a className='link-secondary link-underline-opacity-0' href='tg://resolve?domain=exg1o_channel' target='_blank'>Telegram Channel</a>
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