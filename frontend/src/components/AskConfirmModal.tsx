import React, { ReactElement, ReactNode, memo } from 'react';

import Modal, { ModalProps } from 'react-bootstrap/Modal';
import Button from 'react-bootstrap/Button';

import Loading from './Loading';

export interface AskConfirmModalProps extends Omit<ModalProps, 'onHide'> {
	loading?: boolean;
	title: ReactNode;
	onConfirmButtonClick: () => void;
	onHide: NonNullable<ModalProps['onHide']>;
}

function AskConfirmModal({ loading, title, children, onConfirmButtonClick, ...props }: AskConfirmModalProps): ReactElement<AskConfirmModalProps> {
	return (
		<Modal {...props}>
			<Modal.Header closeButton>
				<Modal.Title as='h5'>{title}</Modal.Title>
			</Modal.Header>
			{loading ? (
				<Modal.Body>
					<Loading size='md' className='m-auto' />
				</Modal.Body>
			) : (
				<>
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
							onClick={props.onHide}
						>
							{gettext('Нет')}
						</Button>
					</Modal.Footer>
				</>
			)}
		</Modal>
	);
}

export default memo(AskConfirmModal);