import React, { ReactNode } from 'react';

import Stack from 'react-bootstrap/Stack';

function Header(): ReactNode {
	return (
		<Stack className='align-self-center header' gap={2}>
			<h1 className='fw-semibold mb-0'>Constructor Telegram Bots</h1>
			<p className='lead mb-0'>{gettext('Сайт, с помощью которого вы можете легко, бесплатно и без каких-либо знаний в программировании, создать своего многофункционального Telegram бота.')}</p>
		</Stack>
	);
}

export default Header;