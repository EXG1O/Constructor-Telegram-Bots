import React, { ReactElement, HTMLAttributes, memo, useCallback, useState } from 'react';
import classNames from 'classnames';

import VariableEditModal from './VariableEditModal';

import { Variable } from 'services/api/telegram_bots/types';

export interface EditVariableButtonProps extends Pick<HTMLAttributes<HTMLElement>, 'className'> {
	variable: Variable;
}

function EditVariableButton({ variable, className }: EditVariableButtonProps): ReactElement<EditVariableButtonProps> {
	const [showModal, setShowModal] = useState<boolean>(false);

	return (
		<>
			<VariableEditModal
				variable={variable}
				show={showModal}
				onHide={useCallback(() => setShowModal(false), [])}
			/>
			<i
				className={classNames('d-flex text-secondary bi bi-pencil-square', className)}
				style={{ fontSize: '18px', cursor: 'pointer' }}
				onClick={() => setShowModal(true)}
			/>
		</>
	);
}

export default memo(EditVariableButton);