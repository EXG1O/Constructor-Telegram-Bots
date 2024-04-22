import React, { ReactElement, memo } from 'react';

import TelegramQuillEditor from 'components/TelegramQuillEditor';

import Block, { BlockProps } from '../../Block';

export type Value = string;

export interface MessageBlockProps extends Omit<BlockProps, 'title' | 'onChange' | 'children'> {
	value?: Value;
	onChange: (value: Value) => void;
}

export const defaultValue: Value = '';

function MessageBlock({ value = defaultValue, onChange, ...props }: MessageBlockProps): ReactElement<MessageBlockProps> {
	return (
		<Block {...props} title={gettext('Сообщение')}>
			<Block.Body>
				<TelegramQuillEditor
					height={220}
					value={value}
					placeholder={gettext('Введите текст')}
					onChange={onChange}
				/>
			</Block.Body>
		</Block>
	);
}

export default memo(MessageBlock);