import React, { ReactElement } from 'react';
import { Params, json, useRouteLoaderData } from 'react-router-dom';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import TelegramBotCard from 'components/TelegramBotCard';

import { LoaderData as TelegramBotMenuRootLoaderData } from 'routes/AuthRequired/TelegramBotMenu/Root';

import TelegramBotCardFooter from './components/TelegramBotCardFooter';

function Index(): ReactElement {
	const { telegramBot } = useRouteLoaderData('telegram-bot-menu-root') as TelegramBotMenuRootLoaderData;

	return (
		<Row className='g-3 g-lg-4'>
			<Col xs={12} lg={6}>
				<TelegramBotCard telegramBot={telegramBot}>
					{props => (
						<TelegramBotCardFooter {...props} />
					)}
				</TelegramBotCard>
			</Col>
		</Row>
	);
}

export default Index;