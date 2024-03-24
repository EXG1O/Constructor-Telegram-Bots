import React, { HTMLAttributes, ReactElement, memo, useState } from 'react';
import classNames from 'classnames';

import InputGroup from 'react-bootstrap/InputGroup';
import Form from 'react-bootstrap/Form';
import Collapse from 'react-bootstrap/Collapse';
import Button from 'react-bootstrap/Button';

import useVariables from '../hooks/useVariables';

export type NameSearchProps = Pick<HTMLAttributes<HTMLDivElement>, 'className'>;

function NameSearch({ className }: NameSearchProps): ReactElement<NameSearchProps> {
	const [name, setName] = useState<string>('');

	const { updateVariables } = useVariables();

	function handleClearButtonClick(): void {
		setName('');
		updateVariables(undefined, undefined, '');
	}

	return (
		<div className={classNames('d-flex', className)}>
			<InputGroup size='sm'>
				<i
					className='d-flex align-items-center bi bi-search text-bg-light border rounded-start-1 px-2'
					style={{ fontSize: '14px' }}
				/>
				<Form.Control
					value={name}
					placeholder={gettext('Введите имя')}
					onChange={e => setName(e.target.value)}
				/>
				<Collapse in={Boolean(name)} dimension='width' unmountOnExit>
					<div>
						<Button
							variant='light'
							className='d-flex align-items-center bi bi-x border rounded-start-0 rounded-end-1 h-100 p-0'
							style={{ fontSize: '21px' }}
							onClick={handleClearButtonClick}
						/>
					</div>
				</Collapse>
			</InputGroup>
			<div>
				<Collapse in={Boolean(name)} dimension='width'>
					<div>
						<Button
							size='sm'
							variant='dark'
							className='ms-2'
							onClick={() => updateVariables(undefined, undefined, name)}
						>
							{gettext('Найти')}
						</Button>
					</div>
				</Collapse>
			</div>
		</div>
	);
}

export default memo(NameSearch);