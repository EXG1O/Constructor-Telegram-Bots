import React, { ReactElement, memo, useCallback, useState } from 'react';

import AddButton, { AddButtonProps } from 'components/AddButton';

import VariableAdditionModal from './VariableAdditionModal';

export type AddVariableButtonProps = Pick<AddButtonProps, 'className' | 'style'>;

function AddVariableButton(props: AddVariableButtonProps): ReactElement<AddVariableButtonProps> {
	const [showModal, setShowModal] = useState<boolean>(false);

	return (
		<>
			<VariableAdditionModal
				show={showModal}
				onHide={useCallback(() => setShowModal(false), [])}
			/>
			<AddButton
				{...props}
				size='sm'
				variant='dark'
				onClick={useCallback(() => setShowModal(true), [])}
			>
				{gettext('Добавить переменную')}
			</AddButton>
		</>
	);
}

export default memo(AddVariableButton);