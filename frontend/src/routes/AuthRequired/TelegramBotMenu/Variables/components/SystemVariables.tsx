import React, { ReactElement, useState } from 'react';

import Card from 'react-bootstrap/Card';
import ToggleButtonGroup from 'react-bootstrap/ToggleButtonGroup';
import ToggleButton, { ToggleButtonProps } from 'react-bootstrap/ToggleButton';
import Table from 'react-bootstrap/Table';

type VariablesTypes = 'personal' | 'global';

interface VariablesTypeToggleButtonProps extends Omit<ToggleButtonProps, 'key' | 'id' | 'value' | 'size' | 'variant' | 'onChange'> {
	value: VariablesTypes;
}

const variablesTypeToggleButtons: VariablesTypeToggleButtonProps[] = [
	{ value: 'personal', children: gettext('Персональные') },
	{ value: 'global', children: gettext('Глобальные') },
];

interface Variables {
	variable: string;
	description: string;
}

const variables: Record<VariablesTypes, Variables[]> = {
	personal: [
		{ variable: 'USER_ID', description: gettext('ID пользователя') },
		{ variable: 'USER_USERNAME', description: gettext('@username пользователя') },
		{ variable: 'USER_FIRST_NAME', description: gettext('Имя пользователя') },
		{ variable: 'USER_LAST_NAME', description: gettext('Фамилия пользователя') },
		{ variable: 'USER_FULL_NAME', description: gettext('Имя и фамилия пользователя') },
		{ variable: 'USER_MESSAGE_ID', description: gettext('ID сообщения пользователя') },
		{ variable: 'USER_MESSAGE_TEXT', description: gettext('Текст сообщения пользователя') },
	],
	global: [
		{ variable: 'BOT_NAME', description: gettext('Название бота') },
		{ variable: 'BOT_USERNAME', description: gettext('@username бота') },
	],
}

function SystemVariables(): ReactElement {
	const [variablesType, setVariablesType] = useState<VariablesTypes>('personal');

	return (
		<Card className='border'>
			<Card.Header as='h5' className='border-bottom text-center'>
				{gettext('Системные переменные')}
			</Card.Header>
			<Card.Body className='vstack gap-2'>
				<div className='col col-lg-3'>
					<ToggleButtonGroup
						type='radio'
						name='systemVariablesTypes'
						defaultValue='personal'
						className='w-100'
					>
						{variablesTypeToggleButtons.map((props, index) => (
							<ToggleButton
								{...props}
								key={index}
								id={`btn-radio-system-variables-type-${props.value}`}
								size='sm'
								variant='outline-dark'
								onChange={() => setVariablesType(props.value)}
							/>
						))}
					</ToggleButtonGroup>
				</div>
				<div className='border rounded'>
					<Table responsive borderless striped className='overflow-hidden rounded mb-0'>
						<tbody>
							{variables[variablesType].map((data, index) => (
								<tr key={index}>
									<td className='w-50'>
										<div className='d-flex gap-2'>
											<i
												className='btn-clipboard bi bi-clipboard'
												data-clipboard-text={data.variable}
												style={{ cursor: 'pointer' }}
											/>
											<span className='flex-fill text-info-emphasis'>
												{data.variable}
											</span>
										</div>
									</td>
									<td className='text-nowrap'>
										{data.description}
									</td>
								</tr>
							))}
						</tbody>
					</Table>
				</div>
			</Card.Body>
		</Card>
	);
}

export default SystemVariables;