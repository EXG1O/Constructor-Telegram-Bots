import React, { ReactElement, ReactNode, memo } from 'react';

import Modal, { ModalProps } from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

import Loading from './Loading';

export interface AskConfirmModalProps extends ModalProps {
	loading?: boolean;
	title: ReactNode;
	children: ReactNode;
	onConfirm?: () => void;
	onCancel?: () => void;
}

function AskConfirmModal({ loading, title, children, onConfirm, onCancel, ...props }: AskConfirmModalProps): ReactElement<AskConfirmModalProps> {
	return (
		<Modal {...props}>
			<Modal.Header closeButton>
				<Modal.Title as='h5'>{title}</Modal.Title>
			</Modal.Header>
			{!loading ? (
				<>
					<Modal.Body>{children}</Modal.Body>
					<Modal.Footer className='d-flex gap-2'>
						<Button
							variant='success'
							className='flex-fill'
							onClick={onConfirm ?? props.onHide}
						>
							{gettext('Да')}
						</Button>
						<Button
							variant='danger'
							className='flex-fill'
							onClick={onCancel ?? props.onHide}
						>
							{gettext('Нет')}
						</Button>
					</Modal.Footer>
				</>
			) : (
				<Modal.Body className='d-flex justify-content-center'>
					<Loading size='md' />
				</Modal.Body>
			)}
		</Modal>
	);
}

export default memo(AskConfirmModal);