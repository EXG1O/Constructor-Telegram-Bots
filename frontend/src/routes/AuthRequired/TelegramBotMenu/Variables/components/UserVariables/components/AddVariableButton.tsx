import React, { ReactElement, memo, useCallback, useState } from 'react';

import AddButton, { AddButtonProps } from 'components/AddButton';

import VariableAdditionModal from './VariableAdditionModal';

export type AddVariableButtonProps = Omit<AddButtonProps, 'size' | 'variant'>;

function AddVariableButton({ onClick, ...props }: AddVariableButtonProps): ReactElement<AddVariableButtonProps> {
	const [showModal, setShowModal] = useState<boolean>(false);

	const handleClick = useCallback((event: React.MouseEvent<HTMLButtonElement, MouseEvent>) => {
		setShowModal(true);
		onClick?.(event);
	}, [onClick]);

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
				onClick={handleClick}
			>
				{gettext('Добавить переменную')}
			</AddButton>
		</>
	);
}

export default memo(AddVariableButton);