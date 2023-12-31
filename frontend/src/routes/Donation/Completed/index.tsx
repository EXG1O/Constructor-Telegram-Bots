import React, { ReactNode } from 'react';

import Container from 'react-bootstrap/Container';

function Completed(): ReactNode {
	return (
		<main className='my-auto'>
			<Container className='my-3 my-lg-4'>
				<h2 className='mb-1'>{gettext('Спасибо за пожертвование сайту!')}</h2>
				<p className='mb-0'>
					{gettext('Спасибо за пожертвование сайту, ваше пожертвование очень сильно поможет развитию и улучшению сайта!')} <br />
					{gettext('Чтобы узнать, было ли ваше пожертвование получено сайтом, вы можете написать основателю сайта в ')} <a href='tg://resolve?domain=exg1o'>Telegram</a> {gettext(' и задать ему этот вопрос.')}
				</p>
			</Container>
		</main>
	);
}

export default Completed;