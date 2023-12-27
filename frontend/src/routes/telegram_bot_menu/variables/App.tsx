import React, { ReactNode, useEffect } from 'react';

import ClipboardJS from 'clipboard';

import Table from 'react-bootstrap/esm/Table';

import TableCell from './components/TableCell';

import useToast from 'services/hooks/useToast';

const variables = {
    [gettext('ID пользователя')]: '{{ user_id }}',
    [gettext('Имя пользователя')]: '{{ user_first_name }}',
    [gettext('Фамилия пользователя')]: '{{ user_last_name }}',
    [gettext('@username пользователя')]: '{{ user_username }}',
    [gettext('ID сообщения пользователя')]: '{{ user_message_id }}',
    [gettext('Текст сообщения пользователя')]: '{{ user_message_text }}',
    [gettext('Данные из базы данных')]: '{{ database_records }}',
    [gettext('Ответ с API-запроса')]: '{{ api_response }}',
}

function App(): ReactNode {
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
		<div className='border rounded p-1'>
			<Table borderless className='overflow-hidden border rounded align-middle mb-0'>
				<tbody>
					{Object.keys(variables).map((variable, index) => (
						<TableCell key={index} header={variable} data={variables[variable]} />
					))}
				</tbody>
			</Table>
		</div>
	);
}

export default App;