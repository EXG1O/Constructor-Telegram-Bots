import React, { ReactElement } from 'react';

import Stack from 'react-bootstrap/Stack';

import InfoArea from 'components/InfoArea';

function Stats(): ReactElement {
	return (
		<div className='stats'>
			<h3>{gettext('Информация о сайте')}</h3>
			<Stack gap={1}>
				<InfoArea value={0}>
					{gettext('Количество пользователей')}
				</InfoArea>
				<InfoArea value={1}>
					{gettext('Количество добавленных Telegram ботов')}
				</InfoArea>
				<InfoArea value={1}>
					{gettext('Количество включенных Telegram ботов')}
				</InfoArea>
			</Stack>
		</div>
	);
}

export default Stats;