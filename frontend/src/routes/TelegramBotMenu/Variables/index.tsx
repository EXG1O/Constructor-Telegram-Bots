import React, { ReactElement, useEffect } from 'react';
import ClipboardJS from 'clipboard';

import SystemVariables from './components/SystemVariables';
import UserVariables from './components/UserVariables';

import useToast from 'services/hooks/useToast';

function Variables(): ReactElement {
	const { createMessageToast } = useToast();

	useEffect(() => {
		const clipboard = new ClipboardJS('.btn-clipboard');

		clipboard.on('success', () => createMessageToast({
			message: gettext('Вы успешно скопировали переменную в буфер обмена.'),
			level: 'success',
		}));
		clipboard.on('error', () => createMessageToast({
			message: gettext('При попытки скопировать переменную в буфер обмена, непредвиденная ошибка!'),
			level: 'danger',
		}));
	}, []);

	return (
		<>
			<SystemVariables />
			<UserVariables />
		</>
	);
}

export default Variables;