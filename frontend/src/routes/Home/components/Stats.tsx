import React, { ReactElement } from 'react';

import Stack from 'react-bootstrap/Stack';

import InfoArea from 'components/InfoArea';

function Stats(): ReactElement {
	return (
		<Stack className='align-self-center stats' gap={2}>
			<h3 className='mb-0'>{gettext('Информация о сайте')}</h3>
			<Stack gap={1}>
				<InfoArea value={0} description={gettext('Количество пользователей')} />
				<InfoArea value={1} description={gettext('Количество добавленных Telegram ботов')} />
				<InfoArea value={1} description={gettext('Количество включенных Telegram ботов')} />
			</Stack>
		</Stack>
	);
}

export default Stats;