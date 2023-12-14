import React, { ReactNode } from 'react';

import Modal, { ModalProps } from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

export interface AskConfirmModalProps extends ModalProps {
	title: ReactNode;
	children: ReactNode;
	onConfirmButtonClick: () => void;
}

function AskConfirmModal({ title, children, onConfirmButtonClick, ...modalProps }: AskConfirmModalProps): ReactNode {
	return (
		<Modal {...modalProps}>
			<Modal.Header closeButton>
				<Modal.Title as='h5'>{title}</Modal.Title>
			</Modal.Header>
			<Modal.Body>{children}</Modal.Body>
			<Modal.Footer className='d-flex gap-2'>
				<Button
					variant='success'
					className='flex-fill'
					onClick={onConfirmButtonClick}
				>
					{gettext('Да')}
				</Button>
				<Button
					variant='danger'
					className='flex-fill'
					onClick={modalProps.onHide}
				>
					{gettext('Нет')}
				</Button>
			</Modal.Footer>
		</Modal>
	);
}

export default AskConfirmModal;