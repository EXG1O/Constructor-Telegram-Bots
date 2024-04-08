import React, { ReactElement } from 'react';

import ToggleButtonGroup, { ToggleButtonRadioProps } from 'react-bootstrap/ToggleButtonGroup';
import ToggleButton, { ToggleButtonProps } from 'react-bootstrap/ToggleButton';

import { Type } from '../../..';

import useUsers from '../../../hooks/useUsers';

export type TypeToggleButtonGroupProps = Omit<ToggleButtonRadioProps<Type>, 'type' | 'name' | 'children'>;

interface TypeToggleButtonProps extends Omit<ToggleButtonProps, 'key' | 'id' | 'value' | 'size' | 'variant' | 'onChange'> {
	value: Type;
}

const typeToggleButtons: TypeToggleButtonProps[] = [
	{ value: 'all', children: gettext('Все') },
	{ value: 'allowed', children: gettext('Разрешённые') },
	{ value: 'blocked', children: gettext('Заблокированные') },
];

function TypeToggleButtonGroup(props: TypeToggleButtonGroupProps): ReactElement<TypeToggleButtonGroupProps> {
	const { updateUsers, filter } = useUsers();

	return (
		<ToggleButtonGroup
			{...props}
			type='radio'
			name='user-types'
			value={filter.type}
			onChange={type => updateUsers(undefined, undefined, undefined, type)}
		>
			{typeToggleButtons.map((props, index) => (
				<ToggleButton
					{...props}
					key={index}
					id={`user-types-${props.value}`}
					size='sm'
					variant='outline-dark'
				/>
			))}
		</ToggleButtonGroup>
	);
}

export default TypeToggleButtonGroup;