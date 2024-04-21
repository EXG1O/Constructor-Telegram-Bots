import React, { ReactElement, memo } from 'react';

import Input from 'react-bootstrap/FormControl';

import Block, { BlockProps } from './Block';

export type Value = string;

export interface NameProps extends Omit<BlockProps, 'title' | 'onChange' | 'children'> {
	value?: Value;
	onChange: (value: Value) => void;
}

export const defaultValue: Value = '';

function Name({ value = defaultValue, onChange, ...props }: NameProps): ReactElement<NameProps> {
	return (
		<Block {...props} title={gettext('Название')}>
			<Block.Body>
				<Input
					value={value}
					placeholder={gettext('Придумайте название')}
					onChange={e => onChange(e.target.value)}
				/>
			</Block.Body>
		</Block>
	);
}

export default memo(Name);