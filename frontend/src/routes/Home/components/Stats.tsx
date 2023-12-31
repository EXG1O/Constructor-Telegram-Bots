import React, { ReactNode } from 'react';

import Stack from 'react-bootstrap/Stack';

import InfoArea from 'components/InfoArea';

function Stats(): ReactNode {
	return (
		<Stack className='align-self-center stats' gap={2}>
			<h3 className='mb-0'>{gettext('Информация о сайте')}</h3>
			<Stack gap={1}>
				<InfoArea description={gettext('Количество пользователей')}>0</InfoArea>
				<InfoArea description={gettext('Количество добавленных Telegram ботов')}>1</InfoArea>
				<InfoArea description={gettext('Количество включенных Telegram ботов')}>1</InfoArea>
			</Stack>
		</Stack>
	);
}

export default Stats;